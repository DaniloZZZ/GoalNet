from StateMachine import States
from tgflow import handles as h
from DataBase import db
import requests,datetime,json
import inspect

ps =h.post
a = h.action

notify_api='http://localhost:3200/'

def start_pomodoro(s,d):
    print("Starting pomodoro")
    r = requests.post(
        notify_api,
        data=json.dumps({
            'Goal':{
                "Title":d.get('GoalName','GoalStPomodoro')
            },
            'Record':{
                'Command':'Pomodoro_Start',
                'Type': "pomodoro",
                'Content':{
                    'secret':'SecRet'
                }
            }
        })
    )
    if r.status_code==200:
        return States.POMODORO
    else:
        return States.ERROR

def stop_pomodoro(s,d):
    print("Stopping pomodoro")
    r = requests.post(
        notify_api,
        data=json.dumps({
            'Goal':{
                "Title":d.get('GoalName','GoalStPomodoro')
            },
            'Record':{
                'Command':'Pomodoro_Stop',
                'Type': "pomodoro",
                'Content':{
                    'type':'pomodoro',
                    'secret':'End this shit'
                }
            }
        })
    )
    if r.status_code==200:
        return States.ACTIVITY
    else:
        return States.ERROR
def parse_notif(i,s,**d):
    notif = d.get('NotifData',{})
    print(notif)
    t = notif['Type']
    text = 'Some other notif'
    if t=='Pomodoro_Start':
        text = 'Hey! time to do %s'%notif.get('GoalName')
    elif t=='Pomodoro_Relax':
        text = 'Hey! take an effective rest'

    d.update({'NotifText':text})
    return d

UI={
    States.NOTIF:{
        't':ps(lambda s,**d: d.get('NotifText')),
        'b':[
            {'Start pomodoro':a(start_pomodoro)},
            {'Pick another goal':a(States.ACTIVITY,update_msg=False)},
            {'Remind me in 5 min':a(States.NOT_IMPLEMENTED)},
        ],
        'prepare':parse_notif
    },
    States.POMODORO:{
        't':h.st("WORKING on %s :)",'GoalName'),
        'b':[
            {'Stop':a(stop_pomodoro,update_msg=False)}
        ],
    }
}
print(inspect.getargspec(start_pomodoro))
