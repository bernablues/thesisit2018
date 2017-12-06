import socket
import fcntl
import struct
import threading
import time
from Bundle import Bundle
from BundleFlowInterface import BundleFlowInterface
import logging
from SDTNLogger import SDTNLogger

class ConnectionManager:
    def __init__(self, maxAckTimeout, ifname, helloPort, dataPort, dataMan = None, dataToBundleSize = 5, experiments=None):
        self.ConMan_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.ConMan_logger.classLog('Initializing ConMan...', 'INFO')

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

        self.connected = False
        self.connectedTo = False

        self.ConMan_logger.classLog('ConMan initialized:,MAX_ACK-TIMEOUT:,' + str(maxAckTimeout) + ',hello_port:,' + str(helloPort) + ',data_port:,' + str(dataPort) + ',own_IP_addr:,' + str(self.ownIpAddress), 'INFO')

    def __getOwnIpAddress(self, ifname):
        self.ConMan_logger.classLog('Getting own IP addr...', 'INFO')

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def __createSocket(self, address, port):
        self.ConMan_logger.classLog('Creating socket...', 'INFO')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        self.ConMan_logger.classLog('Created socket:,ADDR:,' + str(address) + ',PORT:,' + str(port), 'INFO')
        return sock
    
    def __createDataSocket(self):
        self.ConMan_logger.classLog('Creating data socket...', 'INFO')
        return self.__createSocket(self.ownIpAddress, self.dataPort)

    def __createHelloSocket(self):
        self.ConMan_logger.classLog('Creating hello socket...', 'INFO')
        return self.__createSocket('', self.helloPort)

    def __resetHelloSocket(self):
        self.ConMan_logger.classLog('Resetting hello socket...', 'INFO')
        self.helloSocket.close()
        self.helloSocket = self.__createHelloSocket()
    
    def __resetHelloBundleFlowInterface(self):
        self.ConMan_logger.classLog('Resetting HelloBFI...', 'INFO')
        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')

    def __initializeSockets(self):
        self.ConMan_logger.classLog('Initializing sockets...', 'INFO')
        self.dataSocket = self.__createDataSocket()
        self.helloSocket = self.__createHelloSocket()
        self.__emptyHelloSocket()

    def __initializeConnection(self, address):
        self.ConMan_logger.classLog('Initializing connection...', 'INFO')
        self.currentAckTimeout = 0
        self.connected = True
        self.connectedTo = address
        return True

    def __terminateConnection(self):
        self.ConMan_logger.classLog('Terminating connection...', 'INFO')
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
        sequenceNumbers = set(bundleData[1:].split(' '))
        ownSequenceNumbers = set(self.helloDataman.getDataMap())
        dataToSync = list(ownSequenceNumbers - sequenceNumbers)
        print "Received SEQ_NUM " + str(sequenceNumbers)
        print "Own SEQ_NUM: " + str(ownSequenceNumbers)
        print "DATA TO SEND: " + str(dataToSync)

        if dataToSync:
            bundle = Bundle(((1,-1,-1),self.helloDataman.getAllData(dataToSync[:self.dataToBundleSize])))
            self.helloSocket.sendto(bundle.toString(), (fromSocket[0], self.dataPort))
            print "SENDING: " + bundle.toString()

    def listenForHello(self, syncMode=False):
        self.ConMan_logger.classLog('Listening for hello...', 'INFO')
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
        
        self.ConMan_logger.classLog('Received hello:,bundleData:,' + bundleData + ',from ADDR:,' + str(fromAddress), 'INFO')
        # print "Received hello:", bundleData, 'from', fromAddress
        self.__initializeConnection(fromAddress)

    def __buildHello(self):
        return "2" + ' '.join(self.helloDataman.getDataMap())

    def __sendHello(self, sock):
        self.ConMan_logger.classLog('Sending hello message...', 'INFO')

        while True:
            time.sleep(1)
            helloMessage = self.__buildHello()
            # Make this parametizable
            sock.sendto(helloMessage, ('172.24.1.255', self.helloPort))
            # print "HELLO: " + helloMessage
            self.ConMan_logger.classLog('Sent hello message to 172.24.1.255', 'INFO')

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
        self.ConMan_logger.classLog('Initializing hello thread...', 'INFO')
        helloSocket = self.getHelloSocket()
        helloSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        thread = threading.Thread(target=self.__sendHello, args=(helloSocket,))
        thread.daemon = True

        self.ConMan_logger.classLog('Hello thread initialized:,Hello socket:,' + str(helloSocket), 'INFO')
        print "Initialized hello thread."
        return thread


    def startHelloThread(self):
        self.ConMan_logger.classLog('Starting hello thread...', 'INFO')
        helloThread = self.__initializeHelloThread()

        helloThread.start()
        self.ConMan_logger.classLog('Hello thread started.', 'INFO')        
        print "Started hello thread."
        return helloThread

    def acknowledgementTimeout(self):
        self.ConMan_logger.classLog('Ack timeout:,OCCURRED.', 'INFO')   
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            self.ConMan_logger.classLog('Ack timeout:,MAX ACK TIMEOUT REACHED.', 'WARNING')
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