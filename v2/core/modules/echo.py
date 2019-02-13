"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint
import multiprocessing as prc

from ..utils import themify, dethemify, get_network_config
def _print(*args):
    print(">EchoModule>",*args)

class EchoModule:
    """
    A simple module that passes everything unchanged as notification
    """
    def __init__(self, netconf,name='echo'):
        #TODO: make a base class of module that will use netconf to get provider
        self.source = self._get_mux_socket(netconf)
        self.sink = self._get_dmx_socket(netconf)
        self.name = name

    def _get_dmx_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUSH)
        s.connect(netconf.get_address("DMX"))
        return s
    def _get_mux_socket_pull(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PULL)
        s.connect(netconf.get_address("MUX_out"))
        return s
    def _get_mux_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        s.setsockopt(zmq.SUBSCRIBE, b'')
        s.connect(netconf.get_address("MUX_out"))
        return s

    def _recv(self):
        raw = self.source.recv_string()
        topic,msg = dethemify(raw)
        return msg

    def run_function(self):
        _print("running...")
        while True:
            msg = self._recv()
            _print("got action")
            #time.sleep(0.01)
            self.sink.send_json(msg)

    def start(self):
        process = prc.Process(target=self.run_function, name=self.name)
        process.start()

def launch_echo(name,netconf):
    echom = EchoModule(netconf,name=name)
    echom.run_function()

def main():
    print("Starting echo module node...")
    netconf = get_network_config()
    launch_echo('echo',netconf)

if __name__=='__main__':
    main()
