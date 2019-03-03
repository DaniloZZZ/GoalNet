"""
Test modules for starting

"""
import sys,time

import unittest
import goalnet as g
from pprint import pprint

class TestStart(unittest.TestCase):
    def setUp(self):
        self.conf_process = process = g.start_cnf()
        time.sleep(0.01)
        #netconf = g.get_network_config()
        #print("Got netconf:")
        #pprint(netconf)
    def tearDown(self):
        #print("Terminating conf server process")
        self.conf_process.terminate()
        self.conf_process.join()

    def test_start_MUX(self):
        process = g.start_mux(parallel=True)
        time.sleep(0.1)
        print("Terminating MUX process")
        process.terminate()
        process.join()

    def test_logging_module(self):
        module = g.start_module('logger')
        print("Terminating logging process")
        time.sleep(0.1)
        module.process.terminate()
        module.process.join()


if __name__=="__main__":
    unittest.main()
