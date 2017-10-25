import logging
from SDTNLogger import SDTNLogger

<<<<<<< HEAD

class Bundle:

    def __init__(self, data, experiments):

        self.Bundle_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.Bundle_logger.classLog("Initializing Bundle...", 'INFO')

        
        
=======
class Bundle:
    def __init__(self, data, experiments=None):
        self.Bundle_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.Bundle_logger.classLog("Initializing Bundle...", 'INFO')

>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
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
<<<<<<< HEAD
        # self.Bundle_logger.classLog("Bundle initialized: type: %s seq: %s SID: %s payload: %s, self.type, self.seq, self.sid, self.payload", 'INFO')

    def getBundleProperties(self):
        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')
        
=======

    def getBundleProperties(self):
        self.Bundle_logger.classLog('Bundle initialized:,TYPE:,' + str(self.type) + ',SEQ:,' + str(self.seq) + ',SID:,' + str(self.sid) + ',PAYLOAD:,' + str(self.payload), 'INFO')
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
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
<<<<<<< HEAD
        self.Bundle_logger.classLog('Getting bundle PAYLOAD:,'+ str(self.payload), 'INFO')
        # self.Bundle_logger.info('Getting bundle payload: %s', self.payload)
=======
        self.Bundle_logger.classLog('Getting bundle PAYLOAD:,'+ str(self.payload), 'DEBUG')
        self.Bundle_logger.classLog('Getting bundle PAYLOAD...', 'INFO')
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        return self.payload

    def stringToList(self, string):
        self.Bundle_logger.classLog('Converting string to list...', 'INFO')
<<<<<<< HEAD
        return string.split()

    def tupleToList(self, tupleData):
        self.Bundle_logger.classLog('Converting tuple to list...', 'INFO')
        return [str(x) for x in tupleData]

    def toString(self):
        self.Bundle_logger.classLog('Converting to string...', 'DEBUG')
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload

    def toData(self):
        self.Bundle_logger.classLog('Converting to data...', 'DEBUG')
=======
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
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        return [str(self.sid), str(self.payload)]