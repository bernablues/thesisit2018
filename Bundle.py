class Bundle:
    def __init__(self, string):
        # Check if this can be directly touched by outside code
        bundleData = self.stringToBundle(string)
        self.type = bundleData[0]
        self.sid = bundleData[1]
        self.payload = bundleData[2]

    def getBundleProperties(self):
        return [self.type, self.sid, self.payload]

    def getType(self):
        return self.type

    def getSID(self):
        return self.sid

    def getPayload(self):
        return self.payload

    def stringToBundle(self, string):
        return string.split()

    def toString(self):
        return str(self.type) + ' ' + str(self.sid) + self.payload