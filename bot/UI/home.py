from StateMachine import States
import tgflow as tgf
from tgflow import handles as h
from DataBase import db
import notif
from multiprocessing import Process
import requests,json

ps =h.post
a = h.action
data_server_port = '3030'
endpoint = 'http://localhost'
default_usr_id = '5adcefbaed9d970d42d33d65'

user_goals_endpoint = endpoint+':'+data_server_port+'/user/goals'

home_kb= [
    {'Home':a(States.HOME)},
    {'Contact':a(States.CONTACT)}
]

def start_notifications_longpoll(i,s,**d):
    uid = d.get('_id') or i.from_user.id
    def clb(notif):
        print("**----\ngot notification",notif)
        event = notif['events'][0]
        data = event['data']
        # TODO: make a public method in tgf for this
        tgf.Data.get(uid,{}).update({
            'GoalName':data
        })
        tgf.send_state(States.NOTIF, uid)
    def func():
        return notif.start_longpoll(uid,clb)
    #p1 = Process(target=func)
    #p1.start()
    tgf.Data.get(uid,{}).update({
        '_id':uid
    })

    tgf.send_state(States.HOME, uid)
    notif.start_longpoll(uid,clb)
    return {'notif_started':True,'GoalName':'Notyet'}

def get_activities(i,s,**d):
    print("Getting user goals from ",user_goals_endpoint)
    usr_id = d.get('UserId') or default_usr_id
    r = requests.get(
        user_goals_endpoint,
        params= {
            'id':usr_id
        }
    )
    if r.status_code==200:
        print("Got goals for id ",usr_id)
        # data should be returned in format 
        # [{Name:str,Desc:str,..},..]
        print(r.text)
        goals = json.loads(r.text)
        goal_buttons = []
        print(tgf.Data)
        for goal in goals:
            def f(i,s,**d):
                return States.GOAL,{'GoalName':goal['title']}
            action = a(f,update_msg=False)
            goal_buttons.append(
                {goal['title']:action}
            )
        return  {'GoalButtons':goal_buttons}
    else:
        print("!!**!!\n ERROR",r.status_code)
        return States.ERROR

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
        'kb_txt':"Welcome!",
        'kb':h.obj(home_kb)
      },
    States.START:{
        't':'Start',
        'prepare':start_notifications_longpoll
    },
    States.ACTIVITY:{
        't':"Here are your Goals",
        'b':[
            ps(lambda s,**d: d.get('GoalButtons')),
            {}
        ],
        'prepare':get_activities
    },
    States.GOAL:{
        't':h.st("You are about to work on Goal %s",'GoalName'),
        'b':[
            {'Start pomodoro':a(States.POMODORO)}
        ]
        }
}

