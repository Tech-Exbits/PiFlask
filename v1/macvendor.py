import sqlite3
import logging
from flask import Blueprint, request, jsonify
from database import connectDB
from database import fullpath
from database import closeDB
from auth import isAPIKeyValid

log = logging.getLogger(__name__)
macvendor = Blueprint('macvendor', __name__)
database = "macvendor.db"


@macvendor.route('/api/v1/vendors', methods=['GET'])
def getVendors():
    result = {
        'message': 'failure'
    }
    if isAPIKeyValid(request.headers.get('X-API-Key')):
        db = connectDB(fullpath(database))
        log.info("getVendors() Called.........")
        if db:
            try:
                cursor = db.cursor()
                query = "SELECT * from `macvendor`;"
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
