"""
Written by Dani Lykov @danlkv on 03/03/2019

An implementation of listening for events from a pull zmq socket
and pushing to a push socket

Can be used for workers in a pipeline
"""

from trio_tracer import Tracer
import trio
import zmq
import random
from logger_init import log
from itertools import count
PORT_IN = 5420
PORT_OUT = 5421
COUNTER = count()

class KeyVal():
    def __init__(self):
        self.data = {}
    def put(self,key,val):
        self.data[key] = val
    def get(self,key):
        return self.data.get(key)

class NodeDB(KeyVal):
    def __init__(self):
        super().__init__()
    def set_data(self, user_id, data):
        #log.debug('Set data for %d to %s'%(user_id,data))
        self.put(user_id,data)
    def get_data(self, user_id):
        data = self.get(user_id)
        if not data:
            log.warn("No data for user %i"%user_id)
            data = {}
        #log.debug('give data for %i as %s'%(user_id,data))
        return data

DB = NodeDB()

async def kernel_func(action, data = None):
    await trio.sleep(0)
    notif = 'done'
    def pure_map(data):
        """
        This function will be mapped on up to date data
        before sending a reply to server
        """
        if not data.get("called_cnt"):
            data['called_cnt'] = 0
        data['called_cnt'] +=1
        return notif, data
    return pure_map

async def node_fun(action, consumer):
    user_id = random.randint(0,30)
    user_data = DB.get_data(user_id)
    log.info('Calling kernel for uid %d with data %s \t and action %s'%(user_id,user_data,action))
    ####=====
    pure_map = await kernel_func(action, user_data)
    #-------- Wait here. Other connection can modify data!
    user_data = DB.get_data(user_id)
    notif, new_data = pure_map(user_data)
    ####=====
    log.info('kernel returned: notif %s, data: %s'%(str(notif), str(new_data)) )
    DB.set_data(user_id,new_data)
    log.info('Sending notif from uid %d with response to %s'%(user_id,action))
    consumer.send_json({'user_id':user_id,'notif':notif})

async def connection_handler(message,socket,connection_id):
    try:
        await node_fun(message, socket)
    except Exception as e:
        log.error("Task handler id:%d error %s"%(connection_id,str(e)))

async def server_listen_loop(source, drain):
    async with trio.open_nursery() as nursery:
        while True:
            status = source.poll(1)
            if status==1:
                msg = source.recv_json()
            else:
                await trio.sleep(0)
                continue
            log.debug('Got message: %s'%(str(msg)))
            conn_id = next(COUNTER)
            log.info('Starting handler task. id:%s'%conn_id)
            nursery.start_soon(connection_handler, msg, drain, conn_id)
            await trio.sleep(0)

def get_sockets():
    context = zmq.Context()
    # recieve work
    consumer = context.socket(zmq.PULL)
    consumer.connect("tcp://127.0.0.1:"+str(PORT_IN))
    # send work
    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://127.0.0.1:"+str(PORT_OUT))
    sender.send_json({"H":"H"})
    return consumer, sender

def main():
    """
    Start zmq sockets and init server_listen_loop
    """
    consumer,sender = get_sockets()

    log.info('Starting loop')
    # start looping and polling
    trio.run(server_listen_loop, consumer, sender)

if __name__=='__main__':
    main()

