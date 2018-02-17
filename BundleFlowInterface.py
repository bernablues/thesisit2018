class BundleFlowInterface:
    def __init__(self, sock, toAddress = None, experiments=None):
        self.toAddress = toAddress
        self.sock = sock
        self.port = int(self.sock.getsockname()[1])


    def sendBundle(self, bundle):
        print 'Sending', bundle.toString(), 'to:', self.toAddress, self.port
        # print ""
        bundleString = bundle.toString()
        self.sock.sendto(bundleString, (self.toAddress, self.port))
        

    def receiveBundle(self, timeout=None):
        if timeout:
            self.sock.settimeout(timeout)

        try:
            bundle, fromSocket = self.sock.recvfrom(1024)
            print "RECEIVED: " + bundle
        except KeyboardInterrupt:
            print "Keyboard interrupted. Failed to receive bundle. Terminating from BundleFlowInterface."
            exit()
        except:
            self.sock.settimeout(None)
            print "Receive Timeout"
            return None, None

        if timeout:    
            self.sock.settimeout(None)
            
        return bundle, fromSocket

    def setToAddress(self, toAddress):
        self.toAddress = toAddress
