import trio, json
from trio_websocket import open_websocket_url
import logging

def ws_req_rep(url, message):
    if isinstance(message,list):
        message = trio.run(several_reqs, url, message)
    else:
        message = trio.run(make_request, url, json.dumps(message))
    notif = json.loads(message)
    return notif

async def several_reqs(url, msgs):
    try:
        async with open_websocket_url(url) as ws:
            for m in msgs:
                await ws.send_message(json.dumps(m))
            message = await ws.get_message()
            return message
    except OSError as ose:
        logging.error('Connection attempt failed: %s', ose)

async def make_request(url,message):
    try:
        async with open_websocket_url(url) as ws:
            await ws.send_message(message)
            message = await ws.get_message()
            return message
    except OSError as ose:
        logging.error('Connection attempt failed: %s', ose)
