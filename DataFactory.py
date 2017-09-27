# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time
import random

class DataFactory:
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, dataSize, maxEntries, droppingProtocol, timeToGenerate):
        self.dataSize = dataSize
        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.timeToGenerate = timeToGenerate
        self.data = []

    def printProperties(self):
        print 'Size of data table (in bytes):', self.dataSize
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print 'Time to generate data (in seconds)', self.timeToGenerate
        print '========'

    def generateEntry(self, seq):
        payload = 'x' * self.dataSize
        entry = str(seq) + ' ' + payload
        return entry

    def pushEntry(self, entry):
        self.data.append(entry)
        return True        

    def printData(self):
        print 'SEQ PAYLOAD'
        for i in self.data:
            print i
        print '----'

    def dropFirst(self):
        first = self.data[0]
        del self.data[0]

        return first

    def dropLast(self):
        last = self.data[-1]
        del self.data[-1]

        return last

    def dropRandom(self):
        index = random.randint(0, self.maxEntries - 1)
        entry = self.data[index]
        del self.data[index]

        return entry

    def dropEntry(self):
        droppedEntry = None
        if self.droppingProtocol == self.DROP_FIRST_PROTOCOL:
            droppedEntry = self.dropFirst()
        elif self.droppingProtocol == self.DROP_LAST_PROTOCOL:
            droppedEntry = self.dropLast()
        elif self.droppingProtocol == self.DROP_RANDOM_PROTOCOL:
            droppedEntry = self.dropRandom()      
        print 'Dropped:', droppedEntry
        return droppedEntry

    def isTableFull(self):
        if self.maxEntries == len(self.data):
            return True
        else:
            return False

    def start(self):
        seq = 1

        while True:
            self.printData()
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry(seq)
            seq += 1
            if self.isTableFull():
                if self.droppingProtocol == self.DROP_CURRENT_PROTOCOL:
                    print 'Dropped:', entry
                    continue
                self.dropEntry()
            self.pushEntry(entry)

    def getData(self):
        data = self.data[0]
        del self.data[0]
        print 'Sent data:', data
        return data