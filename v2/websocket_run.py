import goalnet as g
from goalnet.connectors import start_websocket

def main():
    cnf = g.start_cnf()
    mux_p = g.start_mux(parallel=True)
    dmx_p = g.start_dmx(connectors=['websocket'], parallel=True)
    db_process = g.start_module('database')
    start_websocket()

if __name__=="__main__":
    main()
