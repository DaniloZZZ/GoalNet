import unittest, time

import goalnet as g

from goalnet.connectors import NetworkAPI

class TestDatabaseNode(unittest.TestCase):
    def setUp(self):
        ps = []
        ps.append( g.start_cnf() )
        ps.append( g.start_mux() )
        ps.append( g.start_dmx(connectors=['console']) )
        ps.append( g.start_module('database') )
        time.sleep(0.15)
        netconf = g.get_network_config()
        self.netapi = NetworkAPI(netconf, 'test_db_runner','console')

    def test_save_get(self):
        db = g.start_database()
        time.sleep(0.1)
        self.netapi.send({
            'action':'add.user.auth',
            'email':'test@goalnet',
            'pwd_hash':'oxo',
            
        })
        doc = self.netapi.recv()
        self.netapi.reply_notif("OK")
        print("With valid creds",doc)

        self.netapi.send({
            'action':'add.user.auth',
            'email':'test@goalnet',
            'pwd_hash':'oxo12',
            
        })
        doc = self.netapi.recv()
        self.netapi.reply_notif("OK")
        print('With unvalid',doc)


if __name__=="__main__":
    unittest.main()

