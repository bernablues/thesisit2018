class Bundle:
    def __init__(self, data):
        # Check if this can be directly touched by outside code
        if type(data) is str:
            bundleData = self.stringToList(data)
        elif type(data) is tuple:
            bundleData = self.tupleToList(data)
        self.type = bundleData[0]
        self.seq = bundleData[1]

        if len(bundleData) < 3:
            bundleData[2] = ''
        if len(bundleData) < 4:
            bundleData[3] = ''

        self.sid = bundleData[2]
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

    def stringToList(self, string):
        return string.split()

    def tupleToList(self, tupleData):
        return [str(x) for x in tupleData]

    def toString(self):
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload

    def toData(self):
        return [str(self.sid), str(self.payload)]