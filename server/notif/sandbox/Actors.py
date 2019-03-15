from Types import *
import db
def type_check(a,b):
    if isinstance(a,Type) and isinstance(b,Type):
        return a.__type__==b.__type__
    else:
        return isinstance(a,b)

class Merger:
    I = [Link,Link]
    O = [Link]

    def __init__(self):
        print('new Merger')

    def check(self,op):
        if len(self.I)!=len(op):
            raise Exception("Input format err")
        if type(self.I[0])!=type(op[0]):
            raise Exception("Input format err")
        return

    def apply(op):
        self.check_op(op)
        dic ={
            'ref':(op[0].ref,op[1].ref)
        }
        res = Link(
            dic,
            op[0].__type__+op[1].__type__
        )
        #res.__type__=
        return res

class Getter:
    I = Link
    def __init__(self,
                 i_type,
                 o_type,
                 op
                ):
        print('new Getter',i_type,o_type)
        self.func = op
        self.I_t = i_type
        self.O = o_type

    def check_op(self,op):
        if not isinstance(op,self.I):
            raise Exception("Input format err",op,self.I)
        if not op.target_type == self.I_t:
            raise Exception("Input format err",op,self.I)
        return

    def apply(self,op):
        self.check_op(op)
        return self.func(op.ref)

class Notif:
    I = [Record,Link,Link]
    O = [Notification]
    def __init__(self):
        print("new Notif")

    def apply(self,op):
        g_getter = Getter(Goal,Goal,db.get_goal)
        H_getter = Getter(Goal_Notif,Goal_Notif,
                          db.get_goal_notif)
        goal = g_getter.apply(op[1])
        H = H_getter.apply(op[2])
        notif = H.apply(goal)
        return notif

