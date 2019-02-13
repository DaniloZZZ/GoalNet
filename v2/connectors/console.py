"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint
import multiprocessing.dummy as thr
import multiprocessing as prc
from utils import get_network_config

class ConsoleConnector:
    """
    A simple connector that sends text messages on behaf of user with id 1
    """
    def __init__(self,netconf,name='console'):
        self.sink = self._get_mux_socket(netconf)
        self.name = name
        self.source = self._get_source_socket(name,netconf)
        self.appid = '1'

    def _get_source_socket(self, name, netconf):
        my_addr = netconf.get_address(name)
        ctx = zmq.Context()
        s = ctx.socket(zmq.REP)
        print("Console connector is listening at %s named %s"%(my_addr,name))
        s.bind(my_addr)
        return s

    def _get_mux_socket(self,netconf):
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUSH)
        s.connect(netconf.get_address("MUX_in"))
        return s

    def run_function(self,pipe):
        #text,notif =None,None
        def listen_for_notif():
            print("console connector listening for notification...")
            while True:
                notif = self.source.recv_json()
                print('console got notif:',notif)
                self.source.send_string("CONSOLE OK")
        #listener = thr.Process(target=listen_for_input)
        notificator = thr.Process(target=listen_for_notif)
        #listener.start()
        notificator.start()
        while True:
            text =pipe.recv()
            self.send(text)
            time.sleep(0.01)

    def send(self,text):
        msg = {
            'text':text,
            'user_id':1,
            'appid':self.appid
        }
        self.sink.send_json(msg)

    def start_listen(self):
        inp, out = prc.Pipe()
        self.run_function(pipe)
        while True:
            text = input("Console input>>>")
            self.send(text)

    def start_listen_threaded(self):
        inp, out = thr.Pipe()
        process = thr.Process(target=self.run_function,
                args=(inp,), name=self.name)
        process.start()
        while True:
            time.sleep(0.01)
            text = input("Console input>>>")
            self.send(text)

    def start(self, pipe):
        self.run_function(pipe)

def launch_console_connector(name,netconf,pipe):
    consonn= ConsoleConnector(netconf,name=name)
    consonn.start(pipe)

def main():
    print("Starting console connector node...")
    netconf = get_network_config()
    consonn= ConsoleConnector(netconf,name='console')
    consonn.start_listen_threaded()

if __name__=='__main__':
    main()
