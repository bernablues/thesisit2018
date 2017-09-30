import socket
import os
import sys
import time
import atexit
import threading
import MySQLdb
from DataFactory import DataFactory

SERVER_ADDRESS = '172.24.1.1'
CLIENT_ADDRESS = '172.24.1.78'
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

def createSocket(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((address, port))
    return sock

def exitHandler(sock):
    sock.close()

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

def listenForHello():
    helloSocket = createSocket('', HELLO_PORT)
    print "Listening for hello..."
    data, addr = helloSocket.recvfrom(4)
    print "Received hello:", data, 'from', addr
    return True

def main():
    atexit.register(exitHandler)

    dataSocket = createSocket(CLIENT_ADDRESS, DATA_PORT)
    seq = 1
    failedAck = 0

    listenForHello()

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
                    listenForHello()
                continue
        
        except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
            failedAck += 1
            if failedAck == 5:
                failedAck = 0
                listenForHello()
            print "Not reachable\n"
    
def test():
    print "TEST MODE"
    factory = DataFactory(4, 5, DataFactory.DROP_RANDOM_PROTOCOL, 1)
    factory.printProperties()
    thread = threading.Thread(target=factory.start)
    thread.daemon = True
    thread.start()

    while True:
        time.sleep(5)
        data = factory.getData()
        data = data.split()
        db = initializeDB()
        insertMessage(data)        
if __name__ == "__main__":
    test()

# Unused functions

def ping(time):
    response = os.system("timeout " + str(time) + " ping -c 1 " + CLIENT_ADDRESS + " > /dev/null 2>&1")

    if response == 0:
        return True
    else:
        print "Not nearby"
        return False

def connectSocket(sock, address, port):
    server_address = (address, port)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)