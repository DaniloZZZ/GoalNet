"""
Test actions of user
Written by Danli Lykov on 24.03.19

"""
import sys,time
import numpy as np

import unittest
import requests, json
import goalnet as g
from goalnet.helpers.log_init import log
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
            p.terminate()
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

    def test_modules_add(self):
        print("\n******\nTest modules add")
        token = self.login('example@goalnet.test','0xDEAD:BEEF')
        conn = ws.create_connection(self.url)
        message_out = {'action':'add.user.module','token':token,'name':'test'}
        conn.send(json.dumps(message_out))
        message = conn.recv()
        resp = json.loads(message)
        print("\nIN<<\n",resp)
        message_out = {'action':'get.user.module'}
        conn.send(json.dumps(message_out))
        message = conn.recv()
        resp = json.loads(message)
        print("\nIN<<\n",resp)

if __name__=="__main__":
    unittest.main()



