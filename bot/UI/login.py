from StateMachine import States
from frm import handles as h
from DataBase import db

ps =h.post
a = h.action

def contact_check(i,s,d,role=None):
    c= i.contact
    # check if user sent his own contact
    if i.from_user.id ==c.user_id:
        # database call
        if db.user_registered(c.phone_number):
            db.add_chat_id(c.phone_number,c.user_id)
            new_state = States.HOME
        else:
            new_state=States.NOT_REG
    else:
        new_state = States.TG_ERR
    return new_state, d

def set_name(i,s,**d):
    d['name'] = i.from_user.first_name
    return d

login_kb= [
    {'Send contact':a(contact_check,react_to='contact'),
     'kwargs':{'request_contact':True}},
    {'<- Back':a(States.START)}
]


UI={
    States.START:
    {'t':
     h.st(
         ("Hey %s, nice to meet you! "
          "I'm a GoalNet bot!"
          "What would you like to do?"), 
         'name'),
     'b':[
         {'Log in':a(States.TG)},
         {'Explore GoalNet':a(States.NOT_IMPLEMENTED)},
         {'Register':a(States.NOT_IMPLEMENTED)}
     ],
     'prepare':set_name,
    },
    States.TG:{
        't':
        h.st(
            ("%s, Please share your contact details"
             "so I can recognize you"),'name'),
        'kb':h.obj(login_kb)
    },

    States.TG_ERR:{
        't':
        h.st(
            ("%s, I'm afraid this is not your contact. "
             "Please share your contact"),'name'),
        'kb':h.obj(login_kb)
      },

    States.NOT_REG:{
        't':
        ("It seems that you are "
         "not currently registered in GoalNet."
         "Would you like to register now?"
         "Or contact GoalNet if you think "
         "here was a mistake"),
        'b':[
            {'Register':a(States.NOT_IMPLEMENTED)},
            {'Contact':a(States.CONTACT)}
        ]
    }
}
