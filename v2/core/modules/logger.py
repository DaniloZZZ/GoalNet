"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint
import multiprocessing as prc

from ..utils import themify, dethemify, get_network_config

def _print(*args):
    print(">LoggerModule>",*args)

class LoggerModule:
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf,name='logger'):
        #TODO: make a base class of module that will use netconf to get provider
        self.source = self._get_mux_socket(netconf)
        self.sink = self._get_dmx_socket(netconf)
        self.name = name

    def _get_dmx_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUSH)
        s.connect(netconf.get_address("DMX"))
        return s
    def _recv(self):
        raw = self.source.recv_string()
        topic,msg = dethemify(raw)
        return msg
    def _get_mux_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        s.setsockopt(zmq.SUBSCRIBE, b'')
        s.connect(netconf.get_address("MUX_out"))
        return s

    def run_function(self):
        _print("running...")
        while True:
            msg = self._recv()
            _print("Logger got action")
            _print(msg)

    def start(self):
        process = prc.Process(target=self.run_function, name=self.name)
        process.start()

def launch_logger(name,netconf):
    logm = LoggerModule(netconf,name=name)
    logm.run_function()

def main():
    print("Starting logger module node...")
    netconf = get_network_config()
    launch_logger('logger',netconf)

if __name__=='__main__':
    main()
