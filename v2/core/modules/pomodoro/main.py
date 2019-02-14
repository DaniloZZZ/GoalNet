"""
Created by Danil Lykov @danlkv on 14/02/19

A module for time-tracking technique

"""

import zmq, os, time
import json
from pprint import pprint
import multiprocessing.dummy as thread

from utils__ import themify, dethemify, get_network_config
from BaseModule import Module
from enum import Enum

class States(Enum):
    none=0
    work=1
    relax=2
    relax_end=3
    work_end=4

def threadify(f,args=()):
    p = thread.Process(target=f,args=args)
    p.start()

class NotifScheduler:
    def __init__(self,callback):
        self.queue = []
        self.callback = callback

    def _collect_due(self,intents=[]):
        t = time.time()

        intents = [ i for i in self.queue if i[0]<t]
        self.queue = [ i for i in self.queue
                if i not in intents]
        return intents

    def schedule(self, notif, time):
        self.queue.append((time,notif))
        print("queue",self.queue)

    def run(self):
        ts = time.time()
        while True:
            intents = self._collect_due()
            if intents:
                print("intents to resolve",intents)
                for intent in intents:
                    self.callback(intent[1])
            time.sleep(0.1)

    def start(self):
        print("NotifScheduler running...")
        threadify(self.run)

class PomodoroModule(Module):
    def __init__(self,netconf,name='pomodoro'):
        super().__init__(netconf,name=name)
        self.work_time = 4
        self.relax_time = 2
        self.states = {}
        self.sched = NotifScheduler(self.resolve_notif)
        self.sched.start()

    def get_state(self,uid):
        return self.states.get(uid)
    def set_state(self,uid,state):
        self.states[uid]=state

    def handle_action(self,action):
        user_id = action['user_id']
        action = self._parse_action(action)
        if not action:
            self._print("No action parsed")
            return
        state = self.get_state(user_id)
        if state == action:
            self._print("requested state is equal to current")
            return
        if action==States.work:
            self.set_state(user_id,States.work)
            notif = {
                    'content':'Time to relax',
                    'type':'pomodoro',
                    'user_id':user_id,
                    }
            self.delayed_send(notif,self.work_time)
        if action==States.relax:
            self.set_state(user_id,States.relax)
            notif = {
                    'content':'Time to work',
                    'type':'pomodoro',
                    'user_id':user_id,
                    }
            self.delayed_send(notif,self.relax_time)


    def resolve_notif(self,notif):
        self._print("sending notif")
        self._send(notif)

    def delayed_send(self,notif,delay):
        resolve_at = time.time() +  delay
        self.sched.schedule(notif, resolve_at)

    def _parse_action(self, action):
        act = action['content']
        if act=='work':
            return States.work
        if act=='relax':
            return States.relax
        if act=='work_end':
            return States.work_end
        if act=='relax_end':
            return States.relax_end
        if act=='none':
            return States.none

def main():
    print("Starting pomodoro module node...")
    netconf = get_network_config()
    pom = PomodoroModule(netconf,'pomodoro')
    pom.start()

if __name__=="__main__":
    main()
