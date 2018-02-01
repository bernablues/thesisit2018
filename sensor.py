import os
import sys
import time
import threading
# import yaml
from DataFactory import DataFactory
from DatabaseInterface import DatabaseInterface
from ConnectionManager import ConnectionManager
from BundleFlowInterface import BundleFlowInterface
from DataManager import DataManager   
from Bundle import Bundle
import logging
from SDTNLogger import SDTNLogger

class Sensor:

    def __init__(self,experiments=None):
        # with open("sensor_config.yaml", 'r') as ymlfile:
        #     cfg = yaml.load(ymlfile)
        self.sensor_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.sensor_logger.classLog('Initializing sensor...', 'INFO')

        self.sendDataTable_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')    
        self.sendDataTable_logger.classLog('Initializing sensor...', 'INFO')

        self.SID = 1
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'password'
        self.DATABASE_COLUMNS = ['timestamp', 'seq_number', 'data']

        self.conman = ConnectionManager(5, 'wlp2s0', self.HELLO_PORT, self.DATA_PORT)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        self.dataMan = DataManager(20, 0, self.dbi, 5)
        self.dataFactory = DataFactory(1, 1, self.SID, self.dataMan)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = None

        self.currentSeq = 1

        self.sensor_logger.classLog('Sensor initialized:,SID:,' + str(self.SID) + ',DATA_PORT:,' + str(self.DATA_PORT) + ',HELLO_PORT:,' + str(self.HELLO_PORT), 'INFO')

    def sendNext(self):
        self.sensor_logger.classLog('Sending next bundle...', 'INFO')
        self.sendDataTable_logger.classLog('Sending next bundle...', 'INFO')

        data = self.dataMan.getData(True)
        dataBundle = self.appendHeaders(1, data)
        bundle = Bundle(dataBundle)
        self.bfi.sendBundle(bundle)
        return bundle

    def appendHeaders(self, bundleType, data):
        self.sensor_logger.classLog('Appending headers...', 'INFO')
        headers = (bundleType, self.currentSeq, self.SID)
        bundleData = (headers, data)
        return bundleData

    def redirect(self, bundle):
        self.sensor_logger.classLog('Redirecting bundles...', 'INFO')
        if bundle.getType() == 0:
            if self.currentSeq == bundle.getSeq():
                self.sendNext()
            else:
                pass
                # resend(bundle)
        else:
            pass

    def checkConnection(self):
        self.sensor_logger.classLog('Checking connection...', 'INFO')
        if not self.conman.isConnected():
            self.conman.listenForHello()
            self.bfi = BundleFlowInterface(self.dataSocket, self.conman.getConnectedTo())
        else:
            return True

    def resendBundle(self, bundle):
        self.sensor_logger.classLog('Resending bundle...', 'INFO')
        self.sendDataTable_logger.classLog('Resending bundle...', 'INFO')

        self.bfi.sendBundle(bundle)

    def expectAck(self, bundle):
        self.sensor_logger.classLog('Expecting ACK...', 'INFO')
        self.sendDataTable_logger.classLog('Expecting ACK...', 'INFO')

        terminated = False
        while not terminated:
            bundleData = self.bfi.receiveBundle(3)

            if not bundleData[0]:
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

    def start(self):
        self.sensor_logger.classLog('Sensor module starting...', 'INFO')
        # packetsPassed = 0
        # start = time.time()
        while True:
            self.checkConnection()
            time.sleep(2)
            try:
                bundle = self.sendNext()
                self.expectAck(bundle)
                # packetsPassed += 1

            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print "Not reachable"
            self.sensor_logger.classLog('Not reachable...', 'WARNING')

        # end = time.time()
        # timeElapsed = end-start
        # print "Time elapsed:", str(timeElapsed)
        # print "Packets sent:", str(packetsPassed)
        # bandwidth = 902 * packetsPassed / timeElapsed
        # print "Bandwidth:", str(bandwidth)
def main():
    sensor = Sensor()
    dataFactoryThread = threading.Thread(target=sensor.dataFactory.start, args=())
    dataFactoryThread.daemon = True
    dataFactoryThread.start()

    sensor.start()
    
def test():
    print "TEST MODE"
    sensor = Sensor()
    print "Created Sensor"

if __name__ == "__main__":
    main()
