import sqlite3
import logging
import sys
log = logging.getLogger(__name__)

'''
...............Depricated..............
def fullpath(dbfile):
    abspath = sys.argv[0]
    abspath = abspath.split('v1')[0]
    path = open(abspath+"default.config")
    dir = path.read()
    dbpath = dir + dbfile
    return dbpath
'''

def fullpath(dbfile):
    records = getPyConfig()
    dbpath = records['path'] + dbfile
    return dbpath


def getPyConfig():
    abspath = sys.argv[0]
    abspath = abspath.split('v1')[0]
    path = open(abspath+"default.config")
    records = []
    for line in path.readlines():
        array = line.strip().split("  ")
        array[0] = array[0].lower()
        records.append(array)
    path.close()
    records = dict(records)
    return records


def getData(file, splitter, lower):
    records = []
    config = open(fullpath(file))
    for line in config.readlines():
        array = line.strip().split(splitter)
        if lower:
            array[0] = array[0].lower()
        records.append(array)
    config.close()
    return records


def connectDB(dbpath):
    dbinstance = None
    try:
        dbinstance = sqlite3.connect(dbpath)
        log.info('Database Connected..........')
    except sqlite3.Error as error:
        log.info('Error while connecting to SQLite: %s', error)
    return dbinstance


def closeDB(db):
    if db:
        db.commit()
        db.close()
        log.info('Database Connection Closed.........')
    else:
        log.info('Cannot Close Connection..........')

