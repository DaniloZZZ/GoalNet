import zmq
import json

import tgflow as tgf
from tgflow.api.cli import cliAPI
from enum import Enum

from network import ConnectorNetwork
from utils__ import  get_network_config

def _print(*args):
    print(">telegram bot>",*args)

class States(Enum):
    action=1
    settings=2


def bot(netconf):
    net = ConnectorNetwork(netconf,
            appid='0',
            name='telegram'
            )
    def handle_notif(notif):
        str_notif = json.dumps(notif)
        _print("got notif:",str_notif)
        tgf.send_raw(json.dumps(str_notif),0)
        return 'OK'

    net.listen_for_notif(handle_notif)

    def handle_action(i):
        text = i.text
        msg_type = 'telegram'
        try:
            msg_type, content = text.split('\\')
        except ValueError:
            content = text
        message = {
                'type':msg_type,
                'content':content,
                'user_id':'10',
                }
        net.send(message)
        return States.action

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
                }
            }

    tgf.configure(token="0",state=States.action,apiModel=cliAPI)
    tgf.start(UI)

def main():
    netconf = get_network_config()
    print("Starting bot")
    bot(netconf)

if __name__=="__main__":
    main()

