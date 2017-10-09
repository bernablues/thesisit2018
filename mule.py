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
        self.SID = 1
        self.DATA_PORT = 10000
        self.HELLO_PORT = 5000

        self.TABLE_NAME = 'sensor_data'
        self.DATABASE_NAME = 'sdtn'
        self.MYSQL_USER = 'sdtn'
        self.MYSQL_PASSWORD = 'password'

        self.conman = ConnectionManager(5, 'wlan0', 5000, 10000)
        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD)
        self.dataMan = DataManager(1000, DataManager.DROP_FIRST_PROTOCOL, self.dbi)
        self.dataSocket = self.conman.getDataSocket()
        self.bfi = BundleFlowInterface(self.dataSocket)

    def resendBundle(self, bundle):
        self.bfi.sendBundle(bundle)

    def expectAck(self, bundle):
        terminated = False
        while not terminated:
            bundle = self.bfi.receiveBundle(1)
            if not bundle:
                terminated = self.conman.acknowledgementTimeout()
                self.resendBundle(bundle)
            else:
                if bundle.split()[0] == '0':
                    return bundle
                else:
                    continue

    def acknowledge(self, bundle):
        bundleData = '0 ' + str(bundle.getSeq()) + ' x ' + ' x' #does not work when two headers only
        ack = Bundle(bundleData)
        self.bfi.sendBundle(ack)

    def start(self):
        while True:
            try:
                bundleData, fromSocket = self.bfi.receiveBundle()
                fromAddress, fromPort = fromSocket
                self.bfi.setToAddress(fromAddress)
                bundle = Bundle(bundleData)
                print bundle.toString()
                self.dataMan.insertData(bundle.toData())
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