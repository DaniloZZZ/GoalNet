import zmq
import multiprocessing.dummy as thread

class ConnectorNetwork:
    def __init__(self,netconf,appid,name):
        self.netconf = netconf
        self.appid = appid
        self.name = name
        self.myaddr = self.netconf.get_address(name)

        mux_addr = self.netconf.get_address('MUX_in')
        ctx = zmq.Context()
        self.mux_sock= ctx.socket(zmq.PUSH)
        self.mux_sock.connect(mux_addr)

        self.notif_sock = ctx.socket(zmq.REP)
        self.notif_sock.bind(self.myaddr)

    def send(self,message):
        message['appid']=self.appid
        self.mux_sock.send_json(message)

    def listen_for_notif(self, callback):
        def listener(callback):
            while True:
                notif = self.notif_sock.recv_json()
                response = callback(notif)
                self.notif_sock.send_string(response)

        p = thread.Process(target=listener, args=(callback,),
                name=self.name+'_notif_listen')
        p.start()
        return p

