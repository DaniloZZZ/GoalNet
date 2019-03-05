"""
Created by Danil Lykov @danlkv on 13/02/19
"""

from pprint import pprint
import multiprocessing as prc
from goalnet.helpers.log_init import log

from goalnet.utils import get_network_config
from .AsyncBaseModule import AsyncModule

class LoggerModule(AsyncModule):
    """
    A simple module that logs everything and does nothing afterwards
    """
    def __init__(self, netconf,name='logger'):
        super().__init__(netconf, name=name)

    async def node_fun(self,message,drain):
        log.info('message: %s'%message)
        return message

def launch_logger(name,netconf):
    logm = LoggerModule(netconf,name=name)
    logm.start()

def main():
    log.info("Starting logger module node...")
    netconf = get_network_config()
    launch_logger('logger',netconf)

if __name__=='__main__':
    main()
