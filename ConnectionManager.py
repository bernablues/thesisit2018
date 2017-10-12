import socket
import fcntl
import struct
import threading
import time
import logging
from BundleFlowInterface import BundleFlowInterface
from SDTNLogger import SDTNLogger

class ConnectionManager:

    def __init__(self, maxAckTimeout, ifname, helloPort, dataPort):

        self.ConMan_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')
        self.ConMan_logger.classLog('Initializing ConMan...', 'INFO')

        self.maxAckTimeout = maxAckTimeout
        self.currentAckTimeout = 0

        self.helloPort = helloPort
        self.dataPort = dataPort
        self.ownIpAddress = self.__getOwnIpAddress(ifname)

        self.dataSocket = None
        self.helloSocket = None
        self.__initializeSockets()

        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')

        self.connected = False
        self.connectedTo = False

        self.ConMan_logger.classLog('ConMan initialized: max_ack_timeout: ' + str(maxAckTimeout) + ' hello_port: ' + str(helloPort) + ' data_port: ' + ' own_IP_addr: ' + self.ownIpAddress, 'INFO')

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
        self.ConMan_logger.classLog('Created socket at addr: ' + str(address) + ' and port: ' + str(port), 'INFO')
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
        self.ConMan_logger.classLog('Ressetting HelloBFI...', 'INFO')
        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')

    def __initializeSockets(self):
        self.ConMan_logger.classLog('Initializing sockets...', 'INFO')
        self.dataSocket = self.__createDataSocket()
        self.helloSocket = self.__createHelloSocket()

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
        self.__resetHelloSocket()
        self.__resetHelloBundleFlowInterface()

    def getDataSocket(self):
        return self.dataSocket

    def getHelloSocket(self):
        return self.helloSocket

    def getConnectedTo(self):
        return self.connectedTo

    def isConnected(self):
        return self.connected

    def listenForHello(self):
        self.ConMan_logger.classLog('Listening for hello...', 'INFO')
        print "Listening for hello..."
        bundleData, fromSocket = self.helloBundleFlowInterface.receiveBundle()
        fromAddress, fromPort = fromSocket
        self.ConMan_logger.classLog('Received hello: ' + bundleData + ' from ' + str(fromAddress), 'INFO')
        print "Received hello:", bundleData, 'from', fromAddress
        self.__initializeConnection(fromAddress)

    def __sendHello(self, sock):

        self.ConMan_logger.classLog('Sending hello message...', 'INFO')
        helloMessage = "2"

        while True:
            time.sleep(1)
            # Make this parametizable
            sock.sendto(helloMessage, ('172.24.1.255', self.helloPort))
            self.ConMan_logger.classLog('Sent hello message to 172.24.1.255', 'INFO')

    def __initializeHelloThread(self):
        self.ConMan_logger.classLog('Initializing hello thread...', 'INFO')
        helloSocket = self.getHelloSocket()
        helloSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        thread = threading.Thread(target=self.__sendHello, args=(helloSocket,))
        thread.daemon = True

        self.ConMan_logger.classLog('Hello thread initialized: Hello socket: ' + str(helloSocket), 'INFO')
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
        self.ConMan_logger.classLog('Ack timeout occured.', 'INFO')   
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            self.ConMan_logger.classLog('Max ack timeout reached.', 'WARNING')
            print 'Max ack timeout reached. Terminating connection...'
            self.__terminateConnection()
            return True
        else:
            return False
