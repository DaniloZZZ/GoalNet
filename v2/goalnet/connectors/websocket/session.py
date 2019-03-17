import time

def gen_user_id():
    return time.time().as_integer_ratio()[0]

def gen_user_token():
    # TODO: change this to something more relevant
    return time.time().as_integer_ratio()[1]

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def check_user(self, user_id, token):
        dbtoken = self.sessions.get(user_id)
        if not dbtoken:
            return
        if token==dbtoken:
            return True

    def add_user(self):
        user = gen_user_id()
        token = self.add_user_token(user)
        return user,token

    def create_user_token(self,user_id):
        token = gen_user_token()
        self.save_user_token(token)
        return token

    def save_user_token(self, user_id, token):
        user_id = int(user_id)
        self.sessions[user_id] = token
