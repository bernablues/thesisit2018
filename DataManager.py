# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import random

import logging


class DataManager:


    logging.basicConfig(level=logging.DEBUG)

    DataMan_logger = logging.getLogger(__name__)
    DataMan_logger.setLevel(logging.INFO)

    DataMan_handler = logging.FileHandler('DataMan.log')
    DataMan_handler.setLevel(logging.INFO)

    DataMan_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    DataMan_handler.setFormatter(DataMan_formatter)

    DataMan_logger.addHandler(DataMan_handler)
    
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    # DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, maxEntries, droppingProtocol, dbInterface):

        self.DataMan_logger.info('Initializing DataMan...')

        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.dbInterface = dbInterface
        self.equalizeMaxEntries() #Needed for drop current protocol
        # DataMan_logger.info("DataManager initialized: {} (${})".format(self.maxEntries, self.dbInterface))
        self.DataMan_logger.info('DataMan initialized: max_entries: %s dropping_protocol: %s DBI: %S', maxEntries, droppingProtocol, dbInterface)
    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'
        self.DataMan_logger.info('DataMan properties: max_entries: %s dropping_protocol: %s', maxEntries, droppingProtocol)

    def equalizeMaxEntries(self):
        self.DataMan_logger.info('Equalizing max_entries...')
        while self.isBufferFull():
            self.dropLast()
        return True

    def insertData(self, data):
        self.DataMan_logger.info('Inserting data')
        if self.isBufferFull():
            self.dropData()
            return False
        self.dbInterface.insertRow(data)
        self.DataMan_logger.info('Successfully inserted data.')
        return True        

    def printData(self):
        pass

    def dropFirst(self):
        self.DataMan_logger.warning('Dropping first data...')
        first = self.dbInterface.getRows(1)
        self.dbInterface.deleteRows(1)
        self.DataMan_logger.warning('Successfully dropped first data.')
        return first

    def dropLast(self):
        self.DataMan_logger.warning('Dropping last data...')
        last = self.dbInterface.getRows(1, True)
        self.dbInterface.deleteRows(1, True)
        self.DataMan_logger.warning('Successfully dropped last data.')
        return last

    # def dropRandom(self):
    #     index = random.randint(0, self.maxEntries - 1)
    #     data = self.dbInterface.getNthRow(n)
    #     del self.data[index]

    #     return entry

    def dropData(self):
        self.DataMan_logger.warning('Dropping data...')
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
            self.DataMan_logger.warning('Buffer is full.')
            return True
        else:
            self.DataMan_logger.info('Buffer not yet full.')
            return False

    def getData(self, numberOfData, deleteData = False):
        self.DataMan_logger.info('Getting data...')
        data = self.dbInterface.getRows(numberOfData)
        if deleteData:
            self.dbInterface.deleteRows(numberOfData)
        self.DataMan_logger.info('Get data successful.')
        return data

    def getAllData(self):
        self.DataMan_logger.info('Getting all data...')
        return self.dbInterface.getAllRows()