import trio
import json
from trio_websocket import serve_websocket, ConnectionClosed
from goalnet.helpers.trio_tracer import Tracer

from goalnet.utils import get_network_config
from .. import NetworkAPI
from .storage import Storage
from goalnet import log

async def echo_server(request):
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            print("Message!",message)
            await ws.send_message(message)
        except ConnectionClosed:
            break
def handle_notif(notif,storage):
    act = notif.get('action')
    user_id = notif.get('user_id')
    if act=="add.user.auth":
        token = notif.get('token')
        if not token: return {"error":"auth error"}
        log.debug("saving token '%s' to user id %s"%(token,user_id))
        storage.sessman.save_user_token( user_id, token)
        return {'result':'0','token':token,'user_id':user_id}
    # fallback to original notif
    return notif

async def listen_for_notif(netapi, storage):
    async def  on_notification(notif):
        # check if output from system has user_id
        # it is needed to get target ws connection
        user_id = notif.get('user_id')
        if not user_id:
            log.error('No user id field in notif %s'%notif)
            return 'FAIL: no user_id'
        #TODO: add logging and better checking
        resp =  handle_notif(notif,storage)
        # sanity check.
        if not resp: return "FAIL"

        # get websocket connection 
        ws = storage.get_connection(user_id)
        if not ws:
            log.error('No connection for id for notif %s'%notif)
            return ('FAIL: not connected')

        notif = resp
        log.info('Sending notif to websocket: %s'%notif)
        message = json.dumps(notif)
        await ws.send_message(message)
        return 'OK'

    while True:
        event_arrived = netapi.poll(timeout=2)
        if event_arrived:
            notif = netapi.recv()
            result = await on_notification(notif)
            netapi.reply_notif(result)
        await trio.sleep(0.01)

async def server_start(netapi, storage):
    PORT = 3032
    async def on_connect(request):
        log.debug("new connection to ws path %s"%request.url)
        user_id = 0
        try:
            ws = await request.accept()
            message = await ws.get_message()
            try:
                json.loads(message)
            except Exception as e:
                log.error("Ser error %s"%e)
                await ws.aclose(1008,reason="auth")
                return
            token = json.loads(message).get('token')
            user_id = storage.sessman.check_token(token)
            ####
            ###@@@@ DEBUG
            if token=='machine':
                user_id=1
            print(user_id)
            if not user_id:
                # invalid user
                log.error("ws token not found %s"%token)
                await ws.aclose(1008,reason="auth")
                return

            log.info("got new websock connection from id %s"%user_id)
            storage.add_connection(ws,user_id)
            while True:
                message = await ws.get_message()
                log.info("got new message from id %s"%user_id)
                ###
                msg = json.loads(message)
                msg['user_id'] = user_id
                netapi.send(msg)
                await trio.sleep(0)

        except ConnectionClosed:
            if user_id:
                storage.remove_connection(user_id)
            log.info("websocket user %s ended connection"%user_id)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(listen_for_notif, netapi,storage)
        log.info("starting websocket")
        await serve_websocket(on_connect, '127.0.0.1', PORT,
                              handler_nursery=nursery, ssl_context=None)

def init_net_api(netconf):
    appid = 'websocket'
    name = 'websocket'
    return NetworkAPI(netconf, appid, name)

def main():
    netconf = get_network_config()
    storage = Storage()
    netapi = init_net_api(netconf)
    #trio.run(server_start, netapi, storage, instruments=[Tracer()])
    trio.run(server_start, netapi, storage)

if __name__=="__main__":
    main()
