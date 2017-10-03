class Bundle:
    def __init__(self, string):
        # Check if this can be directly touched by outside code
        bundleData = self.stringToBundle(string)
        self.type = bundleData[0]
        self.sid = bundleData[1]
        self.seq = bundleData[2]
        self.payload = bundleData[3]

    def getBundleProperties(self):
        return [self.type, self.sid, self.payload]

    def getType(self):
        return self.type

    def getSID(self):
        return self.sid

    def getSeq(self):
        return self.seq

    def getPayload(self):
        return self.payload

    def stringToBundle(self, string):
        return string.split()

    def toString(self):
        return str(self.type) + ' ' + str(self.sid) + self.payload

    def toData(self):
        return [str(self.sid), str(self.payload)]