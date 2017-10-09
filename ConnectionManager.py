import socket
import fcntl
import struct
import threading
import time
from BundleFlowInterface import BundleFlowInterface

import logging

class ConnectionManager:

    logging.basicConfig(level=logging.DEBUG)

    ConMan_logger = logging.getLogger(__name__)
    ConMan_logger.setLevel(logging.INFO)

    ConMan_handler = logging.FileHandler(__name__)
    ConMan_handler.setLevel(logging.INFO)

    ConMan_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ConMan_handler.setFormatter(ConMan_formatter)

    ConMan_logger.addHandler(ConMan_handler)


    def __init__(self, maxAckTimeout, ifname, helloPort, dataPort):
        self.ConMan_logger.info('Initializing ConMan...')

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

        self.ConMan_logger.info('ConMan initialized: max_ack_timeout: %s hello_port: %s data_port: %s own_IP_addr: %s ')

    def __getOwnIpAddress(self, ifname):
        self.ConMan_logger.info('Getting own IP addr...')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def __createSocket(self, address, port):
        self.ConMan_logger.info('Creating socket...')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        self.ConMan_logger.info('Created socket at addr: %s and port: %s', address, port)
        return sock
    
    def __createDataSocket(self):
        self.ConMan_logger.info('Creating data socket...')
        return self.__createSocket(self.ownIpAddress, self.dataPort)

    def __createHelloSocket(self):
        self.ConMan_logger.info('Creating hello socket...')
        return self.__createSocket('', self.helloPort)

    def __resetHelloSocket(self):
        self.ConMan_logger.info('Resetting hello socket...')
        self.helloSocket.close()
        self.helloSocket = self.__createHelloSocket()
    
    def __resetHelloBundleFlowInterface(self):
        self.ConMan_logger.info('Ressetting HelloBFI...')
        self.helloBundleFlowInterface = BundleFlowInterface(self.helloSocket, '')

    def __initializeSockets(self):
        self.ConMan_logger.info('Initializing sockets...')
        self.dataSocket = self.__createDataSocket()
        self.helloSocket = self.__createHelloSocket()

    def __initializeConnection(self, address):
        self.ConMan_logger.info('Initializing connection...')
        self.currentAckTimeout = 0
        self.connected = True
        self.connectedTo = address
        return True

    def __terminateConnection(self):
        self.ConMan_logger.info('Terminating connection...')
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
        self.ConMan_logger.info('Listening for hello...')
        print "Listening for hello..."
        bundleData, fromSocket = self.helloBundleFlowInterface.receiveBundle()
        fromAddress, fromPort = fromSocket
        self.ConMan_logger.info("Received hello: %s", bundleData, 'from %s', fromAddress)
        print "Received hello:", bundleData, 'from', fromAddress
        self.__initializeConnection(fromAddress)

    def __sendHello(self, sock):

        self.ConMan_logger.info('Sending hello message...')
        helloMessage = "2"

        while True:
            time.sleep(1)
            # Make this parametizable
            sock.sendto(helloMessage, ('172.24.1.255', self.helloPort))
            self.ConMan_logger.info('Sent hello message to 172.24.1.255')

    def __initializeHelloThread(self):
        self.ConMan_logger.info('Initializing hello thread...')
        helloSocket = self.getHelloSocket()
        helloSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        thread = threading.Thread(target=self.__sendHello, args=(helloSocket,))
        thread.daemon = True

        self.ConMan_logger.info('Hello thread initialized: Hello socket: %s', helloSocket)
        print "Initialized hello thread."
        return thread


    def startHelloThread(self):
        self.ConMan_logger.info('Starting hello thread...')
        helloThread = self.__initializeHelloThread()

        helloThread.start()
        self.ConMan_logger.info('Hello thread started.')        
        print "Started hello thread."
        return helloThread

    def acknowledgementTimeout(self):
        self.ConMan_logger.info('Ack timeout occured.')   
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            self.ConMan_logger.warning('Max ack timeout reached.')
            print 'Max ack timeout reached. Terminating connection...'
            self.__terminateConnection()
            return True
        else:
            return False
