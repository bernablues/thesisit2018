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

class Station:

    def __init__(self, experiments=None):
        self.station_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')    
        self.station_logger.classLog('Initializing station...', 'INFO')

        self.SID = 1
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'thesisit'
        self.DATABASE_COLUMNS = ['timestamp', 'seq_number', 'data']

        self.conman = ConnectionManager(5, 'wlan0', 5000, 10000)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        self.dataMan = DataManager(1000, DataManager.DROP_FIRST_PROTOCOL, self.dbi, 5)
        self.dataFactory = DataFactory(1, 1, self.SID, self.dataMan)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = None

        self.currentSeq = 1

        self.station_logger.classLog('Station Mule initialized:,SID:,' + str(self.SID) + ',DATA_PORT:,' + str(self.DATA_PORT) + ',HELLO_PORT:,' + str(self.HELLO_PORT), 'INFO')


    def sendNext(self):

        data = self.dataMan.getData(True)
        dataBundle = self.appendHeaders(1, data)
        bundle = Bundle(dataBundle)
        self.bfi.sendBundle(bundle)
        return bundle
        

    def appendHeaders(self, bundleType, data):
        headers = (bundleType, self.currentSeq, self.SID)
        bundleData = (headers, data)
        return bundleData

    def redirect(self, bundle):
        self.station_logger.classLog('Redirecting bundle...', 'INFO')
        if bundle.getType() == 0:
            if self.currentSeq == bundle.getSeq():
                self.sendNext()
            else:
                pass
                # resend(bundle)
        else:
            pass

    def checkConnection(self):
        self.station_logger.classLog('Checking connection...', 'INFO')
        if not self.conman.isConnected():
            self.conman.listenForHello()
            self.bfi = BundleFlowInterface(self.dataSocket, self.conman.getConnectedTo())
            receiveBundle = self.sendReceiveBundle()
            bundle = self.expectAck(receiveBundle)
        else:
            return True

    def resendBundle(self, bundle):
        self.station_logger.classLog('Resending bundle...', 'INFO')
        self.bfi.sendBundle(bundle)

    def expectAck(self, bundle):
        self.station_logger.classLog('Expecting ACK...', 'INFO')
        terminated = False
        while not terminated:
            bundleData = self.bfi.receiveBundle(3)
            fromAddress = bundleData[1]
            bundleData = bundleData[0]

            if not bundleData:
                self.resendBundle(bundle)
                terminated = self.conman.acknowledgementTimeout()
            else:
                if bundleData.split()[0] == '0':
                    self.currentSeq += 1
                    return bundle
                else:
                    continue
    
    def sendReceiveBundle(self):
        self.station_logger.classLog('Sending Receive Bundle...', 'INFO')
        bundleData = '3 ' + ' 0 ' + ' x ' + ' x' #does not work when two headers only
        bundle = Bundle(bundleData)
        self.bfi.sendBundle(bundle)
        return bundle

    def acknowledge(self, bundle):
        self.station_logger.classLog('Acknowledging bundle...', 'INFO')
        bundleData = '0 ' + str(bundle.getSeq()) + ' x ' + ' x' #does not work when two headers only
        ack = Bundle(bundleData)
        self.bfi.sendBundle(ack)

    def start(self):
        self.station_logger.classLog('Starting station miodule...', 'INFO')
        while True:
            self.checkConnection()
            time.sleep(2)
            try:
                bundleData, fromSocket = self.bfi.receiveBundle()
                fromAddress, fromPort = fromSocket
                self.bfi.setToAddress(fromAddress)
                bundle = Bundle(bundleData)

                data = self.dataMan.sliceData(bundle.toData()[1])
                for each in data:
                    self.dataMan.insertData(each)
                self.acknowledge(bundle)


            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print "Not reachable"
                self.station_logger.classLog('Not reachable...', 'WARNING')


def main():
    station = Station()

    station.start()
    
def test():
    print "TEST MODE"

if __name__ == "__main__":
    main()