"""
Created by Danil Lykov @danlkv on 13/02/19
"""

import zmq, os, time
import json
from pprint import pprint
import multiprocessing as prc

from ..utils import themify, dethemify, get_network_config
from goalnet.core.modules.BaseModule import Module


class EchoModule(Module):
    """
    A simple module that passes everything unchanged as notification
    """
    def __init__(self, netconf, name='echo'):
        super().__init__(netconf, name=name)

    def handle_action(self,action):
        self._print("got action")
        return action

def launch_echo(name,netconf):
    echom = EchoModule(netconf,name=name)
    echom.run_function()

def main():
    print("Starting echo module node...")
    netconf = get_network_config()
    launch_echo('echo',netconf)

if __name__=='__main__':
    main()
