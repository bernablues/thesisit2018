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

class Sensor:

    def __init__(self):
        self.SID = 1
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'generated_sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'thesisit'

        self.conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD)
        self.dataMan = DataManager(10, DataManager.DROP_FIRST_PROTOCOL, self.dbi)
        self.dataFactory = DataFactory(5, 1, self.SID, self.dataMan)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = None

        self.currentSeq = 1

    def sendNext(self):
        data = self.dataMan.getData(1, True)[0]
        dataBundle = self.appendHeaders(1, data)
        bundle = Bundle(dataBundle)
        self.bfi.sendBundle(bundle)
        return bundle
        

    def appendHeaders(self, bundleType, bundleData):
        headers = (bundleType, self.currentSeq)
        bundle = headers + bundleData
        return bundle

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
            bundleData = self.bfi.receiveBundle(1)
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

    def start(self):
        while True:
            self.checkConnection()
            time.sleep(2)
            try:
                bundle = self.sendNext()
                self.expectAck(bundle)

            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print "Not reachable"
                self.conman.acknowledgementTimeout()

def main():
    sensor = Sensor()
    dataFactoryThread = threading.Thread(target=sensor.dataFactory.start, args=())
    dataFactoryThread.daemon = True
    dataFactoryThread.start()

    sensor.start()
    
def test():
    print "TEST MODE"

if __name__ == "__main__":
    main()