import time

class Type:
    name = "Base Type"
    __type__="<basetype>"
    def __repr__(self):
        return '<GoalNet Type %s>'%self.name

class Notification(Type):
    name = "Notification"
    __type__="<notif>"
    def __init__(self,dic):
        self.data = dic
        self._created  = time.time()

class Record(Type):
    name = "Record"
    __type__="<record>"
    def __init__(self,dic):
        self.data = dic
        self._created  = time.time()

class Goal(Type):
    name = "Goal"
    __type__ = "<goal>"
    def __init__(self,dic):
        self.data = dic
        self._created  = time.time()

class Link(Type):
    name = "Link"
    __type__ = "<link>"
    def __init__(self,dic,rtype):
        """
        :param: rtype type of the obj where link to
        """
        self.data = dic
        self.ref = dic.get('ref',0)
        self.target_type = rtype
        self._created  = time.time()
T
class Goal_Notif(Type):
    name = "Goal to Notification funct"
    __type__ = "<goal->notif>"
    def __init__(self,dic,func=None):
        self.data = dic
        self.op = func
        self._created  = time.time()

    def check_op(self,op):
        if not isinstance(op,Goal):
            raise Exception("Input format err",op,self.I)

    def apply(self,op):
        self.check_op(op)
        print('applying',self.__type__)
        # TODO: check types output
        return self.op(op)


