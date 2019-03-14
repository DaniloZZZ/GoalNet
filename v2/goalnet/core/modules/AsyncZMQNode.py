
"""
Created by Danil Lykov @danlkv on 04/03/19
"""

import zmq 
from goalnet.helpers.log_init import log
import trio
from itertools import count
COUNTER = count()

class AsyncZMQNode:
    def __init__(self, 
                 source:zmq.Socket,
                 drain:zmq.Socket,
                 timeout_ms = 2
                ):
        self.source = source
        self.drain = drain
        self.timeout_ms = timeout_ms

    async def node_fun(self, message, drain):
        raise NotImplementedError

    async def connection_handler(self,message, connection_id):
        try:
            notif = await self.node_fun(message, self.drain)
            if notif:
                self.drain.send_json(notif)
        except Exception as e:
            log.error("Task handler id:%d error %s"%(connection_id,str(e)))
            self.drain.send_json({"error":"error occured"})

    def _recv(self):
        return self.source.recv_json()

    async def server_listen_loop(self):
        source = self.source
        timeout_ms = self.timeout_ms

        async with trio.open_nursery() as nursery:
            while True:
                # need to poll socket to prevent blocking
                # coroutine task queue when client is silent
                status = source.poll(timeout_ms)
                if status == 1:
                    # we've got message, receive it
                    msg = self._recv()
                else:
                    # let trio process some other handlers
                    await trio.sleep(0)
                    continue
                # use counter to trace responses
                conn_id = next(COUNTER)

                log.debug('Got message: %s id: %i'%(msg, conn_id))
                nursery.start_soon(self.connection_handler, msg, conn_id)
                # give control to some other tasks
                await trio.sleep(0)

    def start(self):
        # this will block so we don't need a stop method
        trio.run(self.server_listen_loop)
