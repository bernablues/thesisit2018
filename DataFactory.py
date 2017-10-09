# Data generator with parameters of
# # size of data in bytes,
# number of entries possible,
# dropping protocol to be used (First, Last, Random, Current),
# number of seconds to generate new entry,
# number of seconds to send data
import time
import logging

logging.basicConfig(level=logging.DEBUG)
DF_logger = logging.getLogger(__name__)

DF_logger.setLevel(logging.INFO)

# create a file handler
DF_handler = logging.FileHandler('DF.log')
DF_handler.setLevel(logging.INFO)

# create a logging format
DF_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
DF_handler.setFormatter(DF_formatter)

# add the handlers to the logger
DF_logger.addHandler(DF_handler)

class DataFactory:
    def __init__(self, dataSize, timeToGenerate, sid, dataManager):
        self.DF_logger.info('Initializing DF')
        
        self.dataManager = dataManager
        self.dataSize = dataSize
        self.timeToGenerate = timeToGenerate
        self.sid = sid

        self.DF_logger.info('DF initialized: data_size (in bytes): %s time_to_generate: %s sid: %s data_mgr: %s', dataSize, timeToGenerate, sid, dataManager)

    def printProperties(self):
        print 'DATA FACTORY PROPERTIES:'
        print 'Size of data (in bytes):', self.dataSize
        print 'Time to generate data (in seconds):', self.timeToGenerate
        print '========'
        self.DF_logger.info('DATA FACTORY PROPERTIES:')
        self.DF_logger.info('Size of data (in bytes):', self.dataSize)
        self.DF_logger.info('Time to generate data (in seconds):', self.timeToGenerate)
        self.DF_logger.info('========')

    def generateEntry(self):
        self.DF_logger.info('Generating entry:')
        payload = 'x' * self.dataSize
        entry = [str(self.sid), payload]
        self.DF_logger.info('Successfully generated entry: %s', entry)
        return entry

    def pushEntry(self, entry):
        self.DF_logger.info('Pushing entry: %s',entry)
        self.dataManager.insertData(entry)
        self.DF_logger.info('Successfully pushed entry: %s',entry)
        return True        

    def start(self):
        self.DF_logger.info('Starting data factory...')
        while True:
            time.sleep(self.timeToGenerate)
            entry = self.generateEntry()
            self.pushEntry(entry)
        self.DF_logger.info('Ended data factory...')
        