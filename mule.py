import socket
import sys
# import atexit
import threading
import time
import MySQLdb
from ConnectionManager import ConnectionManager
from DatabaseInterface import DatabaseInterface

SERVER_ADDRESS = '172.24.1.1'
BROADCAST_ADDRESS = '172.24.1.255'
CLIENT_ADDRESS = '172.24.1.78'
DATA_PORT = 10000
HELLO_PORT = 5000
SID = 10

TABLE_NAME = 'sensor_data'
DATABASE_NAME = 'sdtn'
MYSQL_USER = 'sdtn'
MYSQL_PASSWORD = 'password'

conman = ConnectionManager(5, 'wlan0', 5000, 10000)
dbi = DatabaseInterface(TABLE_NAME, DATABASE_NAME, MYSQL_USER, MYSQL_PASSWORD)


def initializeDB():
    db = MySQLdb.connect('localhost', MYSQL_USER, MYSQL_PASSWORD, DATABASE_NAME)
    return db

def exitHandler(sock):
    sock.close()

def createSocket(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (address, port)
    print 'starting up on', server_address[0], ' port', server_address[1]
    sock.bind(server_address)

    return sock

def insertMessage(data):
    db = initializeDB()
    cursor = db.cursor()
    sql = "INSERT INTO sensor_data (sensor_id, seq, message) VALUES (" + data[1] + "," + data[2] + "," + data[3] +")"

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    
    db.close()

def sendMessage(sock, pType, message):
    message = str(pType) + " " + str(SID) + " " + str(message[0]) + " " + str(message[1])
    print >> sys.stderr, 'Sending', message
    print ""
    sock.sendto(message, ('172.24.1.78', DATA_PORT))
    

def processMessage(message):
    data = message.split()
    print "Type:", data[0], "SID:", data[1], "SEQ:", data[2], "\n"
    # dbi.insertMessage(data)
    return True, int(data[0]), data[1], int(data[2])

def acknowledge(sock, sequenceNumber):
    acknowledgement = "0 " + str(sequenceNumber)
    sock.sendto(acknowledgement, (CLIENT_ADDRESS, DATA_PORT))
    print 'Sending', acknowledgement, "\n"

def sendHello(sock):
    helloMessage = "2"

    while True:
        time.sleep(1)
        sock.sendto(helloMessage, (BROADCAST_ADDRESS, HELLO_PORT))

def initializeHelloThread():
    helloSocket = conman.getHelloSocket()
    helloSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    thread = threading.Thread(target=sendHello, args=(helloSocket,))
    thread.daemon = True

    print "Initialized hello thread."
    return thread

def startHelloThread():
    helloThread = initializeHelloThread()

    helloThread.start()
    print "Started hello thread."
    return helloThread

def confirmAcknowledgement(sock, message):
    terminated = False
    data = False
    while True:
        try:
            sock.settimeout(3)
            data, addr = sock.recvfrom(16) # throws exception when timeout
        except:
            sock.settimeout(None)
            terminated = conman.acknowledgementTimeout()
            
        if terminated:
            return False
        elif data:
            break
        else:
            sendMessage(sock, 1, message)
        
    print "Received message:", data
    data = data.split()
    ackSeq = int(data[1])
    pType = int(data[0])
    print "Message is Type:", pType, "Seq:", ackSeq, "\n"

    if pType != 0:
        return False
    elif ackSeq != message[0]:
        return False
    else:
        return True

def main():
    # atexit.register(exitHandler)
    sock = conman.getDataSocket()

    helloThread = startHelloThread()

    
    try:
        while True:
            time.sleep(1)
            data, addr = sock.recvfrom(4082)
            if data:
                print 'Received messaged:', data
                success, ptype, recvMessage, recvSeq = processMessage(data)
                if ptype == 3:
                    while True:
                        time.sleep(1)
                        sendMessage(sock, 1, '1 x')
                        confirmAcknowledgement(sock, '1 x')
                elif ptype != 1:
                    print "Expecting Type: 1, received Type:", ptype
                else:
                    acknowledge(sock, recvSeq)
            else:
                print 'Disconnected?'
                break
    except:
        exitHandler(sock)

def test():
    print "ENTERING TEST MODE"

if __name__ == "__main__":
    main()
