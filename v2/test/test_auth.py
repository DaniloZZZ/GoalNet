"""
Test modules for starting
Written by Danli Lykov on 16.03.19

"""
import sys,time
import numpy as np

import unittest
import trio
import zmq, requests, json
import goalnet as g
from goalnet.helpers.log_init import log
from pprint import pprint
import multiprocessing as proc

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
        self.login_url = 'http://localhost:8919'
        self.url = 'ws://127.0.0.1:3032'

    def setUp(self):
        self.conf_process = process = g.start_cnf()
        self.mux_p = g.start_mux(parallel=True)
        self.dmx_p = g.start_dmx(connectors=['websocket','login'], parallel=True)
        self.db_process = g.start_module('database')
        self.wsproc = processed(start_websocket, name='ws-connector')
        self.flask = processed(start_login_http, name='login_http-conn')
        time.sleep(0.15)

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
        print("done")

    def login(self,email,pwd):
        auth_payload={'email':email,'pwd_hash':pwd}
        r = requests.post( self.login_url, data=auth_payload )
        print("login: response.text\n",r.text)
        resp = json.loads(r.text)
        user_id = resp['user_id']
        token = resp['token']
        return user_id, token

    def test_login(self):
        print("\n******\nTest login ")
        self.login('example@goalnet.test','0xDEAD:BEEF')

    def test_send(self):
        print("\n******\nTest login + send")
        user_id, token = self.login('example@goalnet.test','0xDEAD:BEEF')
        msg = {
            "test":'foo'
        }
        print("\nLogin done, waiting a bit")
        time.sleep(.05)
        msgauth = {'token':token}
        print("\nmaking request")
        resp = ws_req_rep(self.url, [msgauth,msg])
        print("\nIN<<\n",resp)


if __name__=="__main__":
    unittest.main()



