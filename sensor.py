import os
import sys
import time
import threading
from DataFactory import DataFactory
from DatabaseInterface import DatabaseInterface
from ConnectionManager import ConnectionManager
from BundleFlowInterface import BundleFlowInterface
from DataManager import DataManager   

SID = 1
DATA_PORT = 10000
HELLO_PORT = 5000

TABLE_NAME = 'generated_sensor_data'
DATABASE_NAME = 'sdtn'
MYSQL_USER = 'sdtn'
MYSQL_PASSWORD = 'thesisit'

currentSeq = 1

conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)
dbi = DatabaseInterface(TABLE_NAME, DATABASE_NAME, MYSQL_USER, MYSQL_PASSWORD)
dataMan = DataManager(10, DataManager.DROP_CURRENT_PROTOCOL, dbi)
dataFactory = DataFactory(5, 1, SID, dataMan)
dataSocket = conman.getDataSocket()

def confirmAcknowledgement(sock, message, bfi):
    terminated = False
    data = False
    while True:
        bundle = bfi.receiveBundle(2)
        if bundle:
            terminated = conman.acknowledgementTimeout()

        if terminated:
            return False
        elif bundle:
            break
        else:
            bfi.sendBundle(message)
        
    print "Received message:", bundle
    bundle = bundle.split()
    ackSeq = int(bundle[1])
    pType = int(bundle[0])
    print "Message is Type:", pType, "Seq:", ackSeq, "\n"

    if pType != 0:
        return False
    elif ackSeq != message[0]:
        return False
    else:
        return True

def sendNext():
    pass
def redirect(bundle):
    if bundle.getType == 0:
        if currentSeq == bundle.getSeq():
            sendNext()
        else:
            pass
            # resend(bundle)
    else:
        pass

def start():
    pass

def main():
    dataFactoryThread = threading.Thread(target=dataFactory.start, args=())
    dataFactoryThread.daemon = True
    dataFactoryThread.start()
    
    while True:
        if not conman.isConnected():
            conman.listenForHello()
            bfi = BundleFlowInterface(dataSocket, conman.getConnectedTo())
        time.sleep(2)
        try:
            pass
            # message = dbi.getData(1)
            # dbi.deleteData(1)
            # seq, payload = message[0]
            # bundle = str(seq) + ' 1 X ' + payload
            # bfi.sendBundle(bundle)
            # confirmAcknowledgement(dataSocket, bundle, bfi)
        
        except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
            print "Not reachable"
    
def test():
    print "TEST MODE"

if __name__ == "__main__":
    main()