import zmq, json, time
import multiprocessing.dummy as thread

import vk_api

from intra import ConnectorNetwork
from utils__ import  get_network_config
from db import DB
from flask_app  import start_app
from core.modules.vk_sleep import VkSleepModule

FLASK_PORT = 8990
import logging
logging.basicConfig(level=logging.DEBUG)


db = None
vksleep = None
net = None
def vk_session(token):
    vk_session = vk_api.VkApi(
            app_id=6873513,
            token=token
            )
    vk = vk_session.get_api()
    return vk

def _print(*args):
    print(">vk sleep>",*args)

def handle_info(uid,info):
    event = {
            'user_id':uid,
            'topic':'vksleep'
            }
    event.update(info)
    #net.send(event)
    vksleep.handle_action(event)

def poll_events(db):
    print("Startin poll for events")
    while True:
        for uid, token in db.get_users_tokens():
            print("Uid:",uid)
            sess = vk_session(token)

            info = sess.users.get(fields='online')
            handle_info(uid,info[0])
            print("info:",info)
        time.sleep(1.5)

def vkSleep(netconf):
    global net
    net = ConnectorNetwork(netconf,
            appid='0',
            name='vk'
            )
    global db
    db = DB()
    p = thread.Process(target=poll_events,args=(db,))
    p.start()
    start_app(db)
    p.join()

def main():
    netconf = get_network_config()
    print("Starting vk connector")
    global vksleep
    vksleep = VkSleepModule(netconf)
    vkSleep(netconf)

if __name__=="__main__":
    main()

