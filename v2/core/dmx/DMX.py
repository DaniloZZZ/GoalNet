"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint

import multiprocessing as prc
from ..utils import themify, dethemify, get_network_config

def DMX(my_name, network_config):
    print("DMX is listening named as:%s"%my_name)
    source_addr = network_config.get_address(my_name)
    # But maybe use PUB-SUB for output ??
    ###> Prepare the zmq sockets
    ctx = zmq.Context()
    source = ctx.socket(zmq.PULL)
    print("Binding DMX pull to",source_addr)
    source.bind( source_addr )
    #-----
    connectors  = ['console']
    conn_addr = [(conn, network_config.get_address(conn)) for conn in connectors ]
    sockets = {}
    for name, addr in conn_addr:
        sock = ctx.socket(zmq.REQ)
        sock.connect(addr)
        sockets[name] = sock
    ###<
    while True:
        notif = source.recv_json()
        print("DMX in:")
        print(notif)
        for name,socket in sockets.items():
            print("Sending notif to %s connector"%name)
            socket.send_json(notif)
        for name,socket in sockets.items():
            print("getting answer %s connector"%name)
            answer = socket.recv_string()
            print('dmx %s answ'%name,answer)

def start_dmx():
    netconf = get_network_config()
    p = prc.Process(target=DMX,args=('DMX',netconf),name='dmx')
    p.start()

def main():
    print("Starting DMX node...")
    start_dmx()

if __name__=='__main__':
    main()
