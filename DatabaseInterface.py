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

    def insertMessage(self, data):
        db = self.__openDatabase()
        cursor = db.cursor()
        # To be improved, assumes column names. Could use dictionaries for key->value pairs.
        sql = "INSERT INTO " + self.table + " (seq, payload) VALUES (" + data[0] + ", '" + data[1] + "' )"
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

        return results

    def getData(self, numberOfRows):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "SELECT seq, payload FROM " + self.table + " LIMIT " + str(numberOfRows)

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print "DB Error"

        db.close()

        return results

    def deleteData(self, numberOfRows):
        db = self.__openDatabase()
        cursor = db.cursor()

        sql = "DELETE FROM " + self.table + " LIMIT " + str(numberOfRows)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print "DB Error"

        db.close()