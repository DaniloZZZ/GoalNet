import zmq
import logging as log
import multiprocessing as prc
import time

class DBNode:
    def __init__(self, netconf, name="Database"):
        self.name=name
        self.listen_addr = netconf.get_address('database')

    def _init_sockets(self):
        ctx = zmq.Context()
        listen_addr = self.listen_addr
        self.socket = ctx.socket(zmq.REP)
        log.debug("Binding database to addr %s"%listen_addr)
        self.socket.bind(listen_addr)

    def _recv(self):
        return self.socket.recv_json()

    def _node_loop(self):
        self._init_sockets()
        sock = self.socket

        while True:
            msg = self._recv()
            log.debug('Got msg %s'%msg)
            try:
                response = self.connection_handler(msg)
            except Exception as e:
                log.error("Error in db: %s"%str(e))
                response = {"error":str(e)}
            sock.send_json(response)
            time.sleep(0)

    def start(self):
        p = prc.Process(target=self._node_loop, name=self.name)
        p.start()
        self.p = p
        return p
    def terminate(self):
        self.p.terminate()
        self.p.join()
