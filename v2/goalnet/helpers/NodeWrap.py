from goalnet.helpers.log_init import log
from goalnet.utils import get_network_config

import multiprocessing as proc
def NodeWrap(Module,name):
    def start(name):
        netconf = get_network_config()
        mod = Module(netconf,name=name)
        mod.start()
    process = proc.Process(target=start, args=(name,), name='proc_'+name)
    process.start()
    return process

