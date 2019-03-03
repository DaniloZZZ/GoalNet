import zmq, yaml
import argparse

config_file = 'config.yml'

class StopSignal(Exception):
    pass

def _print(*args):
    print(">control server>",*args)

def read_yaml(name):
    with open(name, 'r') as stream:
        data= yaml.load(stream)
    return data

def read_config():
    config = read_yaml(config_file)
    return config

def _get_netconfig():
    base_addr = 'tcp://127.0.0.1:'
    netconf = {
            'MUX_in':base_addr + '9000',
            'MUX_out':'tcp://127.0.0.1:'+ '9001',
            'DMX':base_addr + '9002',
            'DB':base_addr + '9003',
            'console':base_addr + '9101',
            'telegram':base_addr + '9102',
            'vk':base_addr + '9103',
            'tasks':base_addr + '9104',
            'self_loop':base_addr + '9105',

            'vksleep':base_addr + '9013',
            'logger':base_addr + '9011',
            'echo':base_addr + '9012',
            }
    return netconf

def handle_request(req):
    if req == 'netconfig':
        return _get_netconfig()
    # TODO: Is this secure?
    elif req == 'stop':
        raise StopSignal()
    err = {
            'error':'request didnt match'
            }
    return err

def shut_down():
    print("Shutting down")

def start_config_server():
    config = read_config()
    addr = config['config_address']
    ctx = zmq.Context()
    s = ctx.socket(zmq.REP)
    s.bind(addr)
    print("config server listening on",addr)
    while True:
        request = s.recv_string()
        _print("got request", request)
        try:
            info = handle_request(request)
        except StopSignal:
            print("Stop Signal received")
            shut_down()
            return
        s.send_json(info)

def main():
    start_config_server()

if __name__=='__main__':
    main()
