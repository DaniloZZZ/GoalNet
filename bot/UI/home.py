from StateMachine import States
from frm import handles as h
from DataBase import db
from frm.TgFlow import get_file_link

ps =h.post
a = h.action

def contact_check(i,s,**d):
    db = DataBase()
    c= i.contact
    if i.from_user.id ==c.user_id:
        if db.user_registered(c.phone_number):
            db.add_chat_id(c.phone_number,c.user_id)
            d['role']='student'
            if db.user_gmail(c.user_id):
                new_state = States.HOME
            else:
                new_state=States.GMAIL
        else:
            new_state=States.NOT_ENROLLED
    return new_state, d

home_kb= [
    {'Home':a(States.HOME)},
    {'Contact':a(States.CONTACT)}
]

def format_classes(cls,personal=False):
    t="*Schedule:*\n"
    for c in cls:
        t+=c['title']+'\n'
    return t
def format_course(c):
    f = "%d/%m,%H:%M"
    fr = c['from'].strftime( f)
    to =c['to'].strftime( f)
    return "*%s*\n *Dates*: %s-%s \n *Enrollment*: %s \n%s"%(
        c['title'],fr,to,'Open' if c['active'] else 'Closed',
        c['description'])
def gen_course_text(s,**d):
    c = db.get_course(d['course_id'])
    t=''
    if d['role']=='student':
        t+='Your course details:\n'
        t+=format_course(c)
        t+=format_classes(d['classes'],personal=True)

    if d['role']=='applicant':
        t+='Course details:\n'
        t+=format_course(c)
        t+=format_classes(d['classes'])
    return t

def get_courses(i,s,**d):
    crs = db.get_courses(i.from_user.id)
    if crs:
        d['role']='student'
    d['courses']=crs
    print('crsdfj',crs)
    return d

def save_assignment(i,course_id=None):
    print ('INP',i)
    error= db.save_assignment(**{
                           'user':str(i.from_user.id),
                           'course_id':course_id,
                           'link':get_file_link(i.document.file_id),
    })
    if not error:
        return States.SUCCESS_ASS
    else:
        return States.ERROR

UI={
    States.HOME:{'t':'Here are your courses',
          'b':[{'List other Fless courses':a(States.ALL_COURSES)},
               # button to display each course with title on it
               ps(lambda s,**d:\
                  list(map(lambda c:\
                      {c.get('title') : a(lambda i,s,**d:
                            (States.COURSE,\
                             # and also save course_id he picked
                             dict(d,**{'course_id':str(c.get('_id')),
                                       'course_name':c.get('title'),
                                       'role':'student'})\
                            ))},\
                    d['courses'])))
              ],
                 'prepare':get_courses,
                 'kb_txt':"Welcome!",
                 'kb':h.obj(home_kb)
      },

    States.ASSIGNMENTS:{'t':
                        h.st("*Your assignments for* %s",'course_name'),
                        'b':[{
                            'Show my progress':a(States.PROGRESS)}]
                        #'fetch':True
       },
    States.SEND_ASS:{'t':
                h.st("Please send me your assignment for %s",'course_name'),
                     'b':[{
                         'Back':a(States.HOME)}],
                     'react':a(save_assignment,react_to='document'),
       },
    States.SUCCESS_ASS:{'t':
                     ("Success! Thank you for assignment"),
                     'b':[{
                         'Back to home':a(States.HOME)}]
       },
    States.PROGRESS:{'t':
                     h.st(("I'm sorry %s, but I don't know how to provide "
                      "progress reports - yet. I'm still learning. Meanwhile, "
                      "course instructor will help you out for sure."),'name'),
                     'b':[{
                         'Back to home':a(States.HOME)}]
       },
}
