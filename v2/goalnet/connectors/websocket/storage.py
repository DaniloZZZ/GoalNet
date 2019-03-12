class Storage:
    def __init__(self):
        self.connections = {}
        self.temp_connections = {}

    def add_connection(self,conn,user_id=None):
        if user_id:
            self.connections[user_id] = conn
        else:
            user_id = -len(self.temp_connections.keys())-1
            self.temp_connections[user_id] = conn
        return user_id

    def remove_connection(self,user_id):
        if user_id>0:
            return self.connections.pop(user_id,None)
        elif user_id<0:
            return self.temp_connections.pop(user_id,None)
        else:
            return None

    def get_connection(self,user_id):
        if user_id>0:
            return self.connections.get(user_id)
        elif user_id<0:
            return self.temp_connections.get(user_id)
        else:
            return None


