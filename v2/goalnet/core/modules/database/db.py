"""
Created by Danil Lykov @danlkv on 06/03/19
"""

from pprint import pprint
import multiprocessing as prc

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

class DataBaseModule(AsyncModule):
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf,name='database'):
        super().__init__(netconf, name=name)
        self.db = ArrayDB()
        self.statdata = StatData()

    async def node_fun(self,message,drain):
        log.info('message: %s'%message)
        def response(notif):
            notif.update({'user_id':message['user_id']})
            return notif
        def handle_action(message, aciton, module, target):
            if module == 'test':
                if target=='record':
                    return self.statdata.record(message, action=action)
                if target=='metrics':
                    return self.statdata.metric(message, action=action)

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
