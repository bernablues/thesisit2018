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
import logging
from SDTNLogger import SDTNLogger
from FlowManager import FlowManager

class Mule:

    def __init__(self, experiments=None):
        with open("mule_config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.mule_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')    
        self.mule_logger.classLog('Initializing mule...', 'INFO')

        self.SID = cfg['SENSOR_ID']
        self.DATA_PORT = cfg['DATA_PORT']
        self.HELLO_PORT = cfg['HELLO_PORT']

        self.TABLE_NAME = cfg['MYSQL']['TABLE_NAME']
        self.DATABASE_NAME = cfg['MYSQL']['DATABASE_NAME']
        self.MYSQL_USER = cfg['MYSQL']['USER']
        self.MYSQL_PASSWORD = cfg['MYSQL']['PASSWORD']
        self.DATABASE_COLUMNS = cfg['MYSQL']['COLUMNS']

        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        self.dataMan = DataManager(cfg['MAX_DATA_ENTRIES'], cfg['DROPPING_PROTOCOL'], self.dbi, cfg['DATA_TO_BUNDLE_SIZE'])
        self.conman = ConnectionManager(cfg['MAX_ACK_TIMEOUT'], cfg['WIRELESS_INTERFACE'], self.HELLO_PORT, self.DATA_PORT, self.dataMan, cfg['DATA_TO_BUNDLE_SIZE'])

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
        data = self.dataMan.getBundle(True)
        if not data:
            self.conman.terminateConnection()
            return data
        bundle = Bundle(data)
        self.bfi.sendBundle(bundle)
        return bundle

    def expectAck(self, bundle):
        self.mule_logger.classLog('Expecting ACK...', 'INFO')
        terminated = False
        while not terminated:

            bundleData = self.bfi.receiveBundle(3)

            if not bundleData[0]:
                self.resendBundle(bundle)
                terminated = self.conman.acknowledgementTimeout()
            else:
                fromAddress = bundleData[1]
                bundleData = bundleData[0]
                print "Current SEQ" + self.currentSeq
                if bundleData.split()[0] == '0' and bundleData.split()[1] == self.currentSeq:
                    print "Acked"
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

                bundleData=[bundle.getType(), bundle.getSeq(), bundle.getSID(), fromAddress, ""]
                print "Bundle headers:", bundleData

                match_flowTable=[['1', '1', '4', '1', '172.24.1.226', '', '1'], ['2', bundle.getType(), bundle.getSeq(), bundle.getSID(), fromAddress, "", '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
                noMatch_flowTable=[['1', '1', '4', '1', '172.24.1.2', '', '1'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
                flowManager = FlowManager(bundleData, match_flowTable)
                # flowManager = flowManager(bundleData, noMatch_flowTable)
                print "Flow Table"
                print ""
                print(flowManager.getFlowTable())

                print ""
                print(flowManager.flowMatching())


                #refactor to function
                if bundle.getType() == '3':
                    self.acknowledge(bundle)

                    #create two states for connection if got bundleType = 3 and to passively data if got bundleType = 1
                    self.conman.initializeConnection(bundle, fromAddress)
                    while self.checkConnection():
                        nextBundle = self.sendNext()
                        self.currentSeq = nextBundle.getSeq()
                        if nextBundle:
                            self.expectAck(nextBundle)
                elif bundle.getType() == '1':
                    self.dataMan.insertData(bundle.toString().split())
                    # insert metadata on other table
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
    thread = threading.Thread(target=mule.conman.listenForHello, args=(True,))
    thread.daemon = True

    thread.start()
    mule.start()
    
def test():
    print "TEST MODE"
    mule = Mule()

if __name__ == "__main__":
    main()