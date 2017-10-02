import os
import sys
import time
import threading
from DataFactory import DataFactory
from DatabaseInterface import DatabaseInterface
from ConnectionManager import ConnectionManager

SERVER_ADDRESS = '172.24.1.1'
SID = 1
DATA_PORT = 10000
HELLO_PORT = 5000

TABLE_NAME = 'generated_sensor_data'
DATABASE_NAME = 'sdtn'
MYSQL_USER = 'sdtn'
MYSQL_PASSWORD = 'thesisit'

conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)
dbi = DatabaseInterface(TABLE_NAME, DATABASE_NAME, MYSQL_USER, MYSQL_PASSWORD)
dataFactory = DataFactory(5, 1, dbi)

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

def sendMessage(sock, pType, message):
    message = str(pType) + " " + str(SID) + " " + str(message[0]) + " " + str(message[1])
    print >> sys.stderr, 'Sending', message
    print ""
    sock.sendto(message, (SERVER_ADDRESS, DATA_PORT))

def processMessage(message):
    data = message.split()
    print "Type:", data[0], "SID:", data[1], "SEQ:", data[2], "Payload:", data[3], "\n"
    dbi.insertMessage(data)
    return True, int(data[0]), data[1], int(data[2])


def acknowledge(sock, sequenceNumber):
    acknowledgement = "0 " + str(sequenceNumber)
    sock.sendto(acknowledgement, ('172.24.1.1', DATA_PORT))
    print 'Sending', acknowledgement, "\n"

def main():

    dataSocket = conman.getDataSocket()

    while True:
        if not conman.isConnected():
            conman.listenForHello()
        time.sleep(2)
        try:
            sendMessage(dataSocket, 3, [1, ''])
            data, addr = dataSocket.recvfrom(4082)
            if data:
                print 'Received messaged:', data
                success, ptype, recvMessage, recvSeq = processMessage(data)
                if ptype != 1:
                    print "Expecting Type: 1, received Type:", ptype
                else:
                    acknowledge(dataSocket, recvSeq)
            else:
                print 'Disconnected?'
                break
        
        except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
            print "Not reachable\n"
    
def test():
    print "TEST MODE"
    conman = ConnectionManager(5, 'wlp2s0', 5000, 10000)

if __name__ == "__main__":
    main()