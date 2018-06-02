from StateMachine import States
from tgflow import handles as h
from DataBase import db

ps =h.post
a = h.action

UI={
    States.NOTIF:{
        't':ps('Hey! Time to do %s',
               'notif-goal'
              ),
        'b':[
            {'Start pomodoro':a(States.NOT_IMPLEMENTED)},
            {'Pick another goal':a(States.NOT_IMPLEMENTED)},
            {'Remind me in 5 min':a(States.NOT_IMPLEMENTED)},
        ]
    }
}
