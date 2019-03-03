"""
Created by Danil Lykov on 02/03/2019

A connector for self-looping events

"""
import zmq
import json
#
from intra import ConnectorNetwork
#
def _print(*args):
    print(">tasks>",*args)
