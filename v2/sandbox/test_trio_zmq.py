"""
Written by Dani Lykov @danlkv on 03/03/2019
"""

import unittest, time
import zmq
import trio_zmq as node
import trio
import multiprocessing as prc
def processed(f, args):
    try:
        len(args)
    except TypeError:
        args  = (args,)
    p = prc.Process(target=f,args = args)
    p.start()
    return p

def loader(socket):
    for i in range(300):
        msg = {"counter":i}
        print(">OUT>>", msg )
        socket.send_json(msg)
        time.sleep(0.001)

def start_loader(port):
    context = zmq.Context()
    emitter = context.socket(zmq.PUSH)
    addr = "tcp://127.0.0.1:"+str(port)
    print('binding emiter', addr)
    emitter.bind(addr)
    loader(emitter)

def printer(socket):
    while True:
        js = socket.recv_json()
        print("<<IN<<", js )

def start_reader(port):
    context = zmq.Context()
    consumer = context.socket(zmq.PULL)
    addr = "tcp://127.0.0.1:"+str(port)
    print('binding emiter', addr)
    consumer .bind(addr)
    printer(consumer)

class TestNode(unittest.TestCase):

    def test_ping_pong(self):
        processed(start_loader,node.PORT_IN)
        processed(start_reader,node.PORT_OUT)
        # start looping and polling
        node.main()
        


