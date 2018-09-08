from StateMachine import States
from tgflow import handles as h
from tgflow.coffee_ui import CoffeeUI

ps =h.post
a = h.action

def set_name(i,s,**d):
    d['name'] = i.from_user.first_name
    return d

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
    States.CONTACT:{
        't':
        ("Tell me what's on your mind, and I'll pass it over to"
         "the rest of GoalNet team. We'll get back to you shortly"),
        'b':[{"To start":a(States.START)}],
        'react':a(States.CONTACT_THANKS,react_to='text')
    },
    States.ERROR:{
        't':
        # TODO: prompt user for contacts
        ("Sorry, an error occured."
         "Please contact us on web"),
        'b':[{'To start':a(States.START)}]
    },
}
cof= CoffeeUI(
    """
    CONTACT_THANKS:
        t:'Thank you for your question, we will get to you shortly'
        b:['To start':a 'START']
    NOT_IMPLEMENTED:
        t: 'This feature is not yet implemented'
        b:['Home':a 'HOME']
    """,
    States)
c = cof.get_ui()
UI.update(c)
