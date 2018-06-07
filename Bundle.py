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

        self.averageData = str(bundleData[4])
        self.minData = str(bundleData[5])
        self.maxData = str(bundleData[6])

        self.action = ''

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
        data = ''.join(bundleData[3])
        maxData = bundleData[-1]
        minData = bundleData[-2]
        aveData = bundleData[-3]

        return [bundleType, seq, sid, data, aveData, minData, maxData]

    def tupleToList(self, tupleData):
        headers = tupleData[0]
        bundleType = headers[0]
        seq = headers[1]
        sid = headers[2]
        data = ''
        for each in tupleData[1]:
            dataList = [str(x) for x in each]
            data += ''.join(dataList)
        data = ''.join(data.split())
        average = tupleData[2][0]
        minData = tupleData[2][1]
        maxData = tupleData[2][2]

        bundleData = [bundleType, seq, sid, data, average, minData, maxData]
        return bundleData


    def toString(self):
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload + ' ' + str(self.averageData) + ' ' + str(self.minData) + ' ' + str(self.maxData)

    def toData(self):
        return [str(self.sid), str(self.payload)]