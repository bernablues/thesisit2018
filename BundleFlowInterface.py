import logging
from SDTNLogger import SDTNLogger

class BundleFlowInterface:

    def __init__(self, sock, toAddress=None):
        self.BFI_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')
        self.BFI_logger.classLog('Initializing BFI...', 'INFO')

        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

        self.BFI_logger.classLog('BFI initialized: to_addr: ' + str(self.toAddress) + ' sock: ' + str(self.sock) + ' port: ' + str(self.port), 'INFO')

    def sendBundle(self, bundle):

        # self.BFI_logger.classLog('Sending', bundle.toString(), 'to addr: (%s) port: (%s)', self.toAddress, self.port)
        self.BFI_logger.classLog('Sending ' + bundle.toString() + ' to addr: ' + str(self.toAddress) + ' port: ' + str(self.port), 'INFO')
        self.BFI_logger.classLog('', 'INFO')
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
        self.BFI_logger.classLog('Bundle sent successfully.', 'INFO')

    def receiveBundle(self, timeout=None):

        self.BFI_logger.classLog('Receiving bundle...', 'INFO')
        if timeout:
            self.sock.settimeout(timeout)
            self.BFI_logger.classLog('Setting timeout: ' + str(timeout), 'INFO')

        try:
            bundle, fromAddress = self.sock.recvfrom(1024)
            self.BFI_logger.classLog('Bundle ' + bundle + ' received from ' + str(fromAddress), 'INFO')

        except:
            self.BFI_logger.classLog('No bundle received.', 'WARNING')
            return None

        if timeout:
            self.sock.settimeout(None)
            self.BFI_logger.classLog('Setting timeout: ' + str(timeout), 'INFO')

        return bundle, fromAddress

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.classLog('Setting to_addr: ' + str(toAddress), 'INFO')
