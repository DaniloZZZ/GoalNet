"""
Created by Danil Lykov @danlkv on 06/03/19
"""

from pprint import pprint
import multiprocessing as prc
import time, random
import jwt

from goalnet.helpers.log_init import log

from goalnet.utils import get_network_config, get_action_path
from goalnet.helpers import StatData
from goalnet.core.database.api import with_db_api
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
def gen_token(user_id):
    t = jwt.encode({'user_id':user_id},'secret',algorithm='HS256')
    return t.decode()

@with_db_api
class DataBaseModule(AsyncModule):
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf, name='database_mod'):
        super().__init__(netconf, name=name)
        self.db = ArrayDB()
        self.auth = {}
        self.statdata = StatData()


    def register_user(self, pwd_hash, email):
        #TODO: what if user_id exists?
        # can an attacker overwrite credentials?
        existing_ = self.db_call({
            'request':'get.user',
            'email':email
        })
        if existing_:
            user_id = existing_['user_id']
            log.debug("User exists with id %s"%user_id)
            if pwd_hash!=existing_['pwd_hash']:
                return user_id, None
            else:
                return user_id, gen_token(user_id)
        else:
            user_id = gen_user_id()
            token =gen_token(user_id)
            self.db_call({
                'request':'new.user',
                'email':email,
                'user_id':user_id,
                'pwd_hash':pwd_hash,
                'token':token
            })
            return user_id, token

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
            if module == 'test' or module=='webext':
                if target=='record':
                    res =  self.statdata.record(message, action=action)
                    res.update({"action":module+".record"})
                if target=='metrics':
                    res = self.statdata.metric(message, action=action)
                    res.update({"action":module+".metrics"})
                return  res
            if module=='user':
                if target=='auth':
                    if action=='add':
                        # get user identity
                        try:
                            pwd_hash = message['pwd_hash']
                            email = message['email']
                        except KeyError as e:
                            errmsg = 'no record found with name %s'%e
                            log.error(errmsg)
                            return {"error":errmsg}
                        log.info('new emaii %s'%( email))
                        # Issue an auth token
                        user_id, token = self.register_user( pwd_hash, email)
                        if not token:
                            return {"error":'auth error'}
                        # generate a user id if no id provided
                        # return an action field to so the webserver knows to rememner
                        return {"user_id":user_id,"token":"%s"%token,'action':message['action']}
                if target=='module':
                    if aciton=='add':
                        user_id=message['user_id']
                        name=message['name']
                        self.add_module(user_id,name)
                        modls = self.get_modules(user_id)
                        return {"modules":modls,'action':'user.modules'}
                    if aciton=='get':
                        user_id=message['user_id']
                        modls = self.get_modules(user_id)
                        return {"modules":modls,'action':'user.modules'}

            if action=='get':
                return self.db.get_all()
            else:
                log.info("saving message to db %s"%message)
                self.db.put(message)
                return response({'status':0,'db_len':self.db.len()})
        ## Parse action 
        action_path = get_action_path(message)
        if len(action_path)!=3:
            return response({'error':'action path is invalid'})
        if action_path:
            action = action_path[0]
            module = action_path[1]
            target = action_path[2]
            resp = handle_action(message,action,module,target)
            log.debug('responding %s'%resp)
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
