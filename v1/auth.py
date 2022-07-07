import hashlib
import logging
import datetime
import secrets
import string
import jwt
from flask import Blueprint, request, jsonify
from database import connectDB, getPyConfig
from database import fullpath
from database import closeDB
from database import getData

log = logging.getLogger(__name__)
authentication = Blueprint('authentication', __name__)
database = "setupVars.conf"
clients = []

@authentication.route('/api/v1/signin', methods=['POST'])
def Signin():
    result = {
        'message': 'failure'
    }
    
    if isPasswordValid(request.args.get('password')):
        result['message'] = 'success'
        result['token'] = generateToken()
    else: 
        return jsonify(result), 401
    return jsonify(result)


@authentication.route('/api/v1/signout', methods=['POST'])
def Signout():
    result = {
        'message': 'failure'
    }
    
    if isTokenValid(request.args.get('token')):
        result['message'] = 'success'
    else: 
        return jsonify(result), 401
    return jsonify(result)


def isPasswordValid(password):
    if password != "" and password != None:
        db = dict(getData(database, "=", True))
        dbhashpassword = db['webpassword']
        hashpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hashpassword = hashlib.sha256(hashpassword.encode('utf-8')).hexdigest()
        if(hashpassword == dbhashpassword):
            return True
        else:
            return False
    else:
        return False


def isAPIKeyValid(password):
    if password != "" and password != None:
        db = dict(getData(database, "=", True))
        dbhashpassword = db['webpassword']
        # Token can also be used as API key
        if(password == dbhashpassword or isTokenValid(password)):
            return True
        else:
            return False
    else:
        return False


def isTokenValid(token):
    decodedValue = decodetoken(token)
    if isinstance(decodedValue, dict):
        if decodedValue['appId'] in clients:
            return True
        else:
            return False
    else:
        return False


def generateToken():
    # ct stores current time
    ct = datetime.datetime.now() + datetime.timedelta(minutes = 30)
    
    # ts store timestamp of current time
    ts = ct.timestamp()

    # generate application id
    appId = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(50))
    clients.append(appId)
    options = {"appId": appId, "exp": ts, "iat": datetime.datetime.now().timestamp()}
    encoded = jwt.encode(options, getPyConfig()['jwt-secret'], algorithm="HS256")
    return encoded


def decodetoken(token):
    decoded = ""
    try:
        decoded = jwt.decode(token, getPyConfig()['jwt-secret'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError as error:
        log.info("Token has been expired....")
    return decoded

    
