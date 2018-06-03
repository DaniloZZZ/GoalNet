from StateMachine import States
import tgflow as tgf
from tgflow import handles as h
from DataBase import db
import notif

ps =h.post
a = h.action

home_kb= [
    {'Home':a(States.HOME)},
    {'Contact':a(States.CONTACT)}
]

def start_notifications_longpoll(i,s,**d):
    uid = d.get('_id') or i.from_user.id
    def clb(notif):
        tgf.send_state(States.NOTIF, uid)
    notif.start_longpoll(uid,clb)
    return {'notif_started':True}

def get_activities(i,s,**d):
    # TODO: use api to get all user's scheduled activities
    print("NOT_IMPLEMENTED")
    acts = [{
        'name':'Your dummy act',
        '_id':'1qw21e13d12'
            }]
    d['activs']=acts
    return d

UI={
    States.HOME:{
        't':'Welcome, buddy. Wanna stay super-productive?',
        'b':[
            {'Start activity':a(States.ACTIVITY,update_msg=False)},
            {'View Stats':a(States.NOT_IMPLEMENTED)},
            {'Add new goal':a(States.NOT_IMPLEMENTED)},
            ],
        'prepare':start_notifications_longpoll,
        'kb_txt':"Welcome!",
        'kb':h.obj(home_kb)
      },
    States.ACTIVITY:{
        't':"Choose what to do:",
        'b':[
            # TODO: fetch activs and pass buttons here
            {}
        ]
    }
}

