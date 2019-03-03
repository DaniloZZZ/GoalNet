from flask import Flask, request
app = Flask(__name__)
FLASK_PORT = 8990
db = None

@app.route("/vkauth")
def vkauth():
    args = request.args
    token = args['access_token']
    vkid = args['user_id']
    print('token:', token)
    print('id:', vkid)
    return "vkauth"

@app.route("/new_auth")
def new_auth():
    args = request.args
    try:
        token = args['access_token']
        uid = args['user_id']
        vkid = args['vk_user_id']
    except Exception as e:
        return "FAIL:nokey"
        print("no key",e)
    print('token:', token)
    print('id:', vkid)
    if db:
        db.new_user(uid,token)
        return "OK:"+str(uid)
    else:
        return "FAIL:nodb"

@app.route("/online")
def metrics():
    args = request.args
    try:
        uid = args['user_id']
    except Exception as e:
        return "FAIL:nokey"
        print("no key",e)
    start = args.get('start')
    end = args.get('end')
    step = args.get('step')
    db.update_metrics()
    metrics = db.get_online_metrics(uid)
    if start and end:
        try:
            start = float(start)
            end = float(end)
        except Exception as e:
            return "FAIL:wrongkey"
        if step:
            try:
                step = float(step)
            except Exception as e:
                return "FAIL:wrongkey"
            if (end-start)/step>2000:
                return "FAIL:toomuch"
            return str(metrics[start:end:step])
        return str(metrics[start:end])
    return str(metrics.fix_to_down(metrics.data))

@app.route("/")
def root():
    return "Vk sleep connector running"
@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

def start_app(db_):
    global db
    db = db_
    app.run(
            host='0.0.0.0',
            port=FLASK_PORT,
            debug=True,
            use_reloader=False,
            )
