
import zmq, os, time
import json
import multiprocessing as prc

from goalnet.helpers.log_init import log
from goalnet.core.utils import themify, dethemify
from .AsyncZMQNode import AsyncZMQNode
from .BaseModule import BaseModule

class AsyncModule(AsyncZMQNode, BaseModule):
    def __init__(self, netconf, db=None, name='BaseModule'):
        self.netconf = netconf
        self.name = name
        self.db = db
        source = self._get_mux_socket()
        drain = self._get_dmx_socket()
        super().__init__(source,drain)

    async def kernel_func(self, action, user_data):
        raise NotImplementedError

    async def node_fun(self, message, drain):
        user_id = message.get('user_id', -1)
        user_data = self.db.get_data(user_id)
        log.info('Calling kernel for uid %d with data %s \t and action %s'%(user_id,user_data,action))
        ####=====
        pure_map = await kernel_func(action, user_data)
        #-------- Wait here. Other connection can modify data!
        user_data = self.db.get_data(user_id)
        """
        return a pure map function that
        actually performs transformation
        to ensure that the notification from previous call
        of kernel_func is still relevant

        pure map performs some checks and returns a notification
        that should be sent
        """
        notif, new_data = self.pure_map(user_data)
        log.info('kernel returned: notif %s, data: %s'%(str(notif), str(new_data)) )
        self.set_data(user_id,new_data)
        ####=====
        log.info('Sending notif from uid %d with response to %s'%(user_id,action))
        return {'user_id':user_id,'notif':notif}

    # rewrite _recv method as in base module
    # to fit with SUB socket
    def _recv(self):
        raw = self.source.recv_string()
        topic, msg = dethemify(raw)
        return msg
