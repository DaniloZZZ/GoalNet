import json, time
from metrics import Metrics

class DB:
    def __init__(self):
        self.goals_file= 'goals.json'
        self.goals= _try_read_json(self.goals_file,{})

    def new_task(self,uid, task):
        if not self.goals.get(uid):
            self.goals[uid] = []
        self.goals[uid] += [task]
        _write_json(self.goals_file, self.goals)

    def get_tasks(self,uid):
        return self.goals.get(uid)
    def get_task_metrics(self,uid):
        tasks = self.goals[uid]
        m = []
        for task  in tasks:
            m.append((task['name'],task['start']))
            m.append(('none',task['end']))
        metr = Metrics(m)


def _write_json(fname,js):
    with open(fname,'w+') as f:
        json.dump(js,f)

def _try_read_json(fname,default = None):
    with open(fname,'r') as f:
        try:
            return json.load(f)
        except Exception as e:

            print("Exception while reading %s file!"%fname,e)
            return default


