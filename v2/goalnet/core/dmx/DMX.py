"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint
from goalnet.helpers.log_init import log

import multiprocessing as prc
from ..utils import themify, dethemify, get_network_config

def DMX(my_name, network_config, connectors=[]):
    log.info("DMX is listening named as:%s"%my_name)
    log.info("DMX connectors: %s"%connectors)
    source_addr = network_config.get_address(my_name)
    # But maybe use PUB-SUB for output ??
    ###> Prepare the zmq sockets
    ctx = zmq.Context()
    source = ctx.socket(zmq.PULL)
    log.debug("Binding DMX pull to %s"%source_addr)
    source.bind( source_addr )
    #-----
    #connectors  = ['console','telegram']
    conn_addr = [(conn, network_config.get_address(conn)) for conn in connectors ]
    sockets = {}
    for name, addr in conn_addr:
        sock = ctx.socket(zmq.REQ)
        sock.connect(addr)
        if name=='login':
            trig='auth'
        else:
            trig = ''
        sockets[name] = {'socket': sock,'trig':trig}
    ###<
    while True:
        notif = source.recv_json()
        log.debug("DMX in: %s"%notif)
        for name,props in sockets.items():
            socket = props['socket']
            target = notif.get('action')
            if props['trig']:
                if not target: continue
                m = target.split('.')
                if not len(m)>2: continue
                if m[2]!=props['trig']:
                    continue
            log.debug("Sending notif to %s connector"%name)
            socket.send_json(notif)
        for name,props in sockets.items():
            socket = props['socket']
            target = notif.get('action')
            if props['trig']:
                if not target: continue
                m = target.split('.')
                if not len(m)>2: continue
                if m[2]!=props['trig']:
                    continue
            log.debug("getting answer %s connector"%name)
            answer = socket.recv_string()
            log.debug('dmx %s answ %s'%(name,answer))

def start_dmx():
    netconf = get_network_config()
    p = prc.Process(target=DMX,args=('DMX',netconf),name='dmx')
    p.start()

def main():
    print("Starting DMX node...")
    start_dmx()

if __name__=='__main__':
    main()
