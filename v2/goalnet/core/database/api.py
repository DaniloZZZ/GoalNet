import logging as log
import zmq

class DatabaseAPI:
    def __init__(self, netconf):
        self.db_path = netconf.get_address('database')
        ctx = zmq.Context()
        self.s = ctx.socket(zmq.REQ)
        self.s.connect(self.db_path)

    def get(self,request):
        log.debug("sending '%s' to db"%request)
        self.s.send_json(request)
        return self.s.recv_json()
    
# a wrapper class to inherit db get from
def with_db_api(Cls):
    class WithDB_API(Cls, DatabaseAPI):
        def __init__(self, netconf, *args, **kwargs):
            super().__init__(netconf, *args, **kwargs)
            DatabaseAPI.__init__(self, netconf)

        def db_call(self,request):
            return DatabaseAPI.get(self,request)
    return WithDB_API
