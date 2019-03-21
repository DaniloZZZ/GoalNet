from .node import DBNode
import logging as log
import goalnet as g
from .file_db import FileDB

class Database(DBNode):
    def __init__(self, netconf):
        super().__init__(netconf)
        fname = '/home/danlkv/GoalNet/v2/goalnet/core/database/db.json'
        self.db = FileDB(fname)

    def _write_db(self):
        with open(fname, 'w+') as f:
            json.dump(self.db,f)
    def _read_db(self):
        try:
            with open(fname, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError as e:
            self.db = {}
            self._write_db()

    def connection_handler(self, message):
        request = message['request']
        action, trait = request.split('.')
        if trait == 'user':
            m = message
            if action=='new':
                self.db.new_user(**message)
                return {"status":0}
            if action=='get':
                uid, email, token = (message.get("uid"),
                                     message.get('email'),
                                     message.get('token')
                                    )
                if uid:
                    return self.db.user_by_id(uid)
                if email:
                    return self.db.user_by_email(email)
                if token:
                    return self.db.user_by_token(token)


def start_database():
    netconf = g.get_network_config()
    db = Database(netconf)
    db.start()
    return db

if __name__=="__main__":
    start_database()

