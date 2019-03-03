"""
This file provides methods for telegram bot
to save telegram id of user
to acces saved data
"""

class DB:
    def __init__(self):
        self.telegram_user={
                '1':'1'
                }

    def get_tg_id(self,uid):
        return self.telegram_user.get(uid)

    def save_tg_id(self,uid,tgid):
        self.telegram_user[uid]=tgid
        print('saved tgid, db:',self.telegram_user)


