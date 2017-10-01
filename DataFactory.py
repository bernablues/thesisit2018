# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time

class DataFactory:
    def __init__(self, dataSize, timeToGenerate, dbInterface):
        self.dbInterface = dbInterface
        self.dataSize = dataSize
        self.timeToGenerate = timeToGenerate
        self.data = []

    def printProperties(self):
        print 'DATA FACTORY PROPERTIES:'
        print 'Size of data (in bytes):', self.dataSize
        print 'Time to generate data (in seconds):', self.timeToGenerate
        print '========'

    def generateEntry(self, seq):
        payload = 'x' * self.dataSize
        entry = [str(seq), payload]
        return entry

    def pushEntry(self, entry):
        self.dbInterface.insertMessage(entry)
        return True        

    def start(self):
        seq = 1

        while True:
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry(seq)
            seq += 1
            self.pushEntry(entry)