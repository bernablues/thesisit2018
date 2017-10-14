# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data

import time
import logging
from SDTNLogger import SDTNLogger

class DataFactory:
    
    def __init__(self, dataSize, timeToGenerate, sid, dataManager):
        self.DF_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')    
        self.DF_logger.classLog('Initializing DF...', 'INFO')

        self.dataManager = dataManager
        self.dataSize = dataSize
        self.timeToGenerate = timeToGenerate
        self.sid = sid

        # self.msg = 'DF initialized: data_size (in bytes):"+ %s+ "time_to_generate: "+%s "sid: "+ %r "data_mgr: "+ %r', self.dataSize, self.timeToGenerate, %self.sid, %self.dataManager
        # self.msg = ('DF initialized: data_size (in bytes): %(self.dataSize)s time_to_generate: %(self.timeToGenerate)s sid: %(self.sid)s data_mgr: %(self.dataManager)s')
        # self.msg = ('DF initialized: data_size (in bytes): '+ str(self.dataSize) +' time_to_generate: '+ str(self.timeToGenerate) +' sid: '+ str(self.sid) +' data_mgr: '+ str(self.dataManager))
        
        self.DF_logger.classLog('DF initialized: data_size (in bytes):,' + str(self.dataSize) + ',time_to_generate:,' + str(self.timeToGenerate) + ',sid:,' + str(self.sid) + ',data_mgr:,' + str(self.dataManager), 'INFO')

    def printProperties(self):
        print 'DATA FACTORY PROPERTIES:'
        print 'Size of data (in bytes):', self.dataSize
        print 'Time to generate data (in seconds):', self.timeToGenerate
        print '========'
        self.DF_logger.classLog('DATA FACTORY PROPERTIES:', 'INFO')
        self.DF_logger.classLog('Size of data (in bytes):,' + str(self.dataSize), 'INFO')
        self.DF_logger.classLog('Time to generate data (in seconds):,' + str(self.timeToGenerate), 'INFO')
        self.DF_logger.classLog('========,', 'INFO')

    def generateEntry(self):
        self.DF_logger.classLog('Generating entry:', 'INFO')
        payload = 'x' * self.dataSize
        entry = [str(self.sid), payload]
        self.DF_logger.classLog('Successfully generated entry.', 'INFO')
        self.DF_logger.classLog('Entry is,' + entry, 'DEBUG')
        
        return entry

    def pushEntry(self, entry):
        self.DF_logger.classLog('Pushing entry...', 'INFO')
        self.dataManager.insertData(entry)
        self.DF_logger.classLog('Successfully pushed entry.', 'INFO')
        return True        

    def start(self):
        self.DF_logger.classLog('Starting data factory...', 'INFO')
        while True:
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry()
            self.pushEntry(entry)
        self.DF_logger.classLog('Successfully ended data factory.', 'INFO')