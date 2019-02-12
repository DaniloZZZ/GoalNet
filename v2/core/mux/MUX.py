"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint


def themify(topic,msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

def filter_action(action):
    """
    check if specified connector has rights to send actions
    on the behaf of a user
    check app id of connector
    """
    if not action.get('appid'):
        return None
    if not action.get('user_id'):
        return None
    else:
        return action

def MUX(my_name, network_config):
    print("MUX is listening  named as:%s"%(my_name))
    source_addr = network_config.get_address(my_name+'_in')
    sink_addr = network_config.get_address(my_name+'_out')
    ###> Prepare the zmq sockets
    ctx = zmq.Context()
    source = ctx.socket(zmq.PULL)
    print("Binding MUX in to",source_addr)
    source.bind( source_addr )
    #----
    sink = ctx.socket(zmq.PUB)
    print("Binding MUX out ",sink_addr)
    sink.bind( sink_addr )
    ###<
    while True:
        action = source.recv_json()
        print("MUX in action:")
        print(action)
        action = filter_action(action)
        if action:
            print("MUX out")
            sink.send_string(themify('module',action))
        else:
            print("action forbidden")

