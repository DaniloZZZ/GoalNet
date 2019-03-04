"""
Created by Danil Lykov @danlkv on 14/02/19
"""
import zmq, os, time
import json
from pprint import pprint
import multiprocessing as prc
from goalnet.helpers.log_init import log
from goalnet.core.utils import themify, dethemify, get_network_config
import trio

class Module:
    """
    A base class for Goal Net data processing modules
    """
    def __init__(self, netconf,name='baseModule'):
        self.source = self._get_mux_socket(netconf)
        self.drain = self._get_dmx_socket(netconf)
        self.name = name

    def _print(self,msg):
        log.info(msg)

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

    def _recv(self):
        raw = self.source.recv_string()
        topic, msg = dethemify(raw)
        return msg

    def server_listen_loop(self):
        self._print("running...")
        while True:
            msg = self._recv()
            notif = self.handle_action(msg)
            if notif:
                self._print('sending',notif)
                self.drain.send_json(notif)

    @abstractmethod
    def handle_action(self,msg):
        pass

    def start(self):
        self.server_listen_loop()

    def start_parallel(self):
        process = prc.Process(target=self.server_listen_loop, name=self.name)
        process.start()

