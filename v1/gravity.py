import sqlite3
import logging
from flask import Blueprint, request, jsonify
from database import connectDB
from database import fullpath
from database import closeDB
from database import getData
from auth import isAPIKeyValid


log = logging.getLogger(__name__)
gravity = Blueprint('gravity', __name__)
database = "gravity.db"


@gravity.route('/api/v1/adlist', methods=['GET'])
def getAdList():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getAdList() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `adlist`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['adlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/adlist/group', methods=['GET'])
def getAdListByGroup():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getAdListByGroup() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `adlist_by_group`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['groupadlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/whitelist', methods=['GET'])
def getWhiteAdList():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getWhiteAdList() Called.........")
        if db:
            try:
                cursor = db.cursor()
                urlListquery = "SELECT * from `vw_whitelist`;"
                cursor.execute(urlListquery)
                urlList = cursor.fetchall()
                regexListquery = "SELECT * from `vw_regex_whitelist`;"
                cursor.execute(regexListquery)
                regexList = cursor.fetchall()
                result['whitelist'] = urlList + regexList
                result['message'] = 'success'
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


@gravity.route('/api/v1/blacklist', methods=['GET'])
def getBlackAdList():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getBlackAdList() Called.........")
        if db:
            try:
                cursor = db.cursor()
                urlListquery = "SELECT * from `vw_blacklist`;"
                cursor.execute(urlListquery)
                urlList = cursor.fetchall()
                regexListquery = "SELECT * from `vw_regex_blacklist`;"
                cursor.execute(regexListquery)
                regexList = cursor.fetchall()
                result['blacklist'] = urlList + regexList
                result['message'] = 'success'
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


@gravity.route('/api/v1/clients', methods=['GET'])
def getClients():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getClients() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `client`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['clientlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/clients/group', methods=['GET'])
def getClientsByGroup():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getClientsByGroup() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `client_by_group`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['groupclientlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/domain/audit', methods=['GET'])
def getDomainAudit():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getDomainAudit() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `domain_audit`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['auditlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/domains', methods=['GET'])
def getDomains():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getDomains() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `domainlist`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['domainlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/domains/group', methods=['GET'])
def getDomainsByGroup():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getDomainsByGroup() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `domainlist_by_group`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['vendorlist'] = cursor.fetchall()
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


@gravity.route('/api/v1/gravity', methods=['GET'])
def getGravity():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getGravity() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `gravity`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['gravitylist'] = cursor.fetchall()
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


@gravity.route('/api/v1/groups', methods=['GET'])
def getGroups():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getGroups() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `group`;"
                cursor.execute(query)
                result['message'] = 'success'
                result['grouplist'] = cursor.fetchall()
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


@gravity.route('/api/v1/info', methods=['GET'])
def getInfo():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getInfo() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from info;"
                cursor.execute(query)
                result['message'] = 'success'
                result['dns-info'] = cursor.fetchall() + getData("setupVars.conf", "=", True)
                result['dns-servers'] = getData("dns-servers.conf", ";", False)
                array = getData("dhcp.leases", " ", False)
                del array[array.__len__()-1]
                result['dhcp-leases'] = array
                result["dns-records"] = getData("local.list", " ", False) + getData("custom.list", " ", False)
                result["local-dns-version"] = getData("localversions", " ", False)
                result["github-dns-version"] = getData("GitHubVersions", " ", False)
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


@gravity.route('/api/v1/views/<string:type>', methods=['GET'])
def getViews(type):
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        if type == 'adlist' or type == 'blacklist' or type == 'whitelist' or type == 'regex_blacklist' or type == 'regex_whitelist' or type == 'gravity':
            query = "SELECT * from `vw_"+type+"`;"
            db = connectDB(fullpath(database))
            log.info("getViews(%s) Called.........", type)
            if db:
                try:
                    cursor = db.cursor()
                    cursor.execute(query)
                    result['message'] = 'success'
                    result['data'] = cursor.fetchall()
                    cursor.close()
                except sqlite3.Error as error:
                    log.info('Error while connecting to SQLite: %s', error)
                finally:
                    closeDB(db)
            else: 
                return jsonify(result), 500
        else:
            return jsonify(result), 404
    else: 
        return jsonify(result), 401
    return jsonify(result)
