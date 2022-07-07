import logging
import sys
from flask import Flask, redirect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import gravity as gravity
import elevate as elevate
import ftl as ftl
import macvendor as macvendor
import auth as auth

dns = Flask(__name__)
cors = CORS(dns, resources={r"/api/*": {"origins": "*"}})

def configure_logging():
    # register root logging
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    # create formatter and add it to the handlers
    file_handler = logging.FileHandler(filename='app.log')
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )



""" @dns.route("/")
def index():
    return render_template("index.html") """



'''Swagger Blueprint'''
SWAGGER_URL = '/api'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Pi-Hole DNS",
        'validatorUrl': "none"
    }
)

dns.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
dns.register_blueprint(auth.authentication)
dns.register_blueprint(elevate.elevate)
dns.register_blueprint(gravity.gravity)
dns.register_blueprint(ftl.ftl)
dns.register_blueprint(macvendor.macvendor)

@dns.route("/")
def index():
    return redirect('/api')

if __name__ == '__main__':
    from waitress import serve
    configure_logging()
    serve(dns, host="127.0.0.1", port=5000)

