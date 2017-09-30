# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time
import random

class DataManager:
    DROP_FIRST_PROTOCOL = 0
    DROP_LAST_PROTOCOL = 1
    DROP_RANDOM_PROTOCOL = 2
    DROP_CURRENT_PROTOCOL = 3

    def __init__(self, maxEntries, droppingProtocol):
        self.maxEntries = maxEntries
        self.droppingProtocol = droppingProtocol
        self.data = []

    def printProperties(self):
        print 'Maximum number of entries:', self.maxEntries
        print 'Chosen dropping protocol:', self.droppingProtocol
        print '========'

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

    def isBufferFull(self):
        if self.maxEntries == len(self.data):
            return True
        else:
            return False

    def getData(self):
        data = self.data[0]
        del self.data[0]
        print 'Sent data:', data
        return data