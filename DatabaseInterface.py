import MySQLdb

class DatabaseInterface:
    def __init__(self, table, database, user, password):
        self.table = table
        self.database = database
        self.user = user
        self.password = password

    def __openDatabase(self):
        db = MySQLdb.connect('localhost', self.user, self.password, self.database)
        return db

    def insertRow(self, data):
        db = self.__openDatabase()
        cursor = db.cursor()
        # To be improved, assumes column names. Could use dictionaries for key->value pairs.
        sql = "INSERT INTO " + self.table + " (sid, payload) VALUES (" + data[0] + ", '" + data[1] + "' )"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print 'DB Rollback'
            db.rollback()
        
        db.close()

    def getRowCount(self):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "SELECT COUNT(*) FROM " + self.table

        try:
            cursor.execute(sql)
            results = cursor.fetchone()
        except:
            print "DB Error"

        db.close()

        return results[0]

    def getRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "SELECT sid, payload FROM " + self.table

        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print "DB Error"

        db.close()

        return list(results)

    def getNthRow(self, n):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "SELECT sid, payload FROM " + self.table
        sql = "SELECT * FROM " + self.table + " ORDER BY id LIMIT n-1,1"

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print "DB Error"

        db.close()

        return list(results)

    def getAllRows(self, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "SELECT sid, payload FROM " + self.table
        
        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print "DB Error"

        db.close()

        return list(results)

    def deleteRows(self, numberOfRows, isReversed = False):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "DELETE FROM " + self.table 
        
        if isReversed:
            sql = sql + ' ORDER BY id DESC'

        sql = sql + " LIMIT " + str(numberOfRows)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "DB Error"

        db.close()