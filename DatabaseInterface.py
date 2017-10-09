import MySQLdb
import logging

logging.basicConfig(level=logging.DEBUG)
DBI_logger = logging.getLogger(__name__)

DBI_logger.setLevel(logging.INFO)

# create a file handler
DBI_handler = logging.FileHandler(__name__)
DBI_handler.setLevel(logging.INFO)

# create a logging format
DBI_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
DBI_handler.setFormatter(DBI_formatter)

# add the handlers to the logger
DBI_logger.addHandler(DBI_handler)


class DatabaseInterface:
    def __init__(self, table, database, user, password):
        DBI_logger.info('Initializing DBI...')

        self.table = table
        self.database = database
        self.user = user
        self.password = password

        DBI_logger.info('DBI initialized: db_name: %s table_name: %s user: %s', database, table, user)

    def __openDatabase(self):
        db = MySQLdb.connect('localhost', self.user, self.password, self.database)
        DBI_logger.info('Opening db: %s localhost: %s', self.database, self.user)
        return db

    def insertRow(self, data):
        db = self.__openDatabase()
        cursor = db.cursor()
        # To be improved, assumes column names. Could use dictionaries for key->value pairs.
        sql = "INSERT INTO " + self.table + " (sid, payload) VALUES (" + data[0] + ", '" + data[1] + "' )"

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)                                                                                                                                             
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            DBI_logger.info('Committing to db: %s', self)
            db.commit()
            DBI_logger.info('Successfully committed to db: %s', self)
        except:
            DBI_logger.warning('DB (%s) Rollback', self)
            print 'DB Rollback'
            db.rollback()
        
        DBI_logger.info('Closing db: %s', self)
        db.close()

    def getRowCount(self):
        db = self.__openDatabase()
        cursor = db.cursor()

        DBI_logger.info('Getting row count from db: %s', self)
        sql = "SELECT COUNT(*) FROM " + self.table

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            results = cursor.fetchone()

            DBI_logger.info('Row count: %s', results)


        except:
            print "DB Error"
            DBI_logger.warning('DB Error: getting row count')
            
        DBI_logger.info('Closing db: %s', self)
        db.close()

        return results[0]

    def getRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        DBI_logger.info('Getting rows from db: %s', self)
        sql = "SELECT sid, payload FROM " + self.table

        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            results = cursor.fetchall()
            DBI_logger.info('Rows: %s', results)

        except:
            print "DB Error"
            DBI_logger.warning('DB Error: getting row count')
            
        DBI_logger.info('Closing db: %s', self)
        db.close()

        return results

    def getNthRow(self, n):
        db = self.__openDatabase()
        cursor = db.cursor()

        DBI_logger.info('Getting nth (%s) row from db: %s', n, self)
        sql = "SELECT sid, payload FROM " + self.table
        sql = "SELECT * FROM " + self.table + " ORDER BY id LIMIT n-1,1"

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            results = cursor.fetchall()
            DBI_logger.info('Rows: %s', results)

        except:
            print "DB Error"
            DBI_logger.warning('DB Error: getting nth row')
            
        DBI_logger.info('Closing db: %s', self)
        db.close()

        return results

    def getAllRows(self, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()


        DBI_logger.info('Getting all rows from db: %s', self)
        sql = "SELECT sid, payload FROM " + self.table
        
        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            results = cursor.fetchall()
            DBI_logger.info('Rows: %s', results)
        except:
            print "DB Error"
            DBI_logger.warning('Getting all rows from db: %s', self)

        DBI_logger.info('Closing db: %s', self)
        db.close()

        return results

    def deleteRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        DBI_logger.info('Deleting n (%s) rows from db: %s', numberOfRows, self)
        sql = "DELETE FROM " + self.table 
        
        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            DBI_logger.info('Executing SQL command: %s', sql)
            cursor.execute(sql)                                                                                                                                             
            DBI_logger.info('Successfully executed SQL command: %s', sql)

            DBI_logger.info('Committing to db: ', self)
            db.commit()
            DBI_logger.info('Successfully committed to db: ', self)

        except:

            DBI_logger.warning('DB (%s) rollback', self)
            db.rollback()
            DBI_logger.warning('Deleting n (%s) rows from db: %s', numberOfRows, self)
            print "DB Error"

        DBI_logger.info('Closing db: %s', self)
        db.close()