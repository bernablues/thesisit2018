import logging
from SDTNLogger import SDTNLogger

class BundleFlowInterface:
    def __init__(self, sock, toAddress = None, experiments=None):
        self.BFI_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.BFI_logger.classLog('Initializing BFI...', 'INFO')

        self.sendDataTable_logger = SDTNLogger('sendDataTable', experiments, 'INFO')    
        self.sendDataTable_logger.classLog('Initializing BFI...', 'INFO')


        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

        self.BFI_logger.classLog('BFI initialized:,TO_ADDR:,' + str(self.toAddress) + ',SOCK:,' + str(self.sock) + ',PORT:,' + str(self.port), 'INFO')
        self.sendDataTable_logger.classLog('BFI initialized:,TO_ADDR:,' + str(self.toAddress) + ',SOCK:,' + str(self.sock) + ',PORT:,' + str(self.port), 'INFO')

    def sendBundle(self, bundle):
        self.BFI_logger.classLog('Sending bundle:,' + bundle.toString() + ',TO_ADDR:,' + str(self.toAddress) + ',PORT:,' + str(self.port), 'INFO')
        self.sendDataTable_logger.classLog('Sending bundle:,' + bundle.toString() + ',TO_ADDR:,' + str(self.toAddress) + ',PORT:,' + str(self.port), 'INFO')

        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        # print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
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
            self.BFI_logger.classLog('BUNDLE:,' + str(bundle) + ',RECEIVED_FROM:,' + str(fromSocket), 'INFO')
        except KeyboardInterrupt:
            print "Keyboard interrupted. Failed to receive bundle. Terminating from BundleFlowInterface."
            self.BFI_logger.classLog('No bundle received.', 'WARNING')
            self.sendDataTable_logger.classLog('No bundle received.', 'WARNING')
            exit()
        except:
            self.sock.settimeout(None)
            return None

        if timeout:    
            self.sock.settimeout(None)
            
        return bundle, fromSocket

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.classLog('Setting TO_ADDR:,' + str(toAddress), 'INFO')
