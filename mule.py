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
from FlowManager import FlowManager

class Mule:

    def __init__(self, experiments=None):
        with open("mule_config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.SID = cfg['SENSOR_ID']
        self.DATA_PORT = cfg['DATA_PORT']
        self.HELLO_PORT = cfg['HELLO_PORT']

        self.TABLE_NAME = cfg['MYSQL']['TABLE_NAME']
        self.DATABASE_NAME = cfg['MYSQL']['DATABASE_NAME']
        self.MYSQL_USER = cfg['MYSQL']['USER']
        self.MYSQL_PASSWORD = cfg['MYSQL']['PASSWORD']
        self.DATABASE_COLUMNS = cfg['MYSQL']['COLUMNS']

        self.dbi = DatabaseInterface(self.TABLE_NAME, self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, self.DATABASE_COLUMNS)
        # self.routingDbi = DatabaseInterface('routing_table', self.DATABASE_NAME, self.MYSQL_USER, self.MYSQL_PASSWORD, ['bundle_seq', 'sensor_id', 'sent_to'])
        self.dataMan = DataManager(cfg['MAX_DATA_ENTRIES'], cfg['DROPPING_PROTOCOL'], self.dbi, cfg['DATA_TO_BUNDLE_SIZE'])
        self.conman = ConnectionManager(cfg['MAX_ACK_TIMEOUT'], cfg['WIRELESS_INTERFACE'], self.HELLO_PORT, self.DATA_PORT, self.dataMan, cfg['DATA_TO_BUNDLE_SIZE'])

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
        data = self.dataMan.getBundle()
        if not data:
            self.conman.terminateConnection()
            return data
        bundle = Bundle(data)
        self.bfi.sendBundle(bundle)
        return bundle

    def expectAck(self, bundle):
        terminated = False
        while not terminated:

            bundleData = self.bfi.receiveBundle(3)

            if not bundleData[0]:
                self.resendBundle(bundle)
                terminated = self.conman.acknowledgementTimeout()
            else:
                self.dataMan.getBundle(True)
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
        return self.conman.isConnected()

    def start(self):
        while True:
            try:
                bundleData, fromSocket = self.bfi.receiveBundle()
                fromAddress, fromPort = fromSocket
                self.bfi.setToAddress(fromAddress)
                bundle = Bundle(bundleData)
                # flowTable=[['*', '*', '*', '*', '172.24.1.10', '', '0'], ['*', '*', '*', '*', '172.24.1.1', '', '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
                # flowManager = FlowManager(flowTable)

                # data = [bundle.getType(), bundle.getSeq(), bundle.getSID(), fromAddress, '']

                # action = flowManager.matchFlow(data)
                # print "matched action: " + action
                # if action == '0':
                #     continue
                # else:
                #     bundle.setAction(action)

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
                    data = bundle.toString().split()
                    data.append('2')
                    self.dataMan.insertData(data)
                    # insert metadata on other table
                    self.acknowledge(bundle)

            except KeyboardInterrupt:
                print "Keyboard interrupted. Terminating from mule." 
                break
            except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
                print sys.exc_info()

def main():
    mule = Mule()

    helloFactoryThread = mule.conman.startHelloThread()
    thread = threading.Thread(target=mule.conman.listenForHello, args=(True,))
    thread.daemon = True

    thread.start()
    mule.start()
    
def test():
    print "TEST MODE"
    # mule = Mule()
    bundleJSON = {'type':'1' , 'bundleSeq':'4', 'sid':'1', 'ipAddr':'172.24.1.3'}

    flowManager.packetIn(bundleJSON)
    flowManager.sync()

if __name__ == "__main__":
    main()