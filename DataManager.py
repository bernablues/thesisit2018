# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import random
import time

class DataManager:
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    # DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, maxEntries, droppingProtocol, dbInterface, bundleSize, experiments=None):
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
        while self.isBufferFull():
            self.dropLast()
        return True

    def insertData(self, data, seq_number = None):
        if self.isBufferFull():
            self.dropData()
        if self.hasData(data[1]):
            return True

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

    def checkBundleSizeLimit(self):
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
        return data

    def getBundle(self, deleteBundle = False):
        checkDataTimeout = 0
        time.sleep(2)
        checkDataTimeout += 1
        if checkDataTimeout == 5:
            return None
        data = self.dbInterface.getRows(1)
        if deleteBundle:
            self.dbInterface.deleteRows(1)
        data = str(data[0])[1:-1].split(', ')
        data[0] = data[0][0:-1]
        data[1] = data[1][0:-1]
        data[2] = data[2][0:-1]
        #CLEAN THIS SHIT
        data[3] = data[3][1:-1]
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

        if seqNumbers:
            results = self.dbInterface.getRowsFromSeqNumbers(seqNumbers)
            results = self.padZeroesToDataSeq(results)
            return results
        return self.dbInterface.getAllRows()

    def getDataMap(self):
        return map((lambda x: str(x[1])), self.getAllData())

    def hasData(self, data):
        return data in self.getDataMap()
