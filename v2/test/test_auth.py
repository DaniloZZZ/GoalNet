"""
Test modules for starting
Written by Danli Lykov on 16.03.19

"""
import sys,time
import numpy as np

import unittest
import zmq, requests
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
    def setUp(self):
        self.conf_process = process = g.start_cnf()
        self.mux_p = g.start_mux(parallel=True)
        self.dmx_p = g.start_dmx(connectors=['websocket','login'], parallel=True)
        self.db_process = g.start_module('database')
        self.wsproc = processed(start_websocket, name='ws-connector')
        self.flask = processed(start_login_http, name='login_http-conn')
        time.sleep(0.01)

    def tearDown(self):
        #print("Terminating conf server process")
        for p in [
            self.conf_process,
            self.mux_p,
            self.dmx_p,
            self.db_process,
            self.wsproc
        ]:
            p.terminate()
            p.join()


    def test_db_metrics(self):
        time.sleep(0.01)
        login_url = 'http://localhost:8919'
        url = 'ws://127.0.0.1:3032'
        auth_payload={'email':'example@goalnet.test','pwd_hash':'0xDEAD:BEEF'}
        r = requests.post( login_url, data=auth_payload )
        print("r.text",r.text)


if __name__=="__main__":
    unittest.main()



