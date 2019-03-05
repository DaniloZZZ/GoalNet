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

class BaseModule:
    """
    A base class for Goal Net data processing modules
    """
    def __init__(self, netconf,name='baseModule'):
        self.netconf = netconf
        self.source = self._get_mux_socket()
        self.drain = self._get_dmx_socket()
        self.name = name

    def _print(self,msg):
        """
        A simple wrapper of loggin to maybe pass some
        internal params to log
        """
        log.info(msg)

    """
    Some methods to get sockets of MUX and DMX
    """
    def _get_dmx_socket(self):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUSH)
        s.connect(self.netconf.get_address("DMX"))
        return s
    def _get_mux_socket(self,topics=[b'']):
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        for topic in topics:
            s.setsockopt(zmq.SUBSCRIBE, topic)
        s.connect(self.netconf.get_address("MUX_out"))
        return s

    def _recv(self):
        """
        wrapper for receiving a data from sub socket
        need to get topic first, then parse json from 
        remaining data
        """
        raw = self.source.recv_string()
        topic, msg = dethemify(raw)
        return msg

    def handle_action(self,msg):
        raise NotImplementedError

    def server_listen_loop(self):
        """
        Loop forever and apply handle_action to
        every message, then send result to dmx if any
        """
        self._print("running...")
        while True:
            msg = self._recv()
            notif = self.handle_action(msg)
            if notif:
                self._print('sending',notif)
                self.drain.send_json(notif)


    def start(self):
        self.server_listen_loop()

    def start_process(self):
        process = prc.Process(target=self.start, name=self.name)
        process.start()
        self.process = process

