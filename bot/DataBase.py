from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import urllib,os
import re

import config

class DataBase():
    def __init__(self):
       self.client = MongoClient(config.db_addr, 27017)
       self.db = self.client.local

# User-related
    def user_registered(self,number):
        print('DB>checking if user is registered')
        number = ''.join(re.findall(r'\d+',str(number)))
        u = self.db.Users.find_one({'phone':(number)})
        print('Found %s user for plone %i'%(u,int(number)))
        if u==None:
            return 0
        else: return 1

    def user_gmail(self,tg):
        u = self.db.Users.find_one({'tgchat':int(tg)})
        if 'gmail' in u.keys():
            return 1
        else: return 0

    def add_chat_id(phone_number,user_id):
        #TODO: add chat id method
        print("NOT_IMPLEMENTED")
        return 0

    def save_new_user(self,user):
        print('saving new user %s '%str(user))
        self.db.Users.save(user)

    def update_user(self,user_id, user_update):
        print('updating user %s with data: %s'%(str(user_id), str(user_update)))
        self.db.Users.update({'_id':user_id}, {'$set': user_update})

    def save_gmail(self,gmail,tg):
        user = self.db.Users.find_one({'tgchat':int(tg)})
        user['gmail']=gmail
        print('saving %s g for %s'%(gmail,str(tg)))
        self.db.Users.save(user)
        return 0

db = DataBase()
