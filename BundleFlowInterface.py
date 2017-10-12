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
<<<<<<< HEAD
        # print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        # print ""
=======

        # self.BFI_logger.classLog('Sending', bundle.toString(), 'to addr: (%s) port: (%s)', self.toAddress, self.port)
        self.BFI_logger.classLog('Sending ' + bundle.toString() + ' to addr: ' + str(self.toAddress) + ' port: ' + str(self.port), 'INFO')
        self.BFI_logger.classLog('', 'INFO')
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        print ""
>>>>>>> ebc1f28fc242a94d4ee2da07579e1ded76af4bf1
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
        self.BFI_logger.classLog('Bundle sent successfully.', 'INFO')

    def receiveBundle(self, timeout=None):

        self.BFI_logger.classLog('Receiving bundle...', 'INFO')
        if timeout:
            self.sock.settimeout(timeout)
            self.BFI_logger.classLog('Setting timeout: ' + str(timeout), 'INFO')

        try:
<<<<<<< HEAD
            bundle, fromSocket = self.sock.recvfrom(1024)
        except KeyboardInterrupt:
            print "Keyboard interrupted. Failed to receive bundle. Terminating from BundleFlowInterface."
            exit()
=======
            bundle, fromAddress = self.sock.recvfrom(1024)
            self.BFI_logger.classLog('Bundle ' + bundle + ' received from ' + str(fromAddress), 'INFO')

>>>>>>> ebc1f28fc242a94d4ee2da07579e1ded76af4bf1
        except:
            self.BFI_logger.classLog('No bundle received.', 'WARNING')
            return None

        if timeout:
            self.sock.settimeout(None)
<<<<<<< HEAD
            
        return bundle, fromSocket
=======
            self.BFI_logger.classLog('Setting timeout: ' + str(timeout), 'INFO')

        return bundle, fromAddress
>>>>>>> ebc1f28fc242a94d4ee2da07579e1ded76af4bf1

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.classLog('Setting to_addr: ' + str(toAddress), 'INFO')
