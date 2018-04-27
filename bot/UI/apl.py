from StateMachine import States
from frm import handles as h
from DataBase import db

import pprint
pp = pprint.PrettyPrinter(indent=4)

ps =h.post
a = h.action
app_kb= [
    {'Home':a(lambda i,s,**d:\
              (States.HOME if d.get('role')\
               else States.ALL_COURSES, d
             ))},
    {'Login':a(States.TG)},
    {'Contact':a(States.CONTACT)}
]

def format_classes(cls,personal=False):
    if cls:
        t="\n*Schedule:*\n"
        for c in cls:
            t+=c['title']+'\n'
    else:
        t = "\nNo classes yet"
    return t
def format_course(c):
    f = "%d/%m,%H:%M"
    if c.get('from') and c.get('to'):
        fr = c['from'].strftime( f)
        to =c['to'].strftime( f)
    else:
        fr= 'No start time'
        to='No end time'
    return "*%s*\n *Dates*: %s-%s \n *Enrollment*: %s \n%s"%(
        c['title'],fr,to,'Open' if c.get('active') else 'Closed',
        c.get('description') or 'no description')
def gen_course_text(s,**d):
    pp.pprint(d)
    if d.get('role')=='student':
        c = db.get_course(d['course_id'])
    else:
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

UI={
    States.ALL_COURSES:{'t':'Have a look at our courses',
          'b': ps(lambda s,**d:\
                      list(map(lambda c:\
                                  {c.get('title') :\
                                    a(lambda i,s,**d:
                                        (States.COURSE,\
                                         dict(d,**{'course_id':str(c.get('_id')),
                                                   'course_name':c.get('title'),
                                                   'role':'applicant'})\
                                        )\
                                     )\
                                  },\
                               d['courses'])\
                          )\
                 ) ,
                 'prepare':lambda i,s,**d:\
                 dict(d,**{'courses':db.get_courses()}),
                 'kb_txt':"Welcome!",
                 'kb':h.obj(app_kb)
      },
    States.COURSE:{'t':ps(gen_course_text),
                 'b':[
                   h.choose('role',
                              {'student':{
                                  'Show assignments':a(States.ASSIGNMENTS),
                                  'Submit assignment':a(States.SEND_ASS),
                                  'My progress':a(States.PROGRESS)
                              }},
                              default = [
                                  {'Apply':a(States.APPLY) }
                              ]
                             )],
                 'prepare':lambda i,s,**d:\
                 dict(d,**{'classes':db.get_classes(d['course_id'])})
                  },
    States.APPLY:{'t': "Please type your first name",
                  'react':a(lambda i,s,**d:\
                                (States.LNAME,dict(d,fname=i.text)),
                                 react_to='text')
       },
    States.LNAME:{'t': "Please type your last name",
                  'react':a(lambda i,s,**d:\
                                (States.TG,dict(d,lname=i.text)),
                                 react_to='text')
       },
    States.PROGRESS:{'t':
                     h.st(("I 'm sorry %s, but I don't know how to provide "
                      "progress reports - yet. I'm still learning. Meanwhile, "
                      "course instructor will help you out for sure."),'name'),
                     'b':[{
                         'Back to home':a(States.HOME)}]
       },
}
