"""
Created by Danil Lykov @danlkv on 14/02/19

A NotifScheduler class starts a thread that
checks a queue for due time

"""

# import sched # won't sched if already runnting
import multiprocessing.dummy as thread
import time

class CallScheduler:
    def __init__(self):
        self.queue = []
        self.timefunc = time.time
        self.delayfunc = time.sleep

    def _collect_due(self,intents=[]):
        t = self.timefunc()

        intents = [ i for i in self.queue if i[0]<t ]
        return intents

    def enter(self, delay, func, args=None):
        resolv = self.timefunc() + delay
        self.queue.append((resolv,func,args))
        #print("queue",self.queue)

    def run(self):
        while True:
            if not self.queue:
                # let other threads run
                self.delayfunc(0)
                continue

            intents = self._collect_due()
            if not intents:
                # let other threads run
                self.delayfunc(0.05)
                continue

            for intn in intents:
                resolv, func, args = intn
                #TODO: use tagging to manage other intents
                # based on return value
                self.queue.remove(intn)
                func(*args)
                # let other threads run
                self.delayfunc(0)

    def start(self):
        print("NotifScheduler running...")
        threadify(self.run)

def threadify(func,args=[]):
    p = thread.Process(target=func,args=args)
    p.start()
