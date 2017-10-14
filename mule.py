import os
import sys
import time
import threading
from DataFactory import DataFactory
from DatabaseInterface import DatabaseInterface
from ConnectionManager import ConnectionManager
from BundleFlowInterface import BundleFlowInterface
from DataManager import DataManager   
from Bundle import Bundle

class Mule:

    def __init__(self):
        self.SID = 0
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'password'
        self.DATABASE_COLUMNS = ['timestamp', 'seq_number', 'data']

        self.conman = ConnectionManager(5, 'wlan0', 5000, 10000)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        self.dataMan = DataManager(1000, DataManager.DROP_FIRST_PROTOCOL, self.dbi, 5)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = BundleFlowInterface(self.dataSocket)

        self.currentSeq = 1

    def resendBundle(self, bundle):
        self.bfi.sendBundle(bundle)

    def acknowledge(self, bundle):
        bundleData = '0 ' + str(bundle.getSeq()) + ' x ' + ' x' #does not work when two headers only
        ack = Bundle(bundleData)
        self.bfi.sendBundle(ack)

    def appendHeaders(self, bundleType, data):
        headers = (bundleType, self.currentSeq, self.SID)
        bundleData = (headers, data)
        return bundleData

    def sendNext(self):
        data = self.dataMan.getData(True)
        dataBundle = self.appendHeaders(1, data)
        bundle = Bundle(dataBundle)
        print bundle.toString()
        self.bfi.sendBundle(bundle)
        return bundle

    def expectAck(self, bundle):
        terminated = False
        while not terminated:

            bundleData = self.bfi.receiveBundle(3)

            if not bundleData:
                self.resendBundle(bundle)
                terminated = self.conman.acknowledgementTimeout()
            else:
                fromAddress = bundleData[1]
                bundleData = bundleData[0]
                if bundleData.split()[0] == '0':
                    self.currentSeq += 1
                    return bundle
                else:
                    continue
        
        return False

    def checkConnection(self):
        return self.conman.isConnected()

    def start(self):
        while True:
            try:
                bundleData, fromSocket = self.bfi.receiveBundle()
                fromAddress, fromPort = fromSocket
                self.bfi.setToAddress(fromAddress)
                bundle = Bundle(bundleData)

                #refactor to function
                if bundle.getType() == '3':
                    self.acknowledge(bundle)

                    #create two states for connection if got bundleType = 3 and to passively data if got bundleType = 1
                    self.conman.initializeConnection(bundle, fromAddress)
                    while self.checkConnection():
                        self.sendNext()
                        self.expectAck(bundle)
                elif bundle.getType() == '1':
                    data = self.dataMan.sliceData(bundle.toData()[1])
                    for each in data:
                        self.dataMan.insertData(each)
                    self.acknowledge(bundle)

            except KeyboardInterrupt:
                print "Keyboard interrupted. Terminating from mule." 
                break
            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print "Not reachable"

def main():
    mule = Mule()

    helloFactoryThread = mule.conman.startHelloThread()

    mule.start()
    
def test():
    print "TEST MODE"

if __name__ == "__main__":
    main()