import socket
import fcntl
import struct

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

    def __getOwnIpAddress(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    
    def __initializeSockets(self):
        self.dataSocket = self.__createSocket(self.ownIpAddress, self.dataPort)
        self.helloSocket = self.__createSocket('', self.helloPort)
        
    def __createSocket(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        return sock

    def getDataSocket(self):
        return self.dataSocket

    def getHelloSocket(self):
        return self.helloSocket

    def listenForHello(self):
        print "Listening for hello..."
        data, addr = self.helloSocket.recvfrom(4)
        print "Received hello:", data, 'from', addr
        return addr

    def acknowledgementTimeout(self):
        self.currentAckTimeout += 1
        if self.currentAckTimeout == self.maxAckTimeout:
            return True
        else:
            return False
