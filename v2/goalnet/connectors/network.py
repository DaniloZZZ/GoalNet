import zmq
import logging as log
import multiprocessing.dummy as thread

def _print(*args):
    print(">netconnn>",*args)

class ConnectorNetwork:
    def __init__(self,netconf,appid,name):
        self.netconf = netconf
        self.appid = appid
        self.name = name
        self.myaddr = self.netconf.get_address(name)

        mux_addr = self.netconf.get_address('MUX_in')
        ctx = zmq.Context()
        self.mux_sock= ctx.socket(zmq.PUSH)
        log.debug("connecting to MUX on %s"%mux_addr)
        self.mux_sock.connect(mux_addr)

        self.notif_sock = ctx.socket(zmq.REP)
        log.debug("binding %s to %s"%(self.name,self.myaddr))
        self.notif_sock.bind(self.myaddr)

    def send(self,message):
        message['app_id']=self.appid
        self.mux_sock.send_json(message)

    def recv(self):
        return self.notif_sock.recv_json()

    def poll(self, timeout=None):
        return self.notif_sock.poll(timeout)

    def reply_notif(self,response):
        self.notif_sock.send_string(response)

    def listen_for_notif(self, callback):
        def listener(callback):
            _print("Listening DMX on %s ..."%self.myaddr)
            while True:
                notif = self.notif_sock.recv_json()
                try:
                    response = callback(notif)
                except Exception as e:
                    _print("ERROR in notif callback. sending fail")
                    self.notif_sock.send_string("FAIL")
                    raise e

                self.notif_sock.send_string(response)

        p = thread.Process(target=listener, args=(callback,),
                name=self.name+'_notif_listen')
        p.start()
        return p

