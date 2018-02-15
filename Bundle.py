import logging
from SDTNLogger import SDTNLogger

class Bundle:
    def __init__(self, data, experiments=None):
        self.Bundle_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.Bundle_logger.classLog("Initializing Bundle...", 'INFO')

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
        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')

        self.action = None

    def getBundleProperties(self):
        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')
        return [self.type, self.sid, self.payload]

    def getType(self):
        self.Bundle_logger.classLog('Getting bundle TYPE:,'+ str(self.type), 'INFO')
        return self.type

    def getSID(self):
        self.Bundle_logger.classLog('Getting bundle SID:,'+ str(self.sid), 'INFO')
        return self.sid

    def getSeq(self):
        self.Bundle_logger.classLog('Getting SEQ:,'+ str(self.seq), 'INFO')
        return self.seq

    def getPayload(self):
        self.Bundle_logger.classLog('Getting bundle PAYLOAD:,'+ str(self.payload), 'DEBUG')
        self.Bundle_logger.classLog('Getting bundle PAYLOAD...', 'INFO')
        return self.payload
    
    def setAction(self, action):
        self.action = action

    def stringToList(self, string):
        self.Bundle_logger.classLog('Converting string to list...', 'INFO')
        bundleData = string.split()
        bundleType = bundleData[0]
        seq = bundleData[1]
        sid = bundleData[2]
        data = ''
        data = ''.join(bundleData[3:])
        return [bundleType, seq, sid, data]

    def tupleToList(self, tupleData):
        self.Bundle_logger.classLog('Converting tuple to list...', 'INFO')
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
        self.Bundle_logger.classLog('Converting to string...', 'INFO')
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload

    def toData(self):
        self.Bundle_logger.classLog('Converting to data...', 'INFO')
        return [str(self.sid), str(self.payload)]