
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
        self.db[uid]=user
        
    def user_by_id(self, uid):
        return self.db[uid]
    def user_by_email(self, email):
        for uid, u in self.db.items():
            print("uid",uid,email,u)
            if u.get('email')==email:
                return u

