import zmq, yaml
import argparse

config_file = 'config.yml'

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
            'vksleep':base_addr + '9013',
            'logger':base_addr + '9011',
            'echo':base_addr + '9012',
            }
    return netconf

def handle_request(req):
    if req == 'netconfig':
        return _get_netconfig()
    err = {
            'error':'request didnt match'
            }
    return err

def main():
    config = read_config()
    addr = config['config_address']
    ctx = zmq.Context()
    s = ctx.socket(zmq.REP)
    s.bind(addr)
    print("config server listening on",addr)
    while True:
        request = s.recv_string()
        _print("got request", request)
        info = handle_request(request)
        s.send_json(info)

if __name__=='__main__':
    main()
