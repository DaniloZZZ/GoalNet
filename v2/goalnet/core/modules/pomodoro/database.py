"""
Created by Danil Lykov @danlkv on 16/02/19

An abstraction for pomodoro-needed data
"""
from userdict import UserDict

class PomodoroRecord(UserDict):
    def __init__(self, data):
        super().__init__()
        self.data=data
        self.__dict__=sef.data

class PomodoroDB:
    def __init__(self, conn_params=None):
        print("connection to dbpomodoro done")
        self.reclist = []
        #self.user_cnt_list = 

    def add_pomodoro(self, record):
        print("added pomodoro record",record)
        self.reclist.append(record)
        print('reclist now',self.reclist)

    def get_pomodoro_by_uid(self,uid):
        return [r for r in self.reclist if r['user_id']==uid]

