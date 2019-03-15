import trio
import logging
from logger_init import log
from trio_tracer import Tracer
# a dummyy calback funtion that uses state
class State:
    def __init__(self):
        self.val = 1
    def inc(self,num):
        self.val += num
        print("state is now",self.val)

state = State()
def calee(num):
    """
    This function just calls a method that modifies a state
    The point is that if I have different workers that are 
    manipulating state these changes will be out of order.

    Thus, only using the state as a storage that provides 
    an _immutable for worker_ and scoped piece of data
    """
    state.inc(num)
    print("caleee")

# Vanilia sleeping example
async def sleep_log3_call(time,callback):
    log.debug('waiting for % seconds'%time)
    await trio.sleep(time)
    log.debug('waiting for % seconds'%time)
    await trio.sleep(time)
    log.debug('calling callback')
    res =  callback(2)
    return res

# First get coroutines, and then await them
async def corosleep_log3_call(time,callback):
    coro1 = trio.sleep(time)
    coro2 = trio.sleep(time)
    log.info('coros were created!')
    log.debug('waiting for %s seconds'%time)
    await coro1
    log.debug('waiting for %s seconds'%time)
    await coro2
    log.debug('calling callback')
    res =  callback(20)
    return res

# Use a nurcery to wait for all processes
async def parent():
    log.info('parent started')
    async with trio.open_nursery() as nursery:
        nursery.start_soon(corosleep_log3_call,1,calee)
        nursery.start_soon(sleep_log3_call,1,calee)
    log.info('All done')


#trio.run( sleep_log3_call, 1, calee)
#trio.run( corosleep_log3_call, 1, calee)
#trio.run(parent, instruments=[Tracer()])
trio.run(parent, instruments=[])
