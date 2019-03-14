import unittest
import multiprocessing as proc
import logging, time, json

import trio
from trio_websocket import open_websocket_url

from goalnet.connectors import start_websocket
import goalnet as g

def processed(f, *args,name=None):
    process = proc.Process(target=f, args=args, name=name)
    process.start()
    return process

async def make_request(url,message):
    try:
        async with open_websocket_url(url) as ws:
            await ws.send_message(message)
            message = await ws.get_message()
            logging.info('Received message: %s', message)
            return message
    except OSError as ose:
        logging.error('Connection attempt failed: %s', ose)

class TestWebsocket(unittest.TestCase):
    def setUp(self):
        self.conf_process = process = g.start_cnf()
        time.sleep(0.01)
        self.mux_p = g.start_mux(parallel=True)
        self.dmx_p = g.start_dmx(connectors=['websocket'], parallel=True)
        self.log_p = g.start_module('logger')

    def test_start(self):
        proc = processed(start_websocket, name='ws-connector')
        url = 'ws://127.0.0.1:3032'
        time.sleep(0.1)
        message_out = {'action':'world'}
        message = trio.run(make_request, url, json.dumps(message_out))
        notif = json.loads(message)
        assert notif['action']==message_out['action']
        print(message)
        #proc.terminate()
        proc.join()

    def tearDown(self):
        #print("Terminating conf server process")
        self.conf_process.terminate()
        self.conf_process.join()
        print("Terminating MUX process")
        self.mux_p.terminate()
        self.mux_p.join()
        print("Terminating DMX process")
        self.dmx_p.terminate()
        self.dmx_p.join()
        print("Terminating Logger process")
        self.log_p.terminate()
        self.log_p.join()
 
if __name__=='__main__':
    unittest.main()
