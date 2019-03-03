import trio
import logging
from trio_tracer import Tracer
###
FORMAT = '[%(asctime)s.%(msecs)3d::%(levelname)-5s::%(module)s]\t%(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    format = FORMAT,
    datefmt = '%M:%S',
)
log = logging.getLogger('trio_test')
###

async def sleep_log3_call(time,callback):
    log.debug('waiting for % seconds'%time)
    await trio.sleep(time)
    log.debug('waiting for % seconds'%time)
    await trio.sleep(time)
    log.debug('calling callback')
    res =  callback()
    return res

async def corosleep_log3_call(time,callback):
    coro1 = trio.sleep(time)
    coro2 = trio.sleep(time)
    log.info('coros were created!')
    log.debug('waiting for %s seconds'%time)
    await coro1
    log.debug('waiting for %s seconds'%time)
    await coro2
    log.debug('calling callback')
    res =  callback()
    return res

async def parent():
    log.info('parent started')
    async with trio.open_nursery() as nursery:
        nursery.start_soon(corosleep_log3_call,1,calee)
        nursery.start_soon(sleep_log3_call,1,calee)
    log.info('All done')

def calee():
    print("caleee")
    return 8

#trio.run( sleep_log3_call, 1, calee)
#trio.run( corosleep_log3_call, 1, calee)
trio.run(parent, instruments=[Tracer()])

