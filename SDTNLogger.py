import logging

class SDTNLogger:


    # logging.basicConfig(level=logging.DEBUG)
    # DF_logger = logging.getLogger(__name__)

    # DF_logger.setLevel(logging.INFO)

    # # create a file handler
    # DF_handler = logging.FileHandler('DF.log')
    # DF_handler.setLevel(logging.INFO)

    # # create a logging format
    # DF_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # DF_handler.setFormatter(DF_formatter)

    # add the handlers to the logger

    def __init__(self, className, experiment, degreeLevel):
        # Output to file only
        # =====================

        self.className = className
        self.className_logger = self.className+'_logger'
        self.degreeLevel = degreeLevel

        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_filename = './logs/Class_logs/'+self.className+'.log'
        logging.basicConfig(filename=log_filename, level=self.degreeLevel, format=format_string)

        self.className_logger = logging.getLogger(__name__)
        self.className_logger.setLevel(logging.INFO)
        # =====================


        # # Output to console and file
        # # =====================
        # self.className = className
        # self.className_logger = self.className+'_logger'
        # self.className_handler = self.className+'_handler'
        # self.className_formatter = self.className+'_formatter'
        # self.degreeLevel = degreeLevel

        # logging.basicConfig(level=self.degreeLevel)

        # self.className_logger = logging.getLogger(__name__)
        # self.className_logger.setLevel(logging.INFO)

        # self.className_handler = logging.FileHandler('./logs/Class_logs/'+self.className+'.log')
        # self.className_handler.setLevel(logging.INFO)

        # # instantiate an experiment handler here

        # self.className_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # self.className_handler.setFormatter(self.className_formatter)

        # self.className_logger.addHandler(self.className_handler)
        # # add the experiment handler here

        # # =====================

    def printProperties(self):
        print 'className_logger: ', self.className_logger
        # print 'className_handler: ', self.className_handler
        # print 'className_formatter: ', self.className_formatter
        print 'degreeLevel: ', self.degreeLevel

    def loglog(self, message, level):

        if level == 'DEBUG':
            self.className_logger.debug('%s', message)
        elif level == 'INFO':
            self.className_logger.info('%s', message)

        elif level == 'WARNING':
            self.className_logger.warning('%s', message)

        elif level == 'ERROR':
            self.className_logger.error('%s', message)

        else:
            self.className_logger.critical('%s', message)

    # def __classLogger(self, message, level):

    #     def zero():
    #         return "zero"

    #     def one():
    #         return "one"

    #     def numbers_to_functions_to_strings(argument):
    #         switcher = {
    #             0: zero,
    #             1: one,
    #             2: lambda: "two",
    #         }
    #         # Get the function from switcher dictionary
    #         func = switcher.get(argument, lambda: "nothing")
    #         # Execute the function
    #         return func()

    #     switch degreeLevel:

    #     case debug:
    #         self.className_logger('')
    #     case info:          case
    #     case warning:
    #     case error:
    #     case critical:

    # def __experimentLogger(self, message, level):


    # class A:
    #     def __init__(self):
    #         pass

    #     def sampleFunc(self, arg):
    #         print('you called sampleFunc({})'.format(arg))

    # m = globals()['A']()
    # func = getattr(m, 'sampleFunc')
    # func('sample arg')

    # # Sample, all on one line
    # getattr(globals()['A'](), 'sampleFunc')('sample arg')

    # self.ConMan_logger.info('ConMan initialized: max_ack_timeout: %s hello_port: %s data_port: %s own_IP_addr: %s ')



trialLogger = SDTNLogger('please', None, 'INFO')

# trialLogger.printProperties()

trialLogger.loglog("trial log msg", 'INFO')

