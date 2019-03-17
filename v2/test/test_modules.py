"""
Test modules for starting

"""
import sys,time
import numpy as np

import unittest
import zmq
import goalnet as g
from goalnet.helpers.log_init import log
from pprint import pprint
from goalnet.utils import get_network_config
from goalnet.connectors import NetworkAPI

def get_source_socket(addr):
    ctx = zmq.Context()
    s = ctx.socket(zmq.REP)
    s.bind(addr)
    return s

def get_mux_socket(addr):
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUSH)
    s.connect(addr)
    return s

class TestModules(unittest.TestCase):
    def setUp(self):
        self.conf_process = process = g.start_cnf()
        time.sleep(0.01)
        self.mux_p = g.start_mux(parallel=True)
        self.dmx_p = g.start_dmx(connectors=['console'], parallel=True)

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

    def test_db_metrics(self):
        # start db module
        db_process = g.start_module('database')
        time.sleep(0.01)
        # configure connection to dmx
        netconf = get_network_config()
        netapi = NetworkAPI(netconf,'id1', 'console')
        def send_recv_print(msg):
            log.info(">>OUT>>")
            msg.update({'user_id':1, 'appid':1,})
            netapi.send(msg)
            doc = netapi.recv()
            netapi.reply_notif("OK")
            log.info("<<IN<< %s"%doc)
            return doc

        metrics_name = 'integral'
        record_name = 'zoo'
        def record_gen(name):
            i = 0
            while True:
                i+=1
                yield {
                    'action':'put.test.record',
                    'name':name,
                    'value':i,
                    'time':i,
                }
        def record_gen_str(name):
            i = 0
            animals = ('zebra','panda','grizly','cow')
            cnt = len(animals)

            while True:
                i+=1
                yield {
                    'action':'put.test.record',
                    'name':name,
                    'value':animals[ np.random.randint(cnt) ],
                    'time':i,
                }
        gen = record_gen_str(record_name)
        # create a new record accumulator
        send_recv_print({'action':'add.test.record','name':record_name})

        for i in range(10):
            record = next(gen)
            send_recv_print(record)
        # get some metrics
        send_recv_print({
            'action':'get.test.metrics',
            'provider':record_name,
            'name':metrics_name,
            'start':0,
            'end':6,
            'step':2,
        }
        )

    @unittest.skip
    def test_db_module(self):
        # start db module
        db_process = g.start_module('database')
        # configure connection to dmx
        netconf = get_network_config()
        netapi = NetworkAPI(netconf,'id1', 'console')

        for i in range(10):
            log.info(">>OUT>>")

            netapi.send({"app_id":1,"user_id":1,"action":"put",'data':{'foo':i}})
            doc = netapi.recv()
            netapi.reply_notif("OK")

            log.info("<<IN<< %s"%doc)

        netapi.send({"app_id":1,"user_id":1,"action":"get"})

        doc = netapi.recv()
        netapi.reply_notif("OK")

        log.info("<<IN<< %s"%doc)

        print("Terminating logging process")
        db_process.terminate()
        db_process.join()

    @unittest.skip
    def test_logging_module(self):
        log_process = g.start_module('logger')
        netconf = get_network_config()
        mux_addr = netconf.get_address("MUX_in")
        listen_addr = netconf.get_address("console")
        emitter = get_mux_socket(mux_addr)
        consumer = get_source_socket(listen_addr)
        time.sleep(0.01)
        tms = []
        for i in range(1000):
            st = time.time()
            log.info(">>OUT>>")
            emitter.send_json({"app_id":1,"user_id":1,"hello":"world"})
            doc = consumer.recv_json()
            consumer.send_string("OK")
            log.info("<<IN<<", doc)
            tms.append(time.time()-st)


        tms = np.array(tms)
        print("|\n|\n|",tms.round(5))
        print("|\n|\n|",np.mean(tms))

        time.sleep(0.01)
        print("Terminating logging process")
        log_process.terminate()
        log_process.join()


if __name__=="__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test'))



