import sqlite3
import logging
from flask import Blueprint, request, jsonify
from database import connectDB
from database import fullpath
from database import closeDB
from auth import isAPIKeyValid
from ftlservice import sendRequestToFTL

log = logging.getLogger(__name__)
ftl = Blueprint('ftl', __name__)
database = "pihole-FTL.db"


@ftl.route('/api/v1/aliases', methods=['GET'])
def getAliasClient():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getAliasClient() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `aliasclient`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['aliaslist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
            return jsonify(result), 500
    else:
        return jsonify(result), 401
    return jsonify(result)


@ftl.route('/api/v1/counters', methods=['GET'])
def getCounters():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getCounters() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `counters`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['counterlist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
            return jsonify(result), 500
    else: 
        return jsonify(result), 401
    return jsonify(result)


@ftl.route('/api/v1/ftl/<string:type>', methods=['GET'])
@ftl.route('/api/v1/ftl/<string:type>/<string:subtype>', methods=['GET'])
def getFTL(type, subtype=""):
    log.info("getFTL() Called.........")
    message = '>'
    response = ''
    auth = False
    result = {
        'message': 'failure'
    }
    
    if isAPIKeyValid(request.headers.get('X-API-Key')) :
        auth = True
    else:
        auth = False

    if type == 'stats':
        message = message + 'stats'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'dbstats':
        message = message + 'dbstats'
        response = sendRequestToFTL(message, ":")
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'version' and auth:
        message = message + 'version'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'cacheinfo' and auth:
        message = message + 'cacheinfo'
        response = sendRequestToFTL(message, ':')
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'clientid' and auth:
        message = message + 'clientID'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'blocked' and auth:
        message = message + 'recentBlocked'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'overtime':
        message = message + 'overTime'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                response.pop(0)
                response.insert(0, ['timestamp', 'domain-overtime', 'ads-overtime'])
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'querytypes-overtime':
        message = message + 'QueryTypesoverTime'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'clients-overtime':
        message = message + 'ClientsoverTime'
        response = sendRequestToFTL(message)
        headers = sendRequestToFTL('>top-clients')
        if len(response) > 0 and len(headers) > 0:
                response.pop(0)
                headarray = ["timestamp"]
                for header in headers:
                    name = header[3]
                    ip = header[2]
                    headarray.append(name + " <" + ip + ">") 
                response.insert(0, headarray)
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'domain' and auth:
        message = message + 'domain '+subtype
        response = sendRequestToFTL(message, ':')
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'top-domains' and auth:
        if subtype == 'audit':
            message = message + 'top-domains for audit'
            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500
        else:
            message = message + 'top-domains'
            if request.args.get('topItems'):
                message = message + ' (' + request.args.get('topItems') + ')'

            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500

    elif type == 'top-ads' and auth:
        if subtype == 'audit':
            message = message + 'top-ads for audit'
            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500
        else:
            message = message + 'top-ads'
            if request.args.get('topItems'):
                message = message + ' (' + request.args.get('topItems') + ')'

            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500

    elif type == 'top-clients' and auth:
        if subtype == 'blocked':
            message = message + 'top-clients blocked'
            if request.args.get('topClientsBlocked'):
                message = message + ' (' + request.args.get('topClientsBlocked') + ')'

            response = sendRequestToFTL(message)
            if len(response) > 0:
                newresponse = []
                for item in response:
                    newresponse.append([item[3], item[2], item[1]])
                response = newresponse
                response.insert(0, ['client-name', 'ip-addr', 'total-calls'])
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500
        else:
            message = message + 'top-clients'
            if request.args.get('topClients'):
                message = message + ' (' + request.args.get('topClients') + ')'
            if request.args.get('getQuerySources'):
                message = message + ' (' + request.args.get('getQuerySources') + ')'

            response = sendRequestToFTL(message)
            if len(response) > 0:
                newresponse = []
                for item in response:
                    newresponse.append([item[3], item[2], item[1]])
                response = newresponse
                response.insert(0, ['client-name', 'ip-addr', 'total-calls'])
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500

    elif type == 'client-names' and auth:
        message = message + 'client-names'
        response = sendRequestToFTL(message)
        if len(response) > 0:
            result['response'] = response
            result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'forward-dest' and auth:
        if subtype == 'unsorted':
            message = message + 'forward-dest unsorted'
            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500
        else:
            message = message + 'forward-dest'
            response = sendRequestToFTL(message)
            if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
            else:
                return jsonify(result), 500

    elif type == 'forward-names' and auth:
        message = message + 'forward-names'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'querytypes' and auth:
        message = message + 'querytypes'
        response = sendRequestToFTL(message, ':')
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'getallqueries' and auth:
        message = message + 'getallqueries'
        if subtype == 'time' and request.args.get('from') and request.args.get('to'):
            message = message + '-time ' + request.args.get('from') + ' ' + request.args.get('to')
        
        elif subtype == 'domain' and request.args.get('domain'):
            message = message + '-domain ' + request.args.get('domain')
        
        elif subtype == 'client' and request.args.get('client'):
            message = message + '-client ' + request.args.get('client')
        
        elif subtype == 'client-blocked' and request.args.get('client'):
            message = message + '-client-blocked ' + request.args.get('client')
        
        elif subtype == 'qtype' and request.args.get('querytype'):
            message = message + '-qtype ' + request.args.get('querytype')
        
        elif subtype == 'forward' and request.args.get('forwarddest'):
            message = message + '-forward ' + request.args.get('forwarddest')
        
        else:
            if request.args.get('getAllQueries'):
                message = message + ' (' + request.args.get('getAllQueries') + ')'

        
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    elif type == 'delete-lease' and auth:
        message = message + 'delete-lease'
        response = sendRequestToFTL(message)
        if len(response) > 0:
                result['response'] = response
                result['message'] = 'success'
        else:
            return jsonify(result), 500

    else:
        return jsonify(result), 404
    
    return jsonify(result)
    

@ftl.route('/api/v1/messages', methods=['GET'])
def getMessages():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getMessages() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `message`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['messagelist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
            return jsonify(result), 500
    else: 
        return jsonify(result), 401
    return jsonify(result)


@ftl.route('/api/v1/networks', methods=['GET'])
def getNetwork():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getNetwork() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `network`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['networklist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
                return jsonify(result), 500
    else: 
        return jsonify(result), 401
    return jsonify(result)


@ftl.route('/api/v1/addresses', methods=['GET'])
def getAddresses():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getAddresses() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `network_addresses`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['addresslist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
            return jsonify(result), 500
    else: 
        return jsonify(result), 401
    return jsonify(result)


@ftl.route('/api/v1/queries', methods=['GET'])
def getQueries():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getQueries() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `queries`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['querylist'] = cursor.fetchall()
                cursor.close()
            except sqlite3.Error as error:
                log.info('Error while connecting to SQLite: %s', error)
            finally:
                closeDB(db)
        else:
            return jsonify(result), 500
    else: 
        return jsonify(result), 401
    return jsonify(result)

