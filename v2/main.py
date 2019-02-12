"""
Created by Danil Lykov @danlkv on 13/02/19
"""

from connectors.console import launch_console_connector
from core.modules.echo import  launch_echo
from core.modules.logger import  launch_logger
# TODO: this looks ugly
from core.mux.MUX import MUX
from core.dmx.DMX import DMX

import multiprocessing as prc

from utils import get_network_config

netconf = get_network_config()

def main():
    inp,out = prc.Pipe()

    mux = prc.Process(target=MUX, args=('MUX',netconf),name='mux')
    dmx = prc.Process(target=DMX, args=('DMX',netconf),name='dmx')
    logm = prc.Process(target=launch_logger, args=('logger',netconf),name='log')
    echom = prc.Process(target=launch_echo, args=('echo',netconf),name='echo')
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

main()
