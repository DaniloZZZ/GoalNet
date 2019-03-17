"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint, pformat
import logging as log

import multiprocessing as prc
from ..utils import themify, get_network_config

def themify(topic,msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

def filter_action(action):
    """
    check if specified connector has rights to send actions
    on the behaf of a user
    check app id of connector
    """
    return True
    if not action.get('app_id'):
        return None
    if not action.get('user_id'):
        return None
    return action

def MUX(my_name, network_config):
    log.info("MUX is listening  named as:%s"%(my_name))
    source_addr = network_config.get_address(my_name+'_in')
    sink_addr = network_config.get_address(my_name+'_out')
    ###> Prepare the zmq sockets
    ctx = zmq.Context()
    source = ctx.socket(zmq.PULL)
    log.debug("Binding MUX in to %s",source_addr)
    source.bind( source_addr )
    #----
    sink = ctx.socket(zmq.PUB)
    log.debug("Binding MUX out to %s",sink_addr)
    sink.bind( sink_addr )
    ###<
    while True:
        action = source.recv_json()
        log.debug("MUX<<:%s"%(action))
        send_action = filter_action(action)
        if send_action:
            topic = action.get('action','')
            log.debug("Sending message of action '%s'. User id: %d"%(topic,action.get('user_id',0)))
            sink.send_string(themify(topic, action))
        else:
            log.warn("Action forbidden:%s"%(action))

def start_mux():
    netconf = get_network_config()
    p = prc.Process(target=MUX,args=('MUX',netconf),name='mux')
    p.start()

def main():
    log.info("Starting MUX node...")
    start_mux()

if __name__=='__main__':
    main()

