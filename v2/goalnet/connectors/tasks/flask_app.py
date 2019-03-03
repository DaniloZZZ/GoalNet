
from flask import Flask, request
app = Flask(__name__)
FLASK_PORT = 8991
db = None


@app.route("/new_task")
def new_task():
    args = request.args
    try:
        uid = args['user_id']
        name = args['name']
        start= args['start']
        end= args['end']
    except Exception as e:
        return "FAIL:nokey"
        print("no key",e)
    task = {
            'name':name,
            'start':start,
            'end':end,
            'user_id':uid,
            }
    print('nw task', task)

    if db:
        db.new_task(uid,task)
        return "OK:"+str(uid)
    else:
        return "FAIL:nodb"

@app.route("/get_status")
def metrics():
    args = request.args
    try:
        uid = args['user_id']
        uid = args['at']
    except Exception as e:
        return "FAIL:nokey"
        print("no key",e)
    metrics = db.get_task_metrics(uid)
    return met
    if at:
        try:
            at = float(at)
        except Exception as e:
            return "FAIL:wrongkey"
            return str(metrics[at])
    return "NULL"

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
