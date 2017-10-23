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
import logging
from SDTNLogger import SDTNLogger

class Mule:

    def __init__(self, experiments=None):
        self.mule_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')    
        self.mule_logger.classLog('Initializing mule...', 'INFO')

        self.SID = 0
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'password'
        self.DATABASE_COLUMNS = ['timestamp', 'seq_number', 'data']

        self.conman = ConnectionManager(5, 'wlan0', 5000, 10000, experiments)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS, experiments)
        self.dataMan = DataManager(1000, DataManager.DROP_FIRST_PROTOCOL, self.dbi, 5, experiments)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = BundleFlowInterface(self.dataSocket)

        self.currentSeq = 1

        self.mule_logger.classLog('Mule initialized:,SID:,' + str(self.SID) + ',DATA_PORT:,' + str(self.DATA_PORT) + ',HELLO_PORT:,' + str(self.HELLO_PORT), 'INFO')

    def resendBundle(self, bundle):
        self.mule_logger.classLog('Resending bundle...', 'INFO')
        self.bfi.sendBundle(bundle)

    def acknowledge(self, bundle):
        self.mule_logger.classLog('Acknowledging bundle...', 'INFO')
        bundleData = '0 ' + str(bundle.getSeq()) + ' x ' + ' x' #does not work when two headers only
        ack = Bundle(bundleData)
        self.bfi.sendBundle(ack)

    def appendHeaders(self, bundleType, data):
        self.mule_logger.classLog('Appending headers...', 'INFO')
        headers = (bundleType, self.currentSeq, self.SID)
        bundleData = (headers, data)
        return bundleData

    def sendNext(self):
        self.mule_logger.classLog('Sending next bundle...', 'INFO')
        data = self.dataMan.getData(True)
        dataBundle = self.appendHeaders(1, data)
        bundle = Bundle(dataBundle)
        print bundle.toString()
        self.bfi.sendBundle(bundle)
        return bundle

    def expectAck(self, bundle):
        self.mule_logger.classLog('Expecting ACK...', 'INFO')
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
        self.mule_logger.classLog('Checking connection...', 'INFO')
        return self.conman.isConnected()

    def start(self):
        self.mule_logger.classLog('Starting mule....', 'INFO')
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
                self.mule_logger.classLog('Keyboard interrupted. Terminating from mule.', 'INFO')
                print "Keyboard interrupted. Terminating from mule." 
                break
            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print "Not reachable"
                self.mule_logger.classLog('Keyboard interrupted. Terminating from mule.', 'WARNING')

def main():
    mule = Mule()

    helloFactoryThread = mule.conman.startHelloThread()

    mule.start()
    
def test():
    print "TEST MODE"

if __name__ == "__main__":
    main()