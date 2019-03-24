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

    def user_by_token(self,token):
        return self.get({
            'request':'get.user',
            'token':token
        })
    def get_modules(self,user_id):
        return self.get({
            'request':'get.module',
            'user_id':user_id,
        })
    def add_module(self,user_id,module):
        return self.get({
            'request':'add.module',
            'user_id':user_id,
            'name':module
        })


# a wrapper class to inherit db_call method 
def with_db_api(Cls):
    class WithDB_API(Cls, DatabaseAPI):
        def __init__(self, netconf, *args, **kwargs):
            super().__init__(netconf, *args, **kwargs)
            DatabaseAPI.__init__(self, netconf)

        def db_call(self,request):
            return DatabaseAPI.get(self,request)
    return WithDB_API
