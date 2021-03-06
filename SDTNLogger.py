import logging
from datetime import datetime, timedelta

class SDTNLogger:

# https://docs.python.org/2/howto/logging-cookbook.html
    def __init__(self, className, experiments, degreeLevel):

        # # =====================
        # # Outputs to file only

        # self.className = className
        # self.className_logger = self.className+'_logger'
        # self.degreeLevel = degreeLevel

        # format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # classLog_filename = './logs/Class_logs/'+self.className+'.log'
        # logging.basicConfig(filename=classLog_filename, level=self.degreeLevel, format=format_string)

        # self.className_logger = logging.getLogger(__name__)
        # self.className_logger.setLevel(logging.INFO)
        # # =====================


        # =====================
        # Outputs to multiple files simultaneously
        # No explicit switch cases

        self.formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
        currDate=datetime.now()
        currDateTime=currDate.strftime('%Y-%m-%d %H:%M:%S')

        self.degreeLevel = degreeLevel

        self.className = className
        self.className_logger = self.className+'_logger'

        class_filename = './logs/Class_logs/'+str(currDate)+'_'+self.className+'.csv'
        self.class_handler = logging.FileHandler(class_filename)
        self.class_handler.setFormatter(self.formatter)

        self.className_logger = logging.getLogger(self.className)
        self.className_logger.setLevel(logging.INFO)
        self.className_logger.addHandler(self.class_handler)

        if experiments:
            for experiment in experiments:
                self.experiment = experiment
                self.experiment_logger = self.experiment+'_logger'
                expt_filename = './logs/Experiment_logs/'+self.experiment+'.csv'
                expt_handler = logging.FileHandler(expt_filename)        
                expt_handler.setFormatter(self.formatter)
                self.className_logger.addHandler(expt_handler)

        dropDataTable_filename = './logs/Table_logs/'+str(currDate)+'_'+'dropDataTable_.csv'
        dropDataTable_handler = logging.FileHandler(dropDataTable_filename)        
        dropDataTable_handler.setFormatter(self.formatter)

        dropDataTable_logger = logging.getLogger(dropDataTable_filename)
        dropDataTable_logger.setLevel(logging.INFO)
        dropDataTable_logger.addHandler(dropDataTable_handler)

        sendDataTable_filename = './logs/Table_logs/'+str(currDate)+'_'+'sendDataTable_.csv'
        sendDataTable_handler = logging.FileHandler(sendDataTable_filename)        
        sendDataTable_handler.setFormatter(self.formatter)

        sendDataTable_logger = logging.getLogger(sendDataTable_filename)
        sendDataTable_logger.setLevel(logging.INFO)
        sendDataTable_logger.addHandler(sendDataTable_handler)




        # Bawal magkaiba ng degree level yung classLog and experimentLog if ganitong implementation
        # =====================


        # # =====================
        # # Outputs to multiple files only
        # # Explicit switch cases

        # self.className = className
        # self.className_logger = self.className+'_logger'
        # self.experiments = experiments
        # self.degreeLevel = degreeLevel

        # format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # classLog_filename = './logs/Class_logs/'+self.className+'.log'
        # logging.basicConfig(filename=classLog_filename, level=self.degreeLevel, format=format_string)

        # self.className_logger = logging.getLogger(__name__)
        # self.className_logger.setLevel(logging.INFO)

        # for experiment in experiments:
        #     self.experiment = experiment
        #     self.experiment_logger = self.experiment+'_logger'

        #     expt_filename = './logs/Experiment_logs/'+self.experiment+'.log'
        #     expt_handler = logging.FileHandler(expt_filename)        
        #     expt_handler.setFormatter(formatter)

        #   #  # self.className_logger.addHandler(expt_handler)


        # =====================


        # # =====================
        # # Outputs to both console and file
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

        # Pwede magkaiba ng degree level yung classLog and experimentLog if ganitong implementation

        # # =====================

    def printProperties(self):
        print 'className_logger: ', self.className_logger
        print 'className_handler: ', self.class_handler
        print 'className_formatter: ', self.formatter
        print 'degreeLevel: ', self.degreeLevel

    def classLog(self, message, level):

        # if expt not null, call experimentLog()

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


    def experimentLog(self, message, level):

        if level == 'DEBUG':
            self.experiment_logger.debug('%s', message)
        elif level == 'INFO':
            self.experiment_logger.info('%s', message)

        elif level == 'WARNING':
            self.experiment_logger.warning('%s', message)

        elif level == 'ERROR':
            self.experiment_logger.error('%s', message)

        else:
            self.experiment_logger.critical('%s', message)


# trialLogger = SDTNLogger('clsname', ['expt1','expt2'], 'INFO')
# trialLogger.printProperties()
# trialLogger.classLog("trial log msg", 'INFO')
