import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# logger.info('Start reading database')
# # read database here
# records = {'john': 55, 'tom': 66}
# logger.debug('Records: %s', records)
# logger.info('Updating records ...')
# # update records here
# logger.info('Finish updating records')



# ==========================
# logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(__name__)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('try another')

anotherhandler = logging.FileHandler('hi.log')
anotherhandler.setLevel(logging.INFO)

# create a logging format
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
anotherhandler.setFormatter(formatter2)

# add the handlers to the logger
logger.addHandler(anotherhandler)

logger.info('tried another')
