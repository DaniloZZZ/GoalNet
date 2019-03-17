from flask import Flask, request, jsonify
from goalnet.utils import get_network_config
from .. import NetworkAPI
app = Flask("login app")
FLASK_PORT = 8919

def show_the_login_form():
    return "Login form"

def start_app(netapi):
    @app.route('/',methods=["GET","POST"])
    def login_page():
        if request.method == 'POST':
            email = request.form['email']
            pwd = request.form['pwd_hash']

            netapi.send({'action':'add.user.auth','email':email,'pwd_hash':pwd})
            doc = netapi.recv()
            netapi.reply_notif("OK")
            return jsonify(doc)
        else:
            return show_the_login_form()

def init_net_api(netconf):
    appid = 'login'
    name = 'login'
    return NetworkAPI(netconf, appid, name)

def main():
    netconf = get_network_config()
    netapi = init_net_api(netconf)
    start_app(netapi)
    app.run(
            host='0.0.0.0',
            port=FLASK_PORT,
            debug=True,
            use_reloader=False,
            )


