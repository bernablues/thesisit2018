# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import random
import logging
from SDTNLogger import SDTNLogger

class DataManager:

    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    # DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

<<<<<<< HEAD
    def __init__(self, maxEntries, droppingProtocol, dbInterface, experiments):
        # self.DataMan_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')
        self.DataMan_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')    

        self.DataMan_logger.classLog('Initializing DataMan...', 'INFO')
=======
    def __init__(self, maxEntries, droppingProtocol, dbInterface, bundleSize, experiments=None):
        self.DataMan_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.DataMan_logger.classLog('Initializing DataMan...', 'INFO')
        
        self.dropDataTable_logger = SDTNLogger('dropDataTable', experiments, 'INFO')
        self.dropDataTable_logger.classLog('Initializing DataMan...', 'INFO')
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b

        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.dbInterface = dbInterface
        self.equalizeMaxEntries() #Needed for drop current protocol
<<<<<<< HEAD
        # DataMan_logger.info("DataManager initialized: {} (${})".format(self.maxEntries, self.dbInterface))
        # self.DataMan_logger.info('DataMan initialized: max_entries: %s  %s DBI: %S', maxEntries, droppingProtocol, dbInterface)
        self.DataMan_logger.classLog('DataMan initialized:,MAX_ENTRIES:,' + str(self.maxEntries) + ',DROPPING_PROTOCOL:,' + str(self.droppingProtocol) + ',DBI:,' + str(self.dbInterface), 'INFO')
=======
        self.bundleSize = bundleSize
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b

    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'
        self.DataMan_logger.classLog('DataMan initialized:,MAX_ENTRIES:,' + str(self.maxEntries) + ',DROPPING_PROTOCOL:,' + str(self.droppingProtocol) + ',DBI:,' + str(self.dbInterface), 'INFO')

    def equalizeMaxEntries(self):
        self.DataMan_logger.classLog('Equalizing max_entries...', 'INFO')
        while self.isBufferFull():
            self.dropLast()
        return True

    def insertData(self, data):
        self.DataMan_logger.classLog('Inserting data...', 'INFO')
        if self.isBufferFull():
            self.dropData()
            return False
        self.dbInterface.insertRow(data)
<<<<<<< HEAD
        self.DataMan_logger.classLog('Successfully inserted data.', 'INFO')
=======
        self.dbInterface.insertRow(data)
        self.DataMan_logger.classLog('Successfully inserted data.', 'INFO')        
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        return True        

    def printData(self):
        pass

    def dropFirst(self):
<<<<<<< HEAD
        self.DataMan_logger.classLog('Dropping FIRST_DATA...', 'WARNING')
        first = self.dbInterface.getRows(1)
        self.dbInterface.deleteRows(1)
        self.DataMan_logger.classLog('Successfully dropped:,FIRST_DATA.', 'WARNING')
        return first

    def dropLast(self):
        self.DataMan_logger.classLog('Dropping LAST_DATA...', 'WARNING')
        last = self.dbInterface.getRows(1, True)
        self.dbInterface.deleteRows(1, True)
        self.DataMan_logger.classLog('Successfully dropped:,LAST_DATA.', 'WARNING')
=======
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
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        return last

    # def dropRandom(self):
    #     index = random.randint(0, self.maxEntries - 1)
    #     data = self.dbInterface.getNthRow(n)
    #     del self.data[index]

    #     return entry

    def dropData(self):
        self.DataMan_logger.classLog('Dropping data...', 'WARNING')
<<<<<<< HEAD
=======
        self.dropDataTable_logger.classLog('Dropping data...', 'WARNING')
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
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
<<<<<<< HEAD
        if self.maxEntries < currentEntries:
            self.DataMan_logger.classLog('Buffer full:,TRUE.', 'WARNING')
            return True
        else:
            self.DataMan_logger.classLog('Buffer full:,FALSE.', 'INFO')
            return False

    def getData(self, numberOfData, deleteData = False):
        self.DataMan_logger.classLog('Getting data...', 'INFO')
        data = self.dbInterface.getRows(numberOfData)
        if deleteData:
            self.dbInterface.deleteRows(numberOfData)
=======
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

    def getData(self, deleteData = False):
        self.DataMan_logger.classLog('Getting data...', 'INFO')
        while not self.checkBundleSizeLimit():
            continue
        data = self.dbInterface.getRows(self.bundleSize)
        if deleteData:
            self.dbInterface.deleteRows(self.bundleSize)
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
        self.DataMan_logger.classLog('Get data successful.', 'INFO')
        return data

    def sliceData(self, data):
        # Fix this when bundle headers are defined
        timestampLength = 18
        seqNumberLength = 1
        dataLength = 1
        rowLength = timestampLength + seqNumberLength + dataLength

        payload = data
        payload = [payload[i: i + rowLength] for i in range(0, len(payload), rowLength)]
        slicedData = []

        for each in payload:
            slicedData.append([each[0:10] + ' ' + each[10:18], each[18:19], each[19:20]])
        return slicedData

    def getAllData(self):
<<<<<<< HEAD
        self.DataMan_logger.classLog('Getting all data...', 'INFO')
        return self.dbInterface.getAllRows()
=======
        self.DataMan_logger.classLog('Get data successful.', 'INFO')
        return self.dbInterface.getAllRows()
>>>>>>> 16a27b48504596ee80bff325278896cf038df95b
