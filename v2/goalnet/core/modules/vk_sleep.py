from core.modules.BaseModule import Module
from enum import Enum
from ..utils import get_network_config
import time, json
class States(Enum):
    ONLINE=1
    OFFLINE=0
class VkSleepModule(Module):
    """
    """
    def __init__(self, netconf, name='vksleep'):

        super().__init__(netconf, name=name)
        self.data_path = 'online_data.json'
        with open(self.data_path,'r') as f:
            try:
                db = json.load(f)
            except Exception as e:
                print("Exception while reading vk data file!",e)
                db = None
        if db:
            self.user_data = db
        else:
            self.user_data = {}
        self.user_states = {}

    def get_state(self,uid):
        return self.user_states.get(uid)
    def set_state(self,uid,state):
        self.user_states[uid] = state
    def get_data(self,uid):
        return self.user_data.get(uid)
    def set_data(self,uid, datum):
        self.user_data[uid] = datum
        self._write_data()
    def append_data(self,uid, datum):
        if not self.user_data.get(uid):
            self.user_data[uid] = []
        self.user_data[uid] += [datum]
        self._write_data()
    def _write_data(self):
        self._print("WRITING DATA to",self.data_path)
        with open(self.data_path,'w+') as f:
            json.dump(self.user_data,f)


    def set_online(self,uid):
        state = self.get_state(uid)
        if not state==States.ONLINE:
            self.set_state(uid,States.ONLINE)
            return self.become_online(uid)
    def set_offline(self,uid):
        state = self.get_state(uid)
        if not state==States.OFFLINE:
            self.set_state(uid,States.OFFLINE)
            return self.become_offline(uid)

    def become_online(self,uid):
        self._print("becoming o nline")
        self.append_data(uid,{'start':time.time()})
        return {'user_id':uid,'status':'online'}

    def become_offline(self,uid):
        if not self.user_data.get(uid):
            self.user_data[uid]=[]
            return {'user_id':uid,'status':'offline'}
        ret = self.get_data(uid)[-1]
        ret.update({'end':time.time()})
        ret.update({'user_id':uid,'status':'offline'})
        self._write_data()
        return ret

    def handle_action(self,action):
        self._print("got action",action)
        uid = action['user_id']
        if not 'online' in action.keys():
            self._print('invalid action:',action)
            return
        if action['online']==1:
            notif = self.set_online(uid)
        else:
            notif = self.set_offline(uid)
        if notif:
            notif.update({'type' : 'vk' })
            notif.update({'content':'vk status:'+notif['status']})
            return notif

def launch_module(name,netconf):
    vksleep = VkSleepModule(netconf,name=name)
    vksleep.run_function()

def main():
    print("Starting vksleep module node...")
    netconf = get_network_config()
    launch_module('vksleep',netconf)

if __name__=='__main__':
    main()
