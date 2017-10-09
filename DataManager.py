# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import random

class DataManager:
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    # DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, maxEntries, droppingProtocol, dbInterface):
        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.dbInterface = dbInterface
        self.equalizeMaxEntries() #Needed for drop current protocol

    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'

    def equalizeMaxEntries(self):
        while self.isBufferFull():
            self.dropLast()
        return True

    def insertData(self, data):
        if self.isBufferFull():
            self.dropData()
            return False
        self.dbInterface.insertRow(data)
        return True        

    def printData(self):
        pass

    def dropFirst(self):
        first = self.dbInterface.getRows(1)
        self.dbInterface.deleteRows(1)
        return first

    def dropLast(self):
        last = self.dbInterface.getRows(1, True)
        self.dbInterface.deleteRows(1, True)
        return last

    # def dropRandom(self):
    #     index = random.randint(0, self.maxEntries - 1)
    #     data = self.dbInterface.getNthRow(n)
    #     del self.data[index]

    #     return entry

    def dropData(self):
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
            return True
        else:
            return False

    def getData(self, numberOfData, deleteData = False):
        data = self.dbInterface.getRows(numberOfData)
        if deleteData:
            self.dbInterface.deleteRows(numberOfData)
        return data

    def getAllData(self):
        return self.dbInterface.getAllRows()