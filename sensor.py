import os
import sys
import time
import threading
import yaml
from DataFactory import DataFactory
from DatabaseInterface import DatabaseInterface
from ConnectionManager import ConnectionManager
from BundleFlowInterface import BundleFlowInterface
from DataManager import DataManager   
from Bundle import Bundle

class Sensor:

    def __init__(self,experiments=None):
        with open("sensor_config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.SID = cfg['SENSOR_ID']
        self.DATA_PORT = cfg['DATA_PORT']
        self.HELLO_PORT = cfg['HELLO_PORT']

        self.TABLE_NAME = cfg['MYSQL']['TABLE_NAME']
        self.DATABASE_NAME = cfg['MYSQL']['DATABASE_NAME']
        self.MYSQL_USER = cfg['MYSQL']['USER']
        self.MYSQL_PASSWORD = cfg['MYSQL']['PASSWORD']
        self.DATABASE_COLUMNS = cfg['MYSQL']['COLUMNS']


        self.conman = ConnectionManager(cfg['MAX_ACK_TIMEOUT'], cfg['WIRELESS_INTERFACE'], self.HELLO_PORT, self.DATA_PORT)

        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        self.dataMan = DataManager(cfg['MAX_DATA_ENTRIES'], cfg['DROPPING_PROTOCOL'], self.dbi, cfg['DATA_TO_BUNDLE_SIZE'])
        self.dataFactory = DataFactory(cfg['DATA_GENERATED_SIZE'], cfg['TIME_TO_GENERATE_DATA'], self.SID, self.dataMan)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = None

        self.currentSeq = 1

    def getDataSummary(self, dataBundle):
        data = dataBundle[1]
        numbers = []


        for i in range(len(data)):
            numbers.append(int(data[i][2]))

        ave = sum(numbers)/len(numbers)
        minData = min(numbers)
        maxData = max(numbers)

        return (ave, minData, maxData)

    def sendNext(self):
        data = self.dataMan.getData()
        dataBundle = self.appendHeaders(1, data)
        dataSummary = self.getDataSummary(dataBundle)
        dataBundle = (dataBundle[0], dataBundle[1], dataSummary)
        bundle = Bundle(dataBundle)
        self.bfi.sendBundle(bundle)
        return bundle

    def appendHeaders(self, bundleType, data):
        headers = (bundleType, self.currentSeq, self.SID)
        bundleData = (headers, data)
        return bundleData

    def redirect(self, bundle):
        if bundle.getType() == 0:
            if self.currentSeq == bundle.getSeq():
                self.sendNext()
            else:
                pass
                # resend(bundle)
        else:
            pass

    def checkConnection(self):
        if not self.conman.isConnected():
            self.conman.listenForHello()
            self.bfi = BundleFlowInterface(self.dataSocket, self.conman.getConnectedTo())
        else:
            return True

    def resendBundle(self, bundle):

        self.bfi.sendBundle(bundle)

    def expectAck(self, bundle):

        terminated = False
        while not terminated:
            bundleData = self.bfi.receiveBundle(3)

            if not bundleData[0]:
                self.resendBundle(bundle)
                terminated = self.conman.acknowledgementTimeout()
            else:
                self.dataMan.getData(True)
                fromAddress = bundleData[1]
                bundleData = bundleData[0]
                if bundleData.split()[0] == '0':
                    self.currentSeq += 1
                    return bundle
                else:
                    continue

    def start(self):
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
