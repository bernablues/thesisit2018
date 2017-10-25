import logging
from SDTNLogger import SDTNLogger

class BundleFlowInterface:
<<<<<<< HEAD

    def __init__(self, sock, toAddress=None, experiments):
        # self.BFI_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')
        
        # self.BFI_logger = SDTNLogger(self.__class__.__name__, ['x','x'], 'INFO')
        self.BFI_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')

        self.BFI_logger.classLog('Initializing BFI...', 'INFO')

=======
    def __init__(self, sock, toAddress = None, experiments=None):
        self.BFI_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.BFI_logger.classLog('Initializing BFI...', 'INFO')

        self.sendDataTable_logger = SDTNLogger('sendDataTable', experiments, 'INFO')    
        self.sendDataTable_logger.classLog('Initializing BFI...', 'INFO')


>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

        self.BFI_logger.classLog('BFI initialized:,TO_ADDR:,' + str(self.toAddress) + ',SOCK:,' + str(self.sock) + ',PORT:,' + str(self.port), 'INFO')
<<<<<<< HEAD

    def sendBundle(self, bundle):

        # self.BFI_logger.classLog('Sending', bundle.toString(), 'to addr: (%s) port: (%s)', self.toAddress, self.port)
        self.BFI_logger.classLog('Sending bundle:,' + bundle.toString() + ',TO_ADDR:,' + str(self.toAddress) + ',PORT:,' + str(self.port), 'INFO')
        self.BFI_logger.classLog('', 'INFO')
=======
        self.sendDataTable_logger.classLog('BFI initialized:,TO_ADDR:,' + str(self.toAddress) + ',SOCK:,' + str(self.sock) + ',PORT:,' + str(self.port), 'INFO')

    def sendBundle(self, bundle):
        self.BFI_logger.classLog('Sending bundle:,' + bundle.toString() + ',TO_ADDR:,' + str(self.toAddress) + ',PORT:,' + str(self.port), 'INFO')
        self.sendDataTable_logger.classLog('Sending bundle:,' + bundle.toString() + ',TO_ADDR:,' + str(self.toAddress) + ',PORT:,' + str(self.port), 'INFO')

>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        # print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
<<<<<<< HEAD
        self.BFI_logger.classLog('Bundle sent successfully.', 'INFO')

    def receiveBundle(self, timeout=None):

        self.BFI_logger.classLog('Receiving bundle...', 'INFO')
        if timeout:
            self.sock.settimeout(timeout)
            self.BFI_logger.classLog('Setting TIMEOUT:,' + str(timeout), 'INFO')

        try:
            bundle, fromAddress = self.sock.recvfrom(1024)
            self.BFI_logger.classLog('BUNDLE:,' + bundle.toString() + ',RECEIVED_FROM:,' + str(fromAddress), 'INFO')

        except:
            self.BFI_logger.classLog('No bundle received.', 'WARNING')
=======
        self.BFI_logger.classLog('Bundle sent:, successfully.', 'INFO')
        self.sendDataTable_logger.classLog('Bundle sent:, successfully.', 'INFO')

    def receiveBundle(self, timeout=None):
        self.BFI_logger.classLog('Receiving bundle...', 'INFO')
        self.sendDataTable_logger.classLog('Receiving bundle...', 'INFO')
        
        if timeout:
            self.sock.settimeout(timeout)
            self.BFI_logger.classLog('Setting TIMEOUT:,' + str(timeout), 'INFO')
            self.sendDataTable_logger.classLog('Receiving bundle...', 'INFO')

        try:
            bundle, fromSocket = self.sock.recvfrom(1024)
            print bundle
            self.BFI_logger.classLog('BUNDLE:,' + bundle.toString() + ',RECEIVED_FROM:,' + str(fromSocket), 'INFO')
        except KeyboardInterrupt:
            print "Keyboard interrupted. Failed to receive bundle. Terminating from BundleFlowInterface."
            self.BFI_logger.classLog('No bundle received.', 'WARNING')
            self.sendDataTable_logger.classLog('No bundle received.', 'WARNING')
            exit()
        except:
            self.sock.settimeout(None)
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
            return None

        if timeout:
            self.sock.settimeout(None)
<<<<<<< HEAD
            self.BFI_logger.classLog('Setting timeout:,' + str(timeout), 'INFO')

        return bundle, fromAddress

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.classLog('Setting TO_ADDR:,' + str(toAddress), 'INFO')
=======
            
        return bundle, fromSocket

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.classLog('Setting TO_ADDR:,' + str(toAddress), 'INFO')
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
