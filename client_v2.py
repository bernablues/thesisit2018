import socket
import os
import sys
import time
import atexit

SERVER_ADDRESS = '172.24.1.1'
CLIENT_ADDRESS = '172.24.1.78'
SID = 1
PORT = 10000

def initializeSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((CLIENT_ADDRESS, PORT))
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

def testSplittingPoint(sock):
    message = "~" * 65507
    print "Sending:", message
    sock.sendto(message, (SERVER_ADDRESS, PORT))

def sendMessage(sock, seq):
    message = "1 " + str(SID) + " " + str(seq)
    print >> sys.stderr, 'Sending', message
    print ""
    sock.sendto(message, (SERVER_ADDRESS, PORT))

def main():
    atexit.register(exitHandler)

    sock = initializeSocket()
    seq = 1

    while True:
        time.sleep(5)
        try:
            sendMessage(sock, seq)
            if confirmAcknowledgement(sock, seq):
                seq += 1
            else: 
                continue
        
        except: #usually triggers on no network reachable eg. wifi off or reconnecting and ctrl c
            print "Not reachable\n"
    
def test():
    print "TEST MODE"
    sock = initializeSocket()

    time.sleep(1)
    testSplittingPoint(sock)
        
if __name__ == "__main__":
    main()

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