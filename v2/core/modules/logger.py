"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint

def themify(topic,msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

def dethemify(topicmsg):
    """ Inverse of themify() """
    json0 = topicmsg.find('{')
    topic = topicmsg[0:json0].strip()
    msg = json.loads(topicmsg[json0:])
    return topic, msg

class LoggerModule:
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf,name='logger'):
        #TODO: make a base class of module that will use netconf to get provider
        self.source = self._get_mux_socket(netconf)
        self.sink = self._get_dmx_socket(netconf)

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

    def start(self):
        while True:
            msg = self._recv()
            print("Logger got action")
            print("log",msg)

def launch_logger(name,netconf):
    logm = LoggerModule(netconf,name=name)
    logm.start()
