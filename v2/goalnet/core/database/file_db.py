
import json
import logging as log

def updates_db(method):
    def f(self,*a,**kw):
        method(self,*a,**kw)
        self._write_db()
    return f

class FileDB:
    def __init__(self,fname):
        self.fname = fname
        self._read_db()

    def _write_db(self):
        print("selfld",self.db)
        with open(self.fname, 'w+') as f:
            json.dump(self.db,f)
    def _read_db(self):
        try:
            with open(self.fname, 'r') as f:
                try:
                    self.db = json.load(f)
                except Exception as e:
                    log.error(str(e))
        except FileNotFoundError as e:
            self.db = {}
            self._write_db()

    @updates_db
    def new_user(self, **user):
        uid = user['user_id']
        log.debug("new user %s"%user)
        uid =str(uid)
        self.db[uid]=user

    def user_by_id(self, uid):
        uid = str(uid)
        log.debug("User ids in db: %s"%list(self.db.keys()))
        return self.db[uid]
    def user_by_email(self, email):
        for uid, u in self.db.items():
            if u.get('email')==email:
                return u
    def user_by_token(self, token):
        log.debug("looking for user of token %s"%token)
        for uid, u in self.db.items():
            if u.get('token')==token:
                return u
    
    @updates_db
    def add_module(self,user_id, name, **k):
        log.debug("addin module user %s"%user_id)
        print(type(user_id))
        usr = self.user_by_id(user_id)
        try:
            m = usr['modules']
        except KeyError:
            usr['modules'] = []
        usr['modules'].append(name)
        
    def get_modules(self, user_id, **k):
        log.debug("getting module user %s"%user_id)
        usr = self.user_by_id(user_id)
        try:
            m = usr['modules']
        except KeyError:
            usr['modules'] = []
        return usr['modules']


