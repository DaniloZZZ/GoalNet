"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq
import yaml,json
import os
config_file = os.environ.get("GNET_CONFIG_YML") or '/home/danlkv/GoalNet/v2/config.yml'

def themify(topic,msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

def dethemify(topicmsg):
    """ Inverse of themify() """
    json0 = topicmsg.find('{')
    topic = topicmsg[0:json0].strip()
    msg = json.loads(topicmsg[json0:])
    return topic, msg

def read_yaml(name):
    with open(name, 'r') as stream:
        data= yaml.load(stream)
    return data

def read_config():
    config = read_yaml(config_file)
    return config

def get_config_server_addr():
    return read_config()['config_address']

def get_network_config():
    ctx = zmq.Context()
    s = ctx.socket(zmq.REQ)
    addr = get_config_server_addr()
    print("Getting network config from %s..."%addr, end=" ", flush=True)
    s.connect(addr)
    s.send_string('netconfig')
    netconf = s.recv_json()
    print("done")
    return NetworkConfig(netconf)

class NetworkConfig:
    """
    This class stores config and lets process get network addresses to connect
    TODO:
    generate personalized configs to take into account whether processes run on the same machine
    """
    def __init__(self, conf={}):
        self.conf = conf

    def add_node(self,name,address):
        self.conf[name] = address

    def get_address(self,name):
        return self.conf[name]

    def __repr__(self):
        return self.conf.__repr__()
