"""
Created by Danil Lykov @danlkv on 14/02/19
"""
import zmq, os, time
import json
from pprint import pprint
import multiprocessing as prc
try:
    from utils__ import themify, dethemify, get_network_config
except ImportError:
    from core.utils import themify, dethemify, get_network_config


class Module:
    """
    A base class for Goal Net data processing modules
    """
    def __init__(self, netconf,name='baseModule'):
        self.source = self._get_mux_socket(netconf)
        self.sink = self._get_dmx_socket(netconf)
        self.name = name

    def _print(self,*args):
        print(">%sModule>"%self.name, *args)

    def _get_dmx_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUSH)
        s.connect(netconf.get_address("DMX"))
        return s
    def _get_mux_socket(self,netconf,topics=[b'']):
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        for topic in topics:
            s.setsockopt(zmq.SUBSCRIBE, topic)
        s.connect(netconf.get_address("MUX_out"))
        return s
    #---- explore if we need this?
    def _get_mux_socket_pull(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PULL)
        s.connect(netconf.get_address("MUX_out"))
        return s
    #----

    def _recv(self):
        raw = self.source.recv_string()
        topic, msg = dethemify(raw)
        return msg

    def run_function(self):
        self._print("running...")
        while True:
            msg = self._recv()
            notif = self.handle_action(msg)
            self._send(notif)

    def _send(self,notif):
        if notif:
            self.sink.send_json(notif)

    def handle_action(self,msg):
        self._print("Do not use base class per se")
        return None

    def start(self):
        self.run_function()

    def start_parallel(self):
        process = prc.Process(target=self.run_function, name=self.name)
        process.start()

