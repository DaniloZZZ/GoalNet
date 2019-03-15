import config
import requests
from datetime import datetime

class Longpoll():
    def __init__(self, upd_checker,
                 params_modifier=lambda x,u: x):
        """
        :param upd_checker:
            a function that returns if
            there was update
            :inp: dict
            :returns: Bool
        :param params_modifier:
            a function that maps previous params
            every time request done and provides
            info if there was updates
            :inp: (dict,bool)
            :returns: dict
        """
        self.func= upd_checker
        self.param_next= params_modifier

    def event_emmitter(self,addr,params={}):
        while True:
            print("**==>>\nMaking longpoll to ",addr,params)
            r = requests.get(addr,params)
            js = r.json()
            if r.status_code==200:
                if (self.func(js)):
                    yield js
                    self.param_next(params,True)
                else:
                    print('** no updates, listening more...')
                    self.param_next(params,False)
            else:
                raise Exception('longpoller error',
                                r.status_code,js,
                                'params:',params)

def was_update(json):
    if json.get('timeout'):
        return False
    else:
        return True

addr ="http://localhost:3100/events"
def start_longpoll(user_id,clb):
    poll = Longpoll(was_update,lambda x,u:x)
    AppId = 0
    for event in poll.event_emmitter(
        addr,
        params = {
            'timeout':'10',
            'category':'telegram:'+str(AppId)
        }):
        print("|**********\n New event:",event)
        clb(event)
        print("----------|\n Event processed, waiting for emitter")

