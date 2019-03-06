"""
Created by Danil Lykov @danlkv on 06/03/19
"""

from pprint import pprint
import multiprocessing as prc
from goalnet.helpers.log_init import log

from goalnet.utils import get_network_config
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

    async def node_fun(self,message,drain):
        log.info('message: %s'%message)
        action = message.get('action')
        if not action:
            return {"error":'No action field'}
        elif action=='get':
            return self.db.get_all()
        else:
            log.info("saving message to db %s"%message)
            self.db.put(message)
            return {'status':0,'db_len':self.db.len()}

def launch_logger(name,netconf):
    logm = LoggerModule(netconf,name=name)
    logm.start()

def main():
    log.info("Starting logger module node...")
    netconf = get_network_config()
    launch_logger('logger',netconf)

if __name__=='__main__':
    main()
