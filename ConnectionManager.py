import socket
import fcntl
import struct
import threading
import time
from Bundle import Bundle
from BundleFlowInterface import BundleFlowInterface

from DatabaseInterface import DatabaseInterface

class ConnectionManager:
    def __init__(self, maxAckTimeout, ifname, helloPort, dataPort, dataMan = None, dataToBundleSize = 5, experiments=None):
        self.dataToBundleSize = dataToBundleSize

        self.maxAckTimeout = maxAckTimeout
        self.currentAckTimeout = 0

        self.helloPort = helloPort
        self.dataPort = dataPort
        self.ownIpAddress = self.__getOwnIpAddress(ifname)

        self.dataSocket = None
        self.helloSocket = None
        self.__initializeSockets()

        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')
        self.helloDataman = dataMan

        self.routingDbi = DatabaseInterface('routing_table', 'sdtn', 'sdtn', 'password', ['bundle_seq', 'sensor_id', 'sent_to'])

        self.connected = False
        self.connectedTo = False


    def __getOwnIpAddress(self, ifname):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def __createSocket(self, address, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        return sock
    
    def __createDataSocket(self):
        return self.__createSocket(self.ownIpAddress, self.dataPort)

    def __createHelloSocket(self):
        return self.__createSocket('', self.helloPort)

    def __resetHelloSocket(self):
        self.helloSocket.close()
        self.helloSocket = self.__createHelloSocket()
    
    def __resetHelloBundleFlowInterface(self):
        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')

    def __initializeSockets(self):
        self.dataSocket = self.__createDataSocket()
        self.helloSocket = self.__createHelloSocket()
        self.__emptyHelloSocket()

    def __initializeConnection(self, address):
        self.currentAckTimeout = 0
        self.connected = True
        self.connectedTo = address
        return True

    def __terminateConnection(self):
        self.connected = False
        self.connectedTo = False
        self.__emptyHelloSocket()
        # THIS WILL BE A PROBLEM WHEN THERE ARE MULTIPLE HELLO BROADCAST IN RANGE
        # self.__resetHelloSocket()
        # self.__resetHelloBundleFlowInterface()

    def getDataSocket(self):
        return self.dataSocket

    def getHelloSocket(self):
        return self.helloSocket

    def getConnectedTo(self):
        return self.connectedTo

    def isConnected(self):
        return self.connected

    def __sync(self, bundleData, fromSocket):
        # check table using received ip address from hello
        # check for bundle seq x SID that has already been sent to that ip address
        # send unsent bundles to received ip address
        routingRows = self.routingDbi.getAllRows()
        allBundles  = self.helloDataman.getAllData()
        fromAddress = fromSocket[0]
        bundlesToSend = []
        bundleFilter = []

        for row in routingRows:
            if row[2] == fromAddress:
                bundleFilter.append((row[0], row[1]))
        
        for bundle in allBundles:
            sendBundle = True
            if bundle[4] == '1':
                # this filters bundles
                continue
            if not bundleFilter:
                bundlesToSend = allBundles
                break
            for filterItem in bundleFilter:
                if not bundle in bundlesToSend and filterItem[0] == bundle[1] and filterItem[1] == bundle[2]:
                    sendBundle = False
            if sendBundle:
                bundlesToSend.append(bundle)
                
        
        print bundlesToSend
        if bundlesToSend:
            for bundle in bundlesToSend:
                headers = (bundle[0], bundle[1], bundle[2])
                tempBundle = Bundle((headers, (bundle[3])))
                self.helloSocket.sendto(tempBundle.toString(), (fromAddress, self.dataPort))
                self.routingDbi.insertRow([str(bundle[1]), str(bundle[2]), fromAddress])
                print "Sending: " + tempBundle.toString()

        # old sync 
        # sequenceNumbers = set(bundleData[1:].split(' '))
        # ownSequenceNumbers = set(self.helloDataman.getDataMap())
        # dataToSync = list(ownSequenceNumbers - sequenceNumbers)

        # if dataToSync:
        #     bundle = Bundle(((1,-1,-1),self.helloDataman.getAllData(dataToSync[:self.dataToBundleSize])))
        #     self.helloSocket.sendto(bundle.toString(), (fromSocket[0], self.dataPort))
        #     print "SENDING: " + bundle.toString()

    def listenForHello(self, syncMode=False):
        print "Listening for hello..."

        if syncMode:
            while True:
                bundleData, fromSocket = self.helloBundleFlowInterface.receiveBundle()
                fromAddress, fromPort = fromSocket
                if fromAddress == self.ownIpAddress:
                    continue

                self.__sync(bundleData, fromSocket)

        bundleData, fromSocket = self.helloBundleFlowInterface.receiveBundle()
        fromAddress, fromPort = fromSocket 
        
        # print "Received hello:", bundleData, 'from', fromAddress
        self.__initializeConnection(fromAddress)

    def __buildHello(self):
        return "2" + ' '.join(self.helloDataman.getDataMap())

    def __sendHello(self, sock):

        while True:
            time.sleep(1)
            helloMessage = self.__buildHello()
            # Make this parametizable
            sock.sendto(helloMessage, ('172.24.1.255', self.helloPort))
            # print "HELLO: " + helloMessage

    def __emptyHelloSocket(self):
        # problematic
        self.helloSocket.settimeout(0.001)
        while True:
            try:
                self.helloSocket.recvfrom(4)
            except:
                break
        self.helloSocket.settimeout(None)

    def __initializeHelloThread(self):
        helloSocket = self.getHelloSocket()
        helloSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        thread = threading.Thread(target=self.__sendHello, args=(helloSocket,))
        thread.daemon = True

        print "Initialized hello thread."
        return thread


    def startHelloThread(self):
        helloThread = self.__initializeHelloThread()

        helloThread.start()
        print "Started hello thread."
        return helloThread

    def acknowledgementTimeout(self):
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            print 'Max ack timeout reached. Terminating connection...'
            self.__terminateConnection()
            return True
        else:
            return False

    def initializeConnection(self, bundle, address):
        self.__initializeConnection(address)
        return True

    def terminateConnection(self):
        self.__terminateConnection()
        return True