"""
Created by Danil Lykov @danlkv on 14/02/19
"""
from collections import UserDict
class BaseNotif(UserDict):
    def __init__(self,uid):
        super().__init__()
        self.data['user_id']=uid

class PomodoroNotif(BaseNotif)
    def __init__(self,uid):
        super().__init__()
        self.data['type'] = 'pomodoro'

class WorkStart(BaseNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Time to work'

class RelaxStart(BaseNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Time to relax'

class WorkEnd(BaseNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'work ended'

class RelaxEnd(BaseNotif):
    def __init__(self, uid, **kwargs):
        super().__init__(uid)
        self.data['content'] = 'Relax ended'
