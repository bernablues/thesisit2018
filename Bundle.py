class Bundle:
    def __init__(self, data):
        # Check if this can be directly touched by outside code
        if type(data) is str:
            bundleData = self.stringToList(data)
        elif type(data) is tuple:
            bundleData = self.tupleToList(data)
        self.type = bundleData[0]
        self.bundleSeq = bundleData[1]
        self.timestamp = bundleData[2]
        self.dataSeq = bundleData[3]
        self.sid = bundleData[4]
        self.data = bundleData[5]

    def getBundleProperties(self):
        return [self.type, self.sid, self.data]

    def getType(self):
        return self.type

    def getSID(self):
        return self.sid

    def getBundleSeq(self):
        return self.bundleSeq

    def getDataSeq(self):
        return self.dataSeq

    def getTimestamp(self):
        return self.timestamp

    def getData(self):
        return self.data

    def stringToList(self, string):
        return string.split()

    def tupleToList(self, tupleData):
        return [str(x) for x in tupleData]

    def toString(self):
        return  str(self.type) + ' ' + \
                str(self.bundleSeq) + ' ' + \
                str(self.timestamp) + ' ' + \
                str(self.dataSeq) + ' ' + \
                str(self.sid) + ' ' + \
                self.data

    def toData(self):
        return [str(self.sid), str(self.timestamp), str(self.dataSeq), str(self.data)]