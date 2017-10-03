import socket
import fcntl
import struct
from BundleFlowInterface import BundleFlowInterface

class ConnectionManager:
    def __init__(self, maxAckTimeout, ifname, helloPort, dataPort):
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

    def __initializeSockets(self):
        self.dataSocket = self.__createDataSocket()
        self.helloSocket = self.__createHelloSocket()

    def __initializeConnection(self, address):
        self.currentAckTimeout = 0
        self.connected = True
        self.connectedTo = address
        return True

    def __terminateConnection(self):
        self.connected = False
        self.connectedTo = False
        self.__resetHelloSocket()

    def getDataSocket(self):
        return self.dataSocket

    def getHelloSocket(self):
        return self.helloSocket

    def getConnectedTo(self):
        return self.connectedTo

    def isConnected(self):
        return self.connected

    def listenForHello(self):
        print "Listening for hello..."
        bundleData, fromSocket = self.helloBundleFlowInterface.receiveBundle()
        fromAddress, fromPort = fromSocket
        print "Received hello:", bundleData, 'from', fromAddress
        self.__initializeConnection(fromAddress)

    def acknowledgementTimeout(self):
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            print 'Max ack timeout reached. Terminating connection...'
            self.__terminateConnection()
            return True
        else:
            return False
