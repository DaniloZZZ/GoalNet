import config

import tgflow as tgf
import sched,time

#from modules import login, student, apply
from UI import goals, notifs
from DataBase import db


tgf.configure(token=config.token,state='start')
def set_time_sec(sec):
    s = sched.scheduler(time.time, time.sleep)
    def sch(i):
        def send():
            print('sending',sec)
            tgf.send_state('notif',i.message.chat.id)
        s.enter(sec,1,send)
        print('starting',sec)
        s.run()
    return sch

UI ={
    'start':{
        't':'hello there!',
        'b':[
            {'call del':tgf.action(set_time_sec(10))}
        ]
    }
}
UI.update(goals.UI)
UI.update(notifs.UI)

tgf.start(UI)


