"""
Created by Danil Lykov @danlkv on 14/02/19
"""
#from collections import UserDict #not json serializable
import json
from userdict import UserDict
class BaseNotif(UserDict):
    def __init__(self,uid):
        super().__init__()
        self.data['user_id']=uid

class PomodoroNotif(BaseNotif):
    def __init__(self,uid):
        super().__init__(uid)
        self.data['type'] = 'pomodoro'

class WorkStart(PomodoroNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Time to work'
        self.data['type'] += '.work'

class RelaxStart(PomodoroNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Time to relax'
        self.data['type'] += '.relax'

class WorkEnd(PomodoroNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'work ended'
        self.data['type'] += '.work_end'

class RelaxEnd(PomodoroNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Relax ended'
        self.data['type'] += '.relax_end'
