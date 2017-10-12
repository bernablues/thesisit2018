import MySQLdb
import logging
from SDTNLogger import SDTNLogger


class DatabaseInterface:

    def __init__(self, table, database, user, password):
        self.DBI_logger = SDTNLogger(self.__class__.__name__, ['W1','W2'], 'INFO')    
        self.DBI_logger.classLog('Initializing DBI...', 'INFO')

        self.table = table
        self.database = database
        self.user = user
        self.password = password

        # self.DBI_logger.info('DBI initialized: db_name: %s table_name: %s user: %s', database, table, user)
        self.DBI_logger.classLog('DBI initialized: db_name: ' + str(self.database) + ' table_name: ' + str(self.table) + ' user: ' + str(self.user), 'INFO') 

    def __openDatabase(self):
        db = MySQLdb.connect('localhost', self.user, self.password, self.database)
        self.DBI_logger.classLog('Opening db: ' + str(self.database) + ' localhost: ' + str(self.user), 'INFO')        
        return db

    def insertRow(self, data):
        db = self.__openDatabase()
        cursor = db.cursor()
        # To be improved, assumes column names. Could use dictionaries for key->value pairs.
        sql = "INSERT INTO " + self.table + " (sid, payload) VALUES (" + data[0] + ", '" + data[1] + "' )"

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)                                                                                                                                             
            self.DBI_logger.classLog('Successfully executed SQL command: ' + sql, 'INFO')

            self.DBI_logger.classLog('Committing to db...', 'INFO')
            db.commit()
            self.DBI_logger.classLog('Successfully committed to db.', 'INFO')
        except:
            self.DBI_logger.classLog('DB Rollback', 'WARNING')
            print 'DB Rollback'
            db.rollback()
        
        self.DBI_logger.classLog('Closing db.', 'INFO')
        db.close()

    def getRowCount(self):
        db = self.__openDatabase()
        cursor = db.cursor()

        self.DBI_logger.classLog('Getting row count from db...', 'INFO')
        sql = "SELECT COUNT(*) FROM " + self.table

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)
            self.DBI_logger.classLog('Successfully executed SQL command: ' + sql, 'INFO')

            results = cursor.fetchone()

            self.DBI_logger.classLog('Row count: ' + str(results), 'INFO')


        except:
            print "DB Error"
            self.DBI_logger.classLog('DB Error: getting row count', 'WARNING')
            
        self.DBI_logger.classLog('Closing db.','INFO')
        db.close()

        return results[0]

    def getRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        self.DBI_logger.classLog('Getting rows from db...', 'INFO')
        sql = "SELECT sid, payload FROM " + self.table

        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)
            self.DBI_logger.classLog('Successfully executed SQL command: '+ sql, 'INFO')

            results = cursor.fetchall()
            self.DBI_logger.classLog('Rows: ' + str(results), 'INFO' )

        except:
            print "DB Error"
            self.DBI_logger.classLog('DB Error: getting row count', 'WARNING')

        self.DBI_logger.classLog('Closing db.','INFO')
        db.close()

        return results

    def getNthRow(self, n):
        db = self.__openDatabase()
        cursor = db.cursor()

        self.DBI_logger.classLog('Getting nth (' + n + ') row from db...', 'INFO')
        sql = "SELECT sid, payload FROM " + self.table
        sql = "SELECT * FROM " + self.table + " ORDER BY id LIMIT n-1,1"

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)
            self.DBI_logger.classLog('Successfully executed SQL command: '+ sql,'INFO')

            results = cursor.fetchall()
            self.DBI_logger.classLog('Rows: ' + str(results), 'INFO' )

        except:
            print "DB Error"
            self.DBI_logger.classLog('DB Error: getting nth row', 'WARNING')

        self.DBI_logger.classLog('Closing db.', 'INFO')
        db.close()

        return results

    def getAllRows(self, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        self.DBI_logger.classLog('Getting all rows from db...', 'INFO')
        sql = "SELECT sid, payload FROM " + self.table

        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)
            self.DBI_logger.classLog('Successfully executed SQL command: ' + sql, 'INFO')

            results = cursor.fetchall()
            self.DBI_logger.classLog('Rows: ' + str(results), 'INFO')
        except:
            print "DB Error"
            self.DBI_logger.classLog('Getting all rows from db...', 'WARNING')

        self.DBI_logger.classLog('Closing db.', 'INFO')
        db.close()

        return results

    def deleteRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        self.DBI_logger.classLog('Deleting n (' + str(numberOfRows) + ') row from db...', 'INFO')
        sql = "DELETE FROM " + self.table 

        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            self.DBI_logger.classLog('Executing SQL command: ' + sql, 'INFO')
            cursor.execute(sql)
            self.DBI_logger.classLog('Successfully executed SQL command: '+ sql, 'INFO')

            self.DBI_logger.classLog('Committing to db.', 'INFO')
            db.commit()
            self.DBI_logger.classLog('Successfully committed to db.', 'INFO')

        except:
            self.DBI_logger.classLog('DB rollback', 'WARNING')
            db.rollback()
            self.DBI_logger.classLog('Deleting n (' + str(numberOfRows) + ') rows from db.', 'WARNING')
            print "DB Error"

        self.DBI_logger.classLog('Closing db.', 'INFO')
        db.close()
