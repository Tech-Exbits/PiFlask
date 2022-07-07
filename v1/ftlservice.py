from database import getData
import socket
import sys
import logging

log = logging.getLogger(__name__)
localaddress = "127.0.0.1"
defaultport = 4711


def getDefaultFTLConfig():
    abspath = sys.argv[0]
    abspath = abspath.split('v1')[0]
    dbconfig = open(abspath+"ftl.config")
    records = []
    for line in dbconfig.readlines():
        array = line.strip().split("  ")
        if len(array) == 3:
            array.pop(1)
        array[0] = array[0].lower()
        records.append(array)
    dbconfig.close()
    records = dict(records)
    records['maxnetage'] = records['maxdbdays']
    return records


def getCurrentFTLConfig():
    data = getData("pihole-FTL.conf", "=", True)
    return dict(data)


def getFullFTLConfig():
    defaultConfig = getDefaultFTLConfig()
    currentConfig = getCurrentFTLConfig()
    fullConfig = defaultConfig.copy()
    for key in currentConfig:
        fullConfig[key] = currentConfig[key]
    return fullConfig


def sendRequestToFTL(message='<stats', splitter=' ', address=localaddress, port=defaultport):
    data = ""
    config = getFullFTLConfig()
    if message != '':
        try:
            if address == localaddress:
                port = config['ftlport']
            connsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connsocket.connect((address, int(port)))
            log.info("Connected To FTLDNS...........Attempting to send message")
            connsocket.sendall(message.encode('utf-8'))
        
            while True:
                response = connsocket.recv(1500)
                print(response)
                log.info(response)
                if '---EOM---' in response.decode('utf-8'):
                    data = response.decode('utf-8').replace('---EOM---', '').strip()
                    data = convertStrtoArray(data, splitter)
                    log.info("Message received.......")
                    break
        except: 
            log.info("Error connecting to FTLDNS %s", sys.exc_info())
        finally:
            log.info("Closing the connection......")
            connsocket.close()
    return data


def convertStrtoArray(str, splitter):
    array = []
    for line in str.splitlines():
        line = line.strip()
        if line != "":
            line = line.split(splitter)
            i = 0
            for value in line:
                value = value.strip()
                line[i] = value
                i=i+1
            array.append(line)
    return array

