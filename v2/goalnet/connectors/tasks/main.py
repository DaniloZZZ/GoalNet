import zmq, json, time
import multiprocessing.dummy as thread

from intra import ConnectorNetwork
from utils__ import  get_network_config
from db import DB
from flask_app  import start_app
from core.modules.vk_sleep import VkSleepModule

FLASK_PORT = 8991
import logging
logging.basicConfig(level=logging.DEBUG)


db = None
vksleep = None
net = None

def _print(*args):
    print(">tasks>",*args)

def start(netconf):
    global net
    net = ConnectorNetwork(netconf,
            appid='0',
            name='tasks'
            )
    global db
    db = DB()
    start_app(db)

def main():
    netconf = get_network_config()
    print("Starting tasks connector")
    global vksleep
    start(netconf)

if __name__=="__main__":
    main()

