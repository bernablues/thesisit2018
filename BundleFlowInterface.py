import logging

logging.basicConfig(level=logging.DEBUG)

BFI_logger = logging.getLogger(__name__)
BFI_logger.setLevel(logging.INFO)

BFI_handler = logging.FileHandler(__name__)
BFI_handler.setLevel(logging.INFO)

BFI_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
BFI_handler.setFormatter(BFI_formatter)

BFI_logger.addHandler(BFI_handler)

class BundleFlowInterface:
    def __init__(self, sock, toAddress = None):
        BFI_logger.info('Initializing BFI...')

        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

        BFI_logger.info('BFI initialized: to_addr: (%s) sock: (%s) port: (%s)', toAddress, sock, self.port)

    def sendBundle(self, bundle):

        BFI_logger.info('Sending', bundle.toString(), 'to addr: (%s) port: (%s)', self.toAddress, self.port)
        BFI_logger.info('')
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
        BFI_logger.info('Bundle sent successfully.')

    def receiveBundle(self, timeout=None):

        BFI_logger.info('Receiving bundle...')
        if timeout:
            self.sock.settimeout(timeout)
            BFI_logger.info('Setting timeout: (%s)', timeout)

        try:
            bundle, fromAddress = self.sock.recvfrom(1024)
            BFI_logger.info('Bundle (%s) received from (%s)', bundle, fromAddress)    
            
        except:
            BFI_logger.warning('No bundle received.')    
            return None

        if timeout:    
            self.sock.settimeout(None)
            BFI_logger.info('Setting timeout: (%s)', timeout)
            
            
        return bundle, fromAddress

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        BFI_logger.info('Setting to_addr: (%s)', toAddress)
            