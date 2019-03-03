import zmq
import json

import tgflow as tgf
from tgflow.api.cli import cliAPI
from enum import Enum

from network import ConnectorNetwork
from utils__ import  get_network_config
from database import DB

def _print(*args):
    print(">telegram bot>",*args)

class States(Enum):
    action=1
    settings=2
    login=3
    start=4

def bot(netconf):
    net = ConnectorNetwork(netconf,
            appid='0',
            name='telegram'
            )
    db = DB()

    def handle_notif(notif):
        str_notif = json.dumps(notif)
        try:
            user_id = str(notif['user_id'])
            tgid = db.get_tg_id(user_id)
        except Exception as e:
            _print("Notif was not sent",e)
            return "FAIL"
        _print("got notif:",str_notif)
        message = "Got new notif of type %s. Content: %s"%(
                notif.get('type'),notif.get('content')
                )
        if not tgid:
            print("User id %s has no telegram log"%user_id)
            return "FAIL"
        try:
            tgf.send_raw(message, tgid)
        except Exception as e:
            _print("Notif was not sent",e)
            return "FAIL"
        return 'OK'

    net.listen_for_notif(handle_notif)

    def login_uid_1(i):
        telegram_id = i.message.chat.id
        user_id = '1'
        db.save_tg_id(user_id,telegram_id)

        return States.action, {'user_id': user_id}

    def handle_action(i,user_id=None):
        _print('inp',i)
        if not user_id:
            _print('user not logged in')
            return States.login
        text = i.text
        msg_type = 'telegram'
        try:
            msg_type, content = text.split('\\')
        except ValueError:
            content = text
        message = {
                'type':msg_type,
                'content':content,
                'user_id':user_id,
                }
        net.send(message)
        # stay silent
        return -1

    UI =  {
            States.action:{
                't':'Enter an action type and content to send',
                'b':[
                    {"Settings":tgf.action(States.settings)}
                    ],
                'react':tgf.action(handle_action,react_to='text')
                },
            States.settings:{
                't':'Settings',
                'b':[
                    {"Action":tgf.action(States.action)}
                    ],
                },
            States.start:{
                't':'Welcome!',
                'b':[
                    {"Log in":tgf.action(States.login)},
                    ]
                },
            States.login:{
                't':'Please log in',
                'b':[
                    {"Log in as 1":
                        tgf.action(login_uid_1)}
                    ],
                }
            }
    key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

    tgf.configure(token=key,
            state=States.start,
            #apiModel=cliAPI,
            verbose=True,
            )
    tgf.start(UI)

def main():
    netconf = get_network_config()
    print("Starting bot")
    bot(netconf)

if __name__=="__main__":
    main()

