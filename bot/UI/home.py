
from threading import Thread
import requests,json
import tgflow as tgf


from StateMachine import States
from tgflow import handles as h
from DataBase import db
import notif
from .notifs import start_pomodoro

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
    uid = 0
    try:
        uid = d.get('_id') or i.from_user.id
    except Exception as e:
        print(e)
    def clb(notif):
        print("<<==\nGot notification:",notif)
        event = notif['events'][0]
        data =event['data']
        # TODO: make a public method in tgf for this
        tgf.Data.get(uid,{}).update({
            'NotifData':data
        })
        t = data['Type']
        notifState = get_notif_state(t)
        tgf.send_state(notifState, uid)
    def func():
        return notif.start_longpoll(uid,clb)
    t = Thread(target=func)
    print('\n**\n**\n**\nstarted Thread')
    t.start()
    print('after start')
    tgf.Data.get(uid,{}).update({
        '_id':uid
    })

    tgf.send_state(States.HOME, uid)
    return {'notif_started':True,'GoalName':'Notyet'}

def get_notif_state(notifType):
    parentType = notifType.split('_')[0]
    d = {
        States.NOTIF_POMO:['Pomodoro_Start','Pomodoro_Relax'],
    }
    s = States.NOTIF
    for state,types in d.items():
        if notifType in types:
            s = state
    return s
    # Code below is deprecated. ts:16/09/18
    if parentType=='Pomodoro':
        return States.POMODORO
    else:
        return States.NOTIF

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
        def handler_gen(goal):
            return lambda: (
                States.GOAL,
                {'ActiveGoal':goal, 'GoalName':goal['title']})
        goal_buttons = [
            {g['title']:a(handler_gen(g))} for g in goals]
        return {'GoalButtons':goal_buttons}
    else:
        print("!!**!!\n ERROR While getting Goals",r.status_code)
        return {}

UI={
    States.HOME:{
        't':'Welcome, buddy. Wanna stay super-productive?',
        'b':[
            {'Start activity':a(States.ACTIVITY,update_msg=False)},
            {'View Stats':a(States.NOT_IMPLEMENTED)},
            {'Add new goal':a(States.NOT_IMPLEMENTED)},
            ],
        #'kb_txt':"Welcome!",
        #'kb':h.obj(home_kb)
      },
    States.START:{
        't':'Notification polling started',
        'b':[
            { 'to home':tgf.action(States.HOME)}
        ],
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
            {'Start pomodoro':a(start_pomodoro)}
        ]
        }
}
 
