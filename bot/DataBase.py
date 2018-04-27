from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime, pytz
import urllib,os
import re

import config

class DataBase():
    def __init__(self):
        self.client = MongoClient(config.db_addr, 27017)
        self.db = self.client.local

    def get_courses(self, tg=None):
        if tg:
            u = self.db.Users.find_one({'tgchat':tg})
            crids = u.get('courses_enrolled')
            if not crids: return []
            ids = [ObjectId(c['course_id']) for c in crids]
            crs = self.db.Courses.find({'_id':
                                        {'$in':ids}
                                       })
        else:
            crs = self.db.Courses.find({})
        if crs is not None:
            return [c for c in crs]
        else: return None


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

    def save_new_user(self,user):
        print('saving new user %s '%str(user))
        user['created'] = datetime.datetime.now(pytz.utc)
        self.db.Users.save(user)

    def update_user(self,user_id, user_update):
        print('updating user %s with data: %s'%(str(user_id), str(user_update)))
        user_update['updated'] = datetime.datetime.now(pytz.utc)
        self.db.Users.update({'_id':user_id}, {'$set': user_update})

    def save_new_course(self,course):
        print('saving new course %s '%str(course))
        course['created'] = datetime.datetime.now(pytz.utc)
        self.db.Courses.save(course)

    def update_course(self,course_id, course_update):
        print('updating course %s with data: %s'%(str(course_id), str(course_update)))
        course_update['updated'] = datetime.datetime.now(pytz.utc)
        self.db.Courses.update({'_id':course_id}, {'$set': course_update})

    def save_gmail(self,gmail,tg):
        user = self.db.Users.find_one({'tgchat':int(tg)})
        user['gmail']=gmail
        print('saving %s g for %s'%(gmail,str(tg)))
        self.db.Users.save(user)
        return 0

    def add_chat_id(self, number,tg):
        number = ''.join(re.findall(r'\d+',str(number)))
        user = self.db.Users.find_one({'phone':number})
        if user == None:
            return 1
        print(number,tg)
        if 'tgchat'not in user.keys():
            user['tgchat']=int(tg)
            print('incerting',tg)
            self.db.Users.save(user)
        return 0
# Assignments
    def save_assignment(self,**data):
        fn = 'user_'+data['user']+'/'+'ass_'+data['course_id']
        folder =  'user_'+data['user']
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
            print('Getting user attachment %s '%data['link'])
            urllib.request.urlretrieve(data['link'],filename=fn)
            print('Done. Saved to %s'%fn)
            return 0
        except Exception as e:
            print("Error",e)
            return 1

# Courses and classes
    def get_classes(self, course_id):
        course = self.get_course(course_id)
        if not course:
            print("ERROR: course with id %s not found"%course_id)
            return []
        if not course.get('classes'):
            print("ERROR: course with id %s has no classes field"%course_id)
            return []
        classes = []
        for class_id in course['classes']:
            class_= self.db.Classes.find_one({'_id':ObjectId(class_id)})
            if class_:
                classes.append(class_)
            else:
                print("WARNING: for classes specified in course %s one with id %s was not found in db"%(course_id,class_id))
        return classes

    def get_course(self, course_id):
        course = self.db.Courses.find_one({'_id':ObjectId(course_id)})
        return course

    def get_user_by_email(self, email):
        user = self.db.Users.find_one({'email':email})
        return user

    def get_course_by_title_group(self, title, group):
        course = self.db.Courses.find_one({'title':title,'group':group})
        return course

    def get_class_by_id(self, class_id):
        class1 = self.db.Classes.find_one({'_id':ObjectId(class_id)})
        return class1

    def get_user_by_id(self, user_id):
        user = self.db.Users.find_one({'_id':ObjectId(user_id)})
        return user

    def save_class_braincert_id(self, class_info, braincert_id):
        print('\n Updating %s with new braincert class id %s '%(class_info["_id"], braincert_id))
        class_info['updated'] = datetime.datetime.now(pytz.utc)
        class_info['braincert_id'] = braincert_id
        self.db.Classes.save(class_info)

    def save_user_link_to_classroom(self, class_info, user_id, link):
        print('\n Updating %s with new link for %s '%(class_info["_id"], user_id))
        class_info['updated'] = datetime.datetime.now(pytz.utc)
        user = self.get_user_by_id(user_id)
        class_info['users'][user_id] = {'class_link': link, 'lastname' : user['lastname']}
        self.db.Classes.save(class_info)

    def get_courses(self, tg=None):
        if tg:
            print('tgchat %i'%tg)
            user = self.db.Users.find_one({'tgchat':tg})
            if not user:
                print('got no users for %i while getting courses'%tg)
                return None
            print('getting courses of user ',user['_id'])
            crs = self.db.Courses.find({'users':
                            {'$elemMatch':{'user_id':ObjectId(user['_id'])}}
                            })
        else:
            # return all unique courses for description
            names = self.db.Courses.distinct("title")
            names = list(names)
            print('uniq names',list(names))
            crs = self.db.Courses.find({})
            courses = []
            for c in crs:
                if c['title'] in names:
                    courses.append(c)
                    names.remove(c['title'])
            crs = courses
        if crs is not None:
            return [c for c in crs]
        else: return None

print('db')
db = DataBase()
