import logging

logging.basicConfig(level=logging.DEBUG)

Bundle_logger = logging.getLogger(__name__)
Bundle_logger.setLevel(logging.INFO)

Bundle_handler = logging.FileHandler(__name__)
Bundle_handler.setLevel(logging.INFO)

Bundle_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
Bundle_handler.setFormatter(Bundle_formatter)

Bundle_logger.addHandler(Bundle_handler)


class Bundle:
    def __init__(self, data):
        Bundle_logger.info('Initializing bundle...')

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

        Bundle_logger.info('Bundle initialized: type: %s seq: %s SID: %s payload: %s', self.type, self.seq, self.sid, self.payload)
        

    def getBundleProperties(self):
        Bundle_logger.info('Bundle properties: type: %s sid: %s payload: %s', self.type, self.sid, self.payload)
        return [self.type, self.sid, self.payload]

    def getType(self):
        Bundle_logger.info('Getting bundle type: %s', self.type)
        return self.type

    def getSID(self):
        Bundle_logger.info('Getting bundle SID: %s', self.sid)
        return self.sid

    def getSeq(self):
        Bundle_logger.info('Getting Seq: %s', self.seq)
        return self.seq

    def getPayload(self):
        Bundle_logger.info('Getting bundle payload: %s', self.payload)
        return self.payload

    def stringToList(self, string):
        Bundle_logger.info('Converting string to list...')
        return string.split()

    def tupleToList(self, tupleData):
        Bundle_logger.info('Converting tuple to list...')
        return [str(x) for x in tupleData]

    def toString(self):
        Bundle_logger.info('Converting to string: %s', self)
        return str(self.type) + ' ' + str(self.seq)+ ' ' + str(self.sid) + ' ' + self.payload

    def toData(self):
        Bundle_logger.info('Converting to data...')
        return [str(self.sid), str(self.payload)]