from StateMachine import States
from tgflow import handles as h
from DataBase import db
import requests,datetime,json

ps =h.post
a = h.action

notify_api='http://localhost:3200/'

def start_pomodoro(s,d):
    print("Starting pomodoro")
    r = requests.post(
        notify_api,
        data=json.dumps({
            'Goal':{
                "Title":'GoalStPomodoro'
            },
            'Record':{
                'Name':'Pomodoro_Start',
                'Content':{
                    'type':'pomodoro',
                    'secret':'SecRet'
                }
            }
        })
    )
    if r.status_code==200:
        return States.WORKING
    return s,d

UI={
    States.NOTIF:{
        't':h.st('Hey! Time to do %s','GoalName'),
        'b':[
            {'Start pomodoro':a(States.POMODORO)},
            {'Pick another goal':a(States.NOT_IMPLEMENTED)},
            {'Remind me in 5 min':a(States.NOT_IMPLEMENTED)},
        ]
    },
    States.POMODORO:{
        't':"WORKING:)",
        'b':[
            {'Stop':a(States.NOT_IMPLEMENTED)}
        ],
        'prepare':start_pomodoro
    }
}
