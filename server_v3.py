import socket
import sys
# import atexit
import threading
import time
import MySQLdb

SERVER_ADDRESS = '172.24.1.1'
BROADCAST_ADDRESS = '172.24.1.255'
CLIENT_ADDRESS = '172.24.1.3'
DATA_PORT = 10000
HELLO_PORT = 5000

TABLE_NAME = 'sensor_data'
DATABASE_NAME = 'sdtn'
MYSQL_USER = 'sdtn'
MYSQL_PASSWORD = 'password'

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
    print "Initialized DB"
    sql = "INSERT INTO sensor_data (sensor_id, seq) VALUES (" + data[1] + "," + data[2] + ")"
    print sql
    
    try:
        print "Executing SQL"
        cursor.execute(sql)
        print "Committing database"
        db.commit()
        print "Committed"
    except:
        db.rollback()
    
    db.close()
    

def processMessage(message):
    data = message.split()
    print "Type:", data[0], "SID:", data[1], "SEQ:", data[2], "\n"
    insertMessage(data)
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
    helloSocket = createSocket(BROADCAST_ADDRESS, HELLO_PORT)
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

def main():
    # atexit.register(exitHandler)
    sock = createSocket(SERVER_ADDRESS, DATA_PORT)

    helloThread = startHelloThread()
    
    awaitingSeq = 1

    try:
        while True:
            time.sleep(1)
            data, addr = sock.recvfrom(4082)
            if data:
                print 'Received messaged:', data
                success, ptype, recvMessage, recvSeq = processMessage(data)
                if ptype != 1:
                    print "Expecting Type: 1, received Type:", ptype
                elif recvSeq == awaitingSeq:
                    acknowledge(sock, awaitingSeq)
                    awaitingSeq += 1
            else:
                print 'Disconnected?'
                break
    except:
        exitHandler(sock)

def test():
    print "ENTERING TEST MODE"

if __name__ == "__main__":
    main()
