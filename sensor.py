import os
import sys
import time
import threading
import MySQLdb
from DataFactory import DataFactory
from ConnectionManager import ConnectionManager

SERVER_ADDRESS = '172.24.1.1'
SID = 1
DATA_PORT = 10000
HELLO_PORT = 5000

TABLE_NAME = 'generated_sensor_data'
DATABASE_NAME = 'sdtn'
MYSQL_USER = 'sdtn'
MYSQL_PASSWORD = 'thesisit'


def initializeDB():
    db = MySQLdb.connect('localhost', MYSQL_USER, MYSQL_PASSWORD, DATABASE_NAME)
    return db

def insertMessage(data):
    db = initializeDB()
    cursor = db.cursor()
    sql = "INSERT INTO generated_sensor_data (seq, payload) VALUES (" + data[0] + ", '" + data[1] + "' )"
    print sql
    try:
        print 'executing sql'
        cursor.execute(sql)
        print 'commiting db'        
        db.commit()
        print 'committed'
    except:
        print 'rollback'
        db.rollback()
    
    db.close()

def confirmAcknowledgement(sock, seq):
    sock.settimeout(5)

    try:
        data, addr = sock.recvfrom(16)
    except:
        sock.settimeout(None)
        return False

    sock.settimeout(None)

    print "Received message:", data
    data = data.split()
    ackSeq = int(data[1])
    pType = int(data[0])
    print "Message is Type:", pType, "Seq:", ackSeq, "\n"

    if pType != 0:
        return False
    elif ackSeq != seq:
        return False
    else:
        return True

def sendMessage(sock, seq):
    message = "1 " + str(SID) + " " + str(seq)
    print >> sys.stderr, 'Sending', message
    print ""
    sock.sendto(message, (SERVER_ADDRESS, DATA_PORT))

def main():
    conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)
    dataSocket = conman.getDataSocket()
    seq = 1
    failedAck = 0

    muleAddress = conman.listenForHello()

    while True:
        time.sleep(2)
        try:
            sendMessage(dataSocket, seq)
            if confirmAcknowledgement(dataSocket, seq):
                failedAck = 0
                seq += 1
            else: 
                failedAck += 1
                if failedAck == 5:
                    failedAck = 0
                    muleAddress = conman.listenForHello()
                continue
        
        except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
            failedAck += 1
            if failedAck == 5:
                failedAck = 0
                muleAddress = conman.listenForHello()
            print "Not reachable\n"
    
def test():
    print "TEST MODE"
    conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)

if __name__ == "__main__":
    main()