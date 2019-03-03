"""
Created by Danil Lykov @danlkv on 13/02/19
"""

#from .connectors.console import launch_console_connector
from .core.modules.echo import EchoModule
from .core.modules.logger import  LoggerModule
from .config_server import start_config_server

# TODO: muxMuxMUX looks ugly
from .core.mux.MUX import MUX
from .core.dmx.DMX import DMX

import multiprocessing as prc

from .utils import get_network_config

MODULES = {
    'logger':LoggerModule,
}

def start_maybe_parallel(func,name,args=[],parallel=True):
    if not parallel:
        print("starting %s server..."%name)
        func()
    else:
        print("starting %s server in process..."%name)
        return processed(func,args=args,name=name)

def conf_start_node(func,name,parallel=True):
    netconf = get_network_config()
    return start_maybe_parallel(func,args=(name,netconf),
                         name=name, parallel=parallel
                        )

def start_connector():
    start_config_server()

def start_module(name):
    Module = MODULES[name]
    netconf = get_network_config()
    print("starting module",name)
    module = Module(netconf, name=name)
    module.start()
    return module

def start_connector():
    start_config_server()

def start_mux(parallel=False):
    return conf_start_node(
        MUX,
        'MUX',
        parallel=parallel
    )

def start_dmx(parallel=False):
    return start_maybe_parallel(
        DMX,
        'DMX',
        parallel=parallel
    )

def start_cnf(parallel=True):
    return start_maybe_parallel(
        start_config_server,
        'config',
        parallel=parallel
    )

def processed(fun,args=[],name=None):
    p= prc.Process(target=fun,args=args,name=name)
    p.daemon=True
    p.start()
    return p

def main():
    netconf = get_network_config()
    inp,out = prc.Pipe()

    mux = prc.Process(target=MUX, args=('MUX',netconf),name='mux')
    dmx = prc.Process(target=DMX, args=('DMX',netconf),name='dmx')
    logm = LoggerModule(netconf,name='logger')
    echom = EchoModule(netconf,name='echo')
    console = prc.Process(target=launch_console_connector, args=('console',netconf,out),name='console')

    print("Goalnet sandbox is starting...")
    try:
        mux.start()
        dmx.start()
        logm.start()
        echom.start()
        console.start()
        print("Console pid is:",console.pid)
        while True:
            inp_text = input('Action message>>>')
            inp.send(inp_text)

    except Exception as e:
        print("Exception, terminating all")
        mux.terminate()
        dmx.terminate()
        logm.terminate()
        echom.terminate()
        console.terminate()
        raise e

if __name__=='__main__':

    main()
