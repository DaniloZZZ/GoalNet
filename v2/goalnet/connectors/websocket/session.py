import time

def gen_user_id():
    return time.time().as_integer_ratio()[0]

def gen_user_token():
    # TODO: change this to something more relevant
    return time.time().as_integer_ratio()[1]

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def check_token(self, token):
        uid = self.sessions.get(token)
        return uid

    def save_user_token(self, user_id, token):
        user_id = int(user_id)
        self.sessions[token] = user_id
