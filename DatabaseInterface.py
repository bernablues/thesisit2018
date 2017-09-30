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
            print "Inserted", data, "on DB" 
        except:
            print 'DB Rollback'
            db.rollback()
        
        db.close()

    # def getRowCount
    # def getData