import json
from metrics import Metrics

class DB:
    def __init__(self):
        self.users_file= 'vk_users.json'
        self.online_file = 'online_data.json'
        self.users = _try_read_json(self.users_file,{})
        self.online = _try_read_json(self.online_file,{})

    def new_user(self,uid, vkauth):
        self.users[uid] = vkauth
        _write_json(self.users_file, self.users)

    def get_vkauth(self, uid):
        return self.users.get(uid)

    def get_users_tokens(self):
        return self.users.items()

    def update_metrics(self):
        self.online = _try_read_json(self.online_file,{})

    def get_online_metrics(self,uid):
        m = []
        for item in self.online[uid]:
            m.append((1,item['start']))
            if item.get('end'):
                m.append((0,item['end']))
        return Metrics(m)

def _try_read_json(fname,default = None):
    with open(fname,'r') as f:
        try:
            return json.load(f)
        except Exception as e:

            print("Exception while reading %s file!"%fname,e)
            return default
def _write_json(fname,js):
    with open(fname,'w+') as f:
        json.dump(js,f)

