"""
Created by Danil Lykov @danlkv on 13/02/19

A class for generic message

NOTE:
    This is not yet used in code.
    I will probably better implemet a type tree
    that is stored in db to dynamically change values
"""
from enum import Enum

class MessageAction(Enum):
    CREATE = 0
    READ = 1
    UPDATE = 2
    DELETE = 3
    @classmethod
    def from_str(cls,string):
        d = {
            cls.CREATE:['create','c'],
            cls.READ:['read','r'],
            cls.UPDATE:['update','u'],
            cls.DELETE:['delete','del','d'],
        }
        print(list(d.items()))
        states = filter(
            lambda state: string in state[1],
            d.items()
        )
        return list(states)[0][0]

class Message:
    def __init__(self, action:MessageAction):
        self.action = action

    @classmethod
    def from_dict(cls,json):
        return cls(
            action = MessageAction.from_str(
                json['action']
            ),
        )

class NetworkMessage(Message):
    def __init__(self, 
                 action:MessageAction,
                 user_id:int,
                 app_id:int
                ):
        super().__init__(action)
        self.user_id = user_id
        self.app_id = app_id

    @classmethod
    def from_dict(cls,json):
        msg  = Message.from_dict(json)
        return cls(
            action = msg.action,
            user_id = json['user_id'],
            app_id = json['app_id']
            )
