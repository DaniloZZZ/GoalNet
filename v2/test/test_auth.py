"""
Test modules for starting
Written by Danli Lykov on 16.03.19

"""
import sys,time
import numpy as np

import  unittest
import trio
import zmq, requests, json
import goalnet as g
from trio_websocket import ConnectionClosed
from goalnet.helpers.log_init import log
from pprint import pprint
import multiprocessing as proc
import websocket as ws

from goalnet.utils import get_network_config
from goalnet.connectors import NetworkAPI
from goalnet.helpers.wsclient import ws_req_rep
from goalnet.connectors import start_websocket
from goalnet.connectors import start_login_http

def processed(f, *args,name=None):
    process = proc.Process(target=f, args=args, name=name)
    process.start()
    return process

class TestModules(unittest.TestCase):
    def __init__(self,a):
        super().__init__(a)
        self.login_url = 'http://localhost:8919/login'
        self.main_url = 'http://localhost:8919/'
        self.url = 'ws://127.0.0.1:3032'

    def setUp(self):
        self.conf_process = process = g.start_cnf()
        self.mux_p = g.start_mux(parallel=True)
        self.dmx_p = g.start_dmx(connectors=['websocket','login'], parallel=True)
        self.db_process = g.start_module('database')
        self.db_node = g.start_database()
        self.wsproc = processed(start_websocket, name='ws-connector')
        self.flask = processed(start_login_http, name='login_http-conn')
        time.sleep(0.1)

    def tearDown(self):
        print("TeadDown test Terminating processes")
        for p in [
            self.conf_process,
            self.mux_p,
            self.dmx_p,
            self.db_process,
            self.wsproc,
            self.flask
        ]:
            #p.terminate()
            p.join()
        self.db_node.terminate()
        print("done")

    def login(self,email,pwd):
        auth_payload={'email':email,'pwd':pwd}
        r = requests.post( self.login_url, data=auth_payload , allow_redirects=False)
        print("login: response.text\n",r.text)
        print("login: response.cookies\n",r.cookies)
        token = r.cookies.get('token')
        return token

    def test_login(self):
        print("\n******\nTest login ")
        token = self.login('example@goalnet.test','0xDEAD:BEEF')
        cookies = {'token':token}
        r = requests.get( self.main_url, cookies=cookies, allow_redirects=False)
        self.assertEqual(r.headers['Location'], 'http://localhost:8080', "Redirects to main page if OK")

    def test_main_page(self):
        r = requests.get( self.main_url, allow_redirects=False)
        self.assertEqual(r.status_code, 302, "Redirects to login page if no token")
        self.assertEqual(r.headers['Location'], 'http://localhost:8080/login', "Redirects to login page if no token")

        cookies = {'token':"invalid token"}
        r = requests.get( self.main_url, cookies=cookies, allow_redirects=False)
        self.assertEqual(r.status_code, 302, "Redirects to login page if invalid")
        self.assertEqual(r.headers['Location'], 'http://localhost:8080/login', "Redirects to login page if invalid")


    def test_send(self):
        print("\n******\nTest login + send")
        token = self.login('example@goalnet.test','0xDEAD:BEEF')
        msg = {
            "test":'foo'
        }
        print("\nLogin done, waiting a bit")
        time.sleep(.05)
        conn = ws.create_connection(self.url)
        message_out = {'action':'world','token':token}
        conn.send(json.dumps(message_out))
        message = conn.recv()
        resp = json.loads(message)
        print("\nIN<<\n",resp)

        msgauth = {'token':"oxdeadbeef"}
        print("\nMaking an invalid request")
        try:
            resp = ws_req_rep(self.url, [msgauth,msg])
        except ConnectionClosed as e:
            print(e)
            assert e.reason.code==1008
        print("\nIN<<\n",resp)


if __name__=="__main__":
    unittest.main()



