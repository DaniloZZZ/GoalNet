import trio

def ws_req_rep(usl, message):
    message = trio.run(make_request, url, json.dumps(message))
    notif = json.loads(message)
    return notif

async def make_request(url,message):
    try:
        async with open_websocket_url(url) as ws:
            await ws.send_message(message)
            message = await ws.get_message()
            logging.info('Received message: %s', message)
            return message
    except OSError as ose:
        logging.error('Connection attempt failed: %s', ose)
