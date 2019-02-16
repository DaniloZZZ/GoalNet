"""
Created by Danil Lykov @danlkv on 14/02/19

A module for time-tracking technique

"""

import zmq, os, time
import json
from pprint import pprint

from utils__ import themify, dethemify, get_network_config
from BaseModule import Module
#---
import sched
from notif_sched import CallScheduler
import notif_types as notifs
from enum import Enum


class States(Enum):
    none=0
    work=1
    relax=2
    relax_end=3
    work_end=4

class PomodoroModule(Module):
    def __init__(self,netconf,name='pomodoro'):
        super().__init__(netconf,name=name)
        self.work_time = 4
        self.relax_time = 2
        self.states = {}
        self.sched = CallScheduler()
        self.sched.start()

    def get_state(self,uid):
        return self.states.get(uid)
    def set_state(self,uid,state):
        self.states[uid]=state

    ###--TODO: wrap this to PomodoroUsr(userid)
    # TODO: figure out the internal structure and make this 
    # mode beautiful
    def _start_work(self, user_id):
        self.set_state(user_id,States.work)
        self._send(
                 notifs.WorkStart(user_id).data
                )
        self.sched.enter(self.work_time, self._on_end_work, (user_id,))

    def _start_relax(self, user_id):
        self.set_state(user_id,States.relax)
        self._send(
                 notifs.RelaxStart(user_id).data
                )
        self.sched.enter(self.relax_time, self._on_end_relax, (user_id,))


    def _on_end_work(self,user_id):
        self.set_state(user_id,States.work_end)
        auto_continue = True
        ##
        self._send(
              notifs.WorkEnd(user_id).data
                )
        if auto_continue:
            self._start_relax(user_id)


    def _on_end_relax(self,user_id):
        self.set_state(user_id,States.relax_end)
        auto_continue = True
        ##
        self._send(
                 notifs.RelaxEnd(user_id).data
                )
        if auto_continue:
            self._start_work(user_id)
    ###--

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

        ###-- This can be more beautiful
        if action==States.work:
            self._start_work(user_id)
        if action==States.relax:
            self._start_relax(user_id)
        ###--


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
