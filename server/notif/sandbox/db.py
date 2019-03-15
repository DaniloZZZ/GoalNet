import time
from Types import *

def get_goal(op):
    print("getting goal")
    # Do the call
    dic = {
        'name':"test goal",
        'thing':"jj",
        '_schedule_link':12
    }
    return Goal(dic)

def get_record(op):
    print("getting goal")
    # Do the call
    dic = {
        'type':"web",
        'content':"example.org",
        'time':time.time(),
        'clicks':2302,
        '_goal_link':212
    }
    return Goal(dic)

def get_goal_notif(op):
    print("getting goal->otif")
    # Do the call
    dic = {
        'when':"always",
        'goals_open':[12,13],
        'time':time.time(),
        'ret type':'telegram',
    }
    f = lambda x: Notification({'foo':'bar'}) if x.data.get('thing') else None
    return Goal_Notif(dic,func=f)
