import logging


class BundleFlowInterface:

    logging.basicConfig(level=logging.DEBUG)

    BFI_logger = logging.getLogger(__name__)
    BFI_logger.setLevel(logging.INFO)

    BFI_handler = logging.FileHandler(__name__)
    BFI_handler.setLevel(logging.INFO)

    BFI_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    BFI_handler.setFormatter(BFI_formatter)

    BFI_logger.addHandler(BFI_handler)

    def __init__(self, sock, toAddress = None):

        self.BFI_logger.info('Initializing BFI...')

        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

        self.BFI_logger.info('BFI initialized: to_addr: (%s) sock: (%s) port: (%s)', toAddress, sock, self.port)

    def sendBundle(self, bundle):

        self.BFI_logger.info('Sending', bundle.toString(), 'to addr: (%s) port: (%s)', self.toAddress, self.port)
        self.BFI_logger.info('')
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        
        self.BFI_logger.info('Bundle sent successfully.')

    def receiveBundle(self, timeout=None):

        self.BFI_logger.info('Receiving bundle...')
        if timeout:
            self.sock.settimeout(timeout)
            self.BFI_logger.info('Setting timeout: (%s)', timeout)

        try:
            bundle, fromAddress = self.sock.recvfrom(1024)
            self.BFI_logger.info('Bundle (%s) received from (%s)', bundle, fromAddress)    
            
        except:
            self.BFI_logger.warning('No bundle received.')    
            return None

        if timeout:    
            self.sock.settimeout(None)
            self.BFI_logger.info('Setting timeout: (%s)', timeout)
            
            
        return bundle, fromAddress

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
        self.BFI_logger.info('Setting to_addr: (%s)', toAddress)
            