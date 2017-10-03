class BundleFlowInterface:
    def __init__(self, sock, toAddress):
        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])

    def sendBundle(self, bundleString):
        print 'Sending', bundleString, 'to:', self.toAddress, self.port
        print ""
        self.sock.sendto(bundleString, (self.toAddress, self.port))
    
    def receiveBundle(self, timeout=None):
        if timeout:
            self.sock.settimeout(timeout)

        try:
            bundle, fromAddress = self.sock.recvfrom(1024)
            
        except:
            return False

        if timeout:    
            self.sock.settimeout(None)
            
        return bundle, fromAddress