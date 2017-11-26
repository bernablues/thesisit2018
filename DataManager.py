# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import random
import time
import logging
from SDTNLogger import SDTNLogger

class DataManager:
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    # DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, maxEntries, droppingProtocol, dbInterface, bundleSize, experiments=None):
        self.DataMan_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.DataMan_logger.classLog('Initializing DataMan...', 'INFO')
        
        self.dropDataTable_logger = SDTNLogger('dropDataTable', experiments, 'INFO')
        self.dropDataTable_logger.classLog('Initializing DataMan...', 'INFO')

        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.dbInterface = dbInterface
        self.equalizeMaxEntries() #Needed for drop current protocol
        self.bundleSize = bundleSize

    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'

    def equalizeMaxEntries(self):
        self.DataMan_logger.classLog('Equalizing max_entries...', 'INFO')
        while self.isBufferFull():
            self.dropLast()
        return True

    def insertData(self, data, seq_number = None):
        self.DataMan_logger.classLog('Inserting data...', 'INFO')
        if self.isBufferFull():
            self.dropData()
        if self.hasData(data[1]):
            return True

        self.dbInterface.insertRow(data)
        self.DataMan_logger.classLog('Successfully inserted data.', 'INFO')        
        return True        

    def printData(self):
        pass

    def dropFirst(self):
        self.DataMan_logger.classLog('NULL,Dropping:, FIRST_DATA...', 'WARNING')
        self.dropDataTable_logger.classLog('NULL,Dropping:, FIRST_DATA...', 'WARNING')
        first = self.dbInterface.getRows(1)
        self.dbInterface.deleteRows(1)
        self.DataMan_logger.classLog('NULL,Successfully dropped:,FIRST_DATA.', 'WARNING')
        self.dropDataTable_logger.classLog('NULL,Successfully dropped:,FIRST_DATA.', 'WARNING')
        return first

    def dropLast(self):
        self.DataMan_logger.classLog('NULL,Dropping:, LAST_DATA...', 'WARNING')
        self.dropDataTable_logger.classLog('NULL,Dropping:, LAST_DATA...', 'WARNING')
        last = self.dbInterface.getRows(1, True)
        self.dbInterface.deleteRows(1, True)
        self.DataMan_logger.classLog('NULL,Successfully dropped:,LAST_DATA.', 'WARNING')
        self.dropDataTable_logger.classLog('NULL,Successfully dropped:,LAST_DATA.', 'WARNING')
        return last

    # def dropRandom(self):
    #     index = random.randint(0, self.maxEntries - 1)
    #     data = self.dbInterface.getNthRow(n)
    #     del self.data[index]

    #     return entry

    def dropData(self):
        self.DataMan_logger.classLog('Dropping data...', 'WARNING')
        self.dropDataTable_logger.classLog('Dropping data...', 'WARNING')
        droppedData = None
        if self.droppingProtocol == self.DROP_FIRST_PROTOCOL:
            droppedData = self.dropFirst()
        elif self.droppingProtocol == self.DROP_LAST_PROTOCOL:
            droppedData = self.dropLast()
        # elif self.droppingProtocol == self.DROP_RANDOM_PROTOCOL:
        #     droppedData = self.dropRandom()     
        elif self.droppingProtocol == self.DROP_CURRENT_PROTOCOL:
            droppedData = 'Current' 
        return droppedData

    def isBufferFull(self):
        currentEntries = self.dbInterface.getRowCount()
        if self.maxEntries <= currentEntries:
            self.DataMan_logger.classLog('NULL,NULL,NULL,Buffer is full:,TRUE.', 'WARNING')
            self.dropDataTable_logger.classLog('NULL,NULL,NULL,Buffer is full:,TRUE.', 'WARNING')
            return True
        else:
            self.DataMan_logger.classLog('NULL,NULL,NULL,Buffer is full:,FALSE.', 'INFO')
            self.dropDataTable_logger.classLog('NULL,NULL,NULL,Buffer is full:,FALSE.', 'INFO')
            return False

    def checkBundleSizeLimit(self):
        self.DataMan_logger.classLog('Checking BundleSize limit...', 'INFO')
        self.dropDataTable_logger.classLog('Checking BundleSize limit...', 'INFO')
        rowsAvailabe = self.dbInterface.getRowCount()
        if self.bundleSize <= rowsAvailabe:
            return True
        else:
            return False
    
    def padZeroesToDataSeq(self, data):
        newData = []
        for datum in data:
            datum = list(datum)
            datum[1] = '%03d' % datum[1]
            datum = tuple(datum)
            newData.append(datum)
        newData = tuple(newData)
        return newData

    def getData(self, deleteData = False):
        checkDataTimeout = 0
        self.DataMan_logger.classLog('Getting data...', 'INFO')
        while not self.checkBundleSizeLimit():
            time.sleep(2)
            checkDataTimeout += 1
            if checkDataTimeout == 5:
                return None
            else:
                continue
        data = self.dbInterface.getRows(self.bundleSize)
        data = self.padZeroesToDataSeq(data)
        if deleteData:
            self.dbInterface.deleteRows(self.bundleSize)
        self.DataMan_logger.classLog('Get data successful.', 'INFO')
        return data

    def sliceData(self, data):
        # Fix this when bundle headers are defined
        timestampLength = 18
        seqNumberLength = 3
        dataLength = 1
        rowLength = timestampLength + seqNumberLength + dataLength

        payload = data
        payload = [payload[i: i + rowLength] for i in range(0, len(payload), rowLength)]
        slicedData = []

        for each in payload:
            slicedData.append([each[0:10] + ' ' + each[10:18], each[18:21], each[21:22]])
        return slicedData

    def getAllData(self, seqNumbers = None):
        self.DataMan_logger.classLog('Get data successful.', 'INFO')

        if seqNumbers:
            results = self.dbInterface.getRowsFromSeqNumbers(seqNumbers)
            results = self.padZeroesToDataSeq(results)
            return results
        return self.dbInterface.getAllRows()

    def getDataMap(self):
        return map((lambda x: str(x[1])), self.getAllData())

    def hasData(self, data):
        return data in self.getDataMap()
