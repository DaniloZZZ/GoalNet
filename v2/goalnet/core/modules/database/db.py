"""
Created by Danil Lykov @danlkv on 06/03/19
"""

from pprint import pprint
import multiprocessing as prc
import time, random

from goalnet.helpers.log_init import log

from goalnet.utils import get_network_config, get_action_path
from goalnet.helpers import StatData
from ..AsyncBaseModule import AsyncModule

class ArrayDB:
    def __init__(self):
        self.data =[]
    def put(self,item):
        self.data.append(item)
    def get_all(self):
        return self.data
    def len(self):
        return len(self.data)

def gen_user_id():
    return time.time().as_integer_ratio()[1]
def gen_token():
    t = time.time().as_integer_ratio()[0]*random.randint(0,1000)
    return hex(t)

class DataBaseModule(AsyncModule):
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf,name='database'):
        super().__init__(netconf, name=name)
        self.db = ArrayDB()
        self.auth = {}
        self.statdata = StatData()

    def register_user(self, user_id, pwd_hash, email):
        #TODO: what if user_id exists?
        # can an attacker overwrite credentials?
        existing_ = self.auth.get(user_id)
        if existing_:
            if pwd_hash!=existing_:
                return None
            else:
                return gen_token()
        else:
            self.auth[user_id] = {'pwd_hash':pwd_hash,'email':email}
            return gen_token()

    async def node_fun(self,message,drain):
        log.info('message: %s'%message)
        def response(notif):
            user_id = message.get('user_id')
            if user_id:
                notif.update(
                    {
                        'user_id':user_id
                    }
                )
            return notif
        def handle_action(message, aciton, module, target):
            if module == 'test':
                if target=='record':
                    return self.statdata.record(message, action=action)
                if target=='metrics':
                    return self.statdata.metric(message, action=action)
            if module=='user':
                if target=='auth':
                    if action=='add':
                        user_id = message.get('user_id')
                        # get user identity
                        try:
                            pwd_hash = message['pwd_hash']
                            email = message['email']
                        except KeyError as e:
                            errmsg = 'no record found with name %s'%e
                            log.error(errmsg)
                            return {"error":errmsg}
                        log.info('new user id %s emaii %s'%(user_id, email))
                        # Issue an auth token
                        token = self.register_user(user_id, pwd_hash, email)
                        if not user_id:
                            user_id = gen_user_id()
                        if not token:
                            return {"error":'auth error'}
                        # return an action field to so the webserver knows to rememner
                        return {"user_id":user_id,"token":"%s"%token,'action':message['action']}

            if action=='get':
                return self.db.get_all()
            else:
                log.info("saving message to db %s"%message)
                self.db.put(message)
                return response({'status':0,'db_len':self.db.len()})
        ## Parse action 
        action_path = get_action_path(message)
        if action_path:
            action = action_path[0]
            module = action_path[1]
            target = action_path[2]
            resp = handle_action(message,action,module,target)
            return response(resp)

        return response({"error":'No action field'})

def launch_logger(name,netconf):
    logm = LoggerModule(netconf,name=name)
    logm.start()

def main():
    log.info("Starting logger module node...")
    netconf = get_network_config()
    launch_logger('logger',netconf)

if __name__=='__main__':
    main()
