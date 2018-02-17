# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time
import datetime

class DataFactory:
    def __init__(self, dataSize, timeToGenerate, sid, dataManager, experiments=None):
        self.dataManager = dataManager
        self.dataSize = dataSize
        self.timeToGenerate = timeToGenerate
        self.sid = sid

        self.seqNumber = 0

    def printProperties(self):
        print 'DATA FACTORY PROPERTIES:'
        print 'Size of data (in bytes):', self.dataSize
        print 'Time to generate data (in seconds):', self.timeToGenerate
        print '========'

    def generateEntry(self):
        data = 'x' * self.dataSize
        timestamp = str(datetime.datetime.now())
        entry = [timestamp, str(self.seqNumber), data]
        self.seqNumber += 1

        if self.seqNumber == 1000:
            self.seqNumber = 0
        
        return entry

    def pushEntry(self, entry):
        self.dataManager.insertData(entry)
        return True        

    def start(self):
        while True:
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry()
            self.pushEntry(entry)