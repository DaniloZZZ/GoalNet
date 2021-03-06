from flask import Flask, request, jsonify, redirect,make_response
from flask_cors import CORS
import json

from goalnet.utils import get_network_config
from goalnet.core.database.api import with_db_api
import logging as log
from .. import NetworkAPI
app = Flask("login app")
CORS(app)
FLASK_PORT = 8919

@with_db_api
class NetworkAPIDB(NetworkAPI):
    pass

APP_PAGE = 'http://localhost:8080'
LOGIN_PAGE = 'http://localhost:8080/login'

def show_the_login_form():
    return "Login form"


def start_app(netapi):
    @app.route('/', methods=['GET'])
    def main_page():
        def get_cookie_token(request):
            return request.cookies.get("token")
        token = get_cookie_token(request)
        if token:
            user = netapi.user_by_token(token)
            log.warn("user for token '%s': %s"%(token,user))
            if not user:
                return redirect(LOGIN_PAGE, 302)
            return redirect(APP_PAGE, 302)
        else:
            return redirect(LOGIN_PAGE, 302)

    @app.route('/login',methods=["GET","POST"])
    def login_page():
        if request.method == 'POST':
            js_request = False
            if len(request.data)>0:
                log.debug("got from json")
                form = json.loads(request.data)
                js_request=True
            else:
                form = request.form
                log.debug("trying to read form")
            try:
                email = form['email']
                pwd = form['pwd']
            except KeyError as e:
                return "auth err",401
            hash = lambda x:x #this is temporary
            pwd = hash(pwd)

            netapi.send({'action':'add.user.auth','email':email,'pwd_hash':pwd})
            doc = {}
            # Temorary patch
            while not doc.get('token'):
                doc = netapi.recv()
                log.debug("Received %s"%doc)
                netapi.reply_notif("OK")
            log.debug("got doc %s"%doc)
            token = doc['token']
            if js_request:
                response = make_response(jsonify({'token':token}))
            else:
                response = make_response(redirect(APP_PAGE, 302))
            header = response.headers
            header['Access-Control-Allow-Origin'] = '*'
            response.set_cookie('token', token)
            return response
        else:
            return show_the_login_form()

def init_net_api(netconf):
    appid = 'login'
    name = 'login'
    return NetworkAPIDB(netconf, appid, name)

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


