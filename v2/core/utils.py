import zmq
import yaml,json

def themify(topic,msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

def dethemify(topicmsg):
    """ Inverse of themify() """
    json0 = topicmsg.find('{')
    topic = topicmsg[0:json0].strip()
    msg = json.loads(topicmsg[json0:])
    return topic, msg

config_file = 'config.yml'

def read_yaml(name):
    with open(name, 'r') as stream:
        data= yaml.load(stream)
    return data

def read_config():
    config = read_yaml(config_file)
    return config

def get_config_server_addr():
    return read_config()['config_address']

ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
def get_network_config():
    addr = get_config_server_addr()
    s.connect(addr)
    s.send_string('netconfig')
    netconf = s.recv_json()
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
