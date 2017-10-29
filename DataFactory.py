# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time
import datetime
import logging
from SDTNLogger import SDTNLogger

class DataFactory:
    def __init__(self, dataSize, timeToGenerate, sid, dataManager, experiments=None):
        self.DF_logger = SDTNLogger(self.__class__.__name__, experiments, 'INFO')
        self.DF_logger.classLog('Initializing DF...', 'INFO')

        self.dataManager = dataManager
        self.dataSize = dataSize
        self.timeToGenerate = timeToGenerate
        self.sid = sid

        self.seqNumber = 0

        self.DF_logger.classLog('DF initialized:,DATA_SIZE (in bytes):,' + str(self.dataSize) + ',TIME_TO_GENERATE:,' + str(self.timeToGenerate) + ',SID:,' + str(self.sid) + ',DATA_MGR:,' + str(self.dataManager), 'INFO')

    def printProperties(self):
        print 'DATA FACTORY PROPERTIES:'
        print 'Size of data (in bytes):', self.dataSize
        print 'Time to generate data (in seconds):', self.timeToGenerate
        print '========'
        self.DF_logger.classLog('DATA FACTORY PROPERTIES:', 'INFO')
        self.DF_logger.classLog('DATA_SIZE (in bytes):,' + str(self.dataSize), 'INFO')
        self.DF_logger.classLog('TIME_TO_GENERATE (in seconds):,' + str(self.timeToGenerate), 'INFO')
        self.DF_logger.classLog('========,', 'INFO')

    def generateEntry(self):
        self.DF_logger.classLog('Generating ENTRY:', 'INFO')
        data = 'x' * self.dataSize
        timestamp = str(datetime.datetime.now())
        entry = [timestamp, self.seqNumber, data]
        self.seqNumber += 1

        if self.seqNumber == 1000:
            self.seqNumber = 0
        
        self.DF_logger.classLog('Successfully generated ENTRY.', 'INFO')
        self.DF_logger.classLog('Entry is:,' + str(entry), 'DEBUG')

        return entry

    def pushEntry(self, entry):
        self.DF_logger.classLog('Pushing ENTRY...', 'INFO')
        self.dataManager.insertData(entry)
        self.DF_logger.classLog('Successfully pushed ENTRY.', 'INFO')
        return True        

    def start(self):
        self.DF_logger.classLog('Starting data factory...', 'INFO')
        while True:
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry()
            self.pushEntry(entry)
        self.DF_logger.classLog('Successfully ended data factory.', 'INFO')