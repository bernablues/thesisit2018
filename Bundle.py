class Bundle:
    def __init__(self, data, experiments=None):
        # Check if this can be directly touched by outside code
        if type(data) is str:
            bundleData = self.stringToList(data)
        elif type(data) is tuple:
            bundleData = self.tupleToList(data)
        elif type(data) is list:
            bundleData = data
        self.type = str(bundleData[0])
        self.seq = str(bundleData[1])

        if len(bundleData) < 3:
            bundleData[2] = ''
        if len(bundleData) < 4:
            bundleData[3] = ''
        self.sid = str(bundleData[2])
        self.payload = str(bundleData[3])
        print "Bundle: " + self.payload

        self.action = '2'

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
    
    def setAction(self, action):
        self.action = action

    def stringToList(self, string):
        bundleData = string.split()
        bundleType = bundleData[0]
        seq = bundleData[1]
        sid = bundleData[2]
        data = ''
        data = ''.join(bundleData[3:])
        return [bundleType, seq, sid, data]

    def tupleToList(self, tupleData):
        headers = tupleData[0]
        bundleType = headers[0]
        seq = headers[1]
        sid = headers[2]
        data = ''
        for each in tupleData[1]:
            dataList = [str(x) for x in each]
            data += ''.join(dataList)
        bundleData = [bundleType, seq, sid, data]
        return bundleData


    def toString(self):
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload + ' ' + str(self.action)

    def toData(self):
        return [str(self.sid), str(self.payload)]