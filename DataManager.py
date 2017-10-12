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

    def __init__(self, maxEntries, droppingProtocol, dbInterface):
        self.DataMan_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')    
        self.DataMan_logger.classLog('Initializing DataMan...', 'INFO')

        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.dbInterface = dbInterface
        self.equalizeMaxEntries() #Needed for drop current protocol
        # DataMan_logger.info("DataManager initialized: {} (${})".format(self.maxEntries, self.dbInterface))
        # self.DataMan_logger.info('DataMan initialized: max_entries: %s  %s DBI: %S', maxEntries, droppingProtocol, dbInterface)
        self.DataMan_logger.classLog('DataMan initialized: max_entries: ' + str(self.maxEntries) + ' dropping_protocol: ' + str(self.droppingProtocol) + ' DBI: ' + str(self.dbInterface), 'INFO')

    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'
        self.DataMan_logger.classLog('DataMan initialized: max_entries: ' + str(self.maxEntries) + ' dropping_protocol: ' + str(self.droppingProtocol) + ' DBI: ' + str(self.dbInterface), 'INFO')


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
        self.DataMan_logger.classLog('Successfully inserted data.', 'INFO')
        return True        

    def printData(self):
        pass

    def dropFirst(self):
        self.DataMan_logger.classLog('Dropping first data...', 'WARNING')
        first = self.dbInterface.getRows(1)
        self.dbInterface.deleteRows(1)
        self.DataMan_logger.classLog('Successfully dropped first data.', 'WARNING')
        return first

    def dropLast(self):
        self.DataMan_logger.classLog('Dropping last data...', 'WARNING')
        last = self.dbInterface.getRows(1, True)
        self.dbInterface.deleteRows(1, True)
        self.DataMan_logger.classLog('Successfully dropped last data.', 'WARNING')
        return last

    # def dropRandom(self):
    #     index = random.randint(0, self.maxEntries - 1)
    #     data = self.dbInterface.getNthRow(n)
    #     del self.data[index]

    #     return entry

    def dropData(self):
        self.DataMan_logger.classLog('Dropping data...', 'WARNING')
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
        if self.maxEntries < currentEntries:
            self.DataMan_logger.classLog('Buffer is full.', 'WARNING')
            return True
        else:
            self.DataMan_logger.classLog('Buffer not yet full.', 'INFO')
            return False

    def getData(self, numberOfData, deleteData = False):
        self.DataMan_logger.classLog('Getting data...', 'INFO')
        data = self.dbInterface.getRows(numberOfData)
        if deleteData:
            self.dbInterface.deleteRows(numberOfData)
        self.DataMan_logger.classLog('Get data successful.', 'INFO')
        return data

    def getAllData(self):
        self.DataMan_logger.classLog('Getting all data...', 'INFO')
        return self.dbInterface.getAllRows()
