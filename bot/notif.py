import config
from datetime import datetime

def start_longpoll(user_id,clb):
    #TODO: implement longpoll to notif server
    print("NOT_IMPLEMENTED")
    notif={
        'type':'start',
        'target':'Dummy goal',
        'start':datetime.now(),
        'end':datetime.now(),
    }
    clb(notif)
