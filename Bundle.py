import logging
from SDTNLogger import SDTNLogger


class Bundle:

    def __init__(self, data):

        self.Bundle_logger = SDTNLogger(self.__class__.__name__, ['Y1','Y2'], 'INFO')
        self.Bundle_logger.classLog("Initializing Bundle...", 'INFO')

        
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

        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')
        # self.Bundle_logger.classLog("Bundle initialized: type: %s seq: %s SID: %s payload: %s, self.type, self.seq, self.sid, self.payload", 'INFO')

    def getBundleProperties(self):
        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')
        
        return [self.type, self.sid, self.payload]

    def getType(self):
        self.Bundle_logger.classLog('Getting bundle TYPE: '+ str(self.type), 'INFO')
        return self.type

    def getSID(self):
        self.Bundle_logger.classLog('Getting bundle SID: '+ str(self.sid), 'INFO')
        return self.sid

    def getSeq(self):
        self.Bundle_logger.classLog('Getting SEQ: '+ str(self.seq), 'INFO')
        return self.seq

    def getPayload(self):
        self.Bundle_logger.classLog('Getting bundle PAYLOAD: '+ str(self.payload), 'INFO')
        # self.Bundle_logger.info('Getting bundle payload: %s', self.payload)
        return self.payload

    def stringToList(self, string):
        self.Bundle_logger.classLog('Converting string to list...', 'INFO')
        return string.split()

    def tupleToList(self, tupleData):
        self.Bundle_logger.classLog('Converting tuple to list...', 'INFO')
        return [str(x) for x in tupleData]

    def toString(self):
        self.Bundle_logger.classLog('Converting to string...', 'DEBUG')
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload

    def toData(self):
        self.Bundle_logger.classLog('Converting to data...', 'DEBUG')
        return [str(self.sid), str(self.payload)]