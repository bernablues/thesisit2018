import socket
import sys
import atexit

SERVER_ADDRESS = '172.24.1.1'
CLIENT_ADDRESS = '172.24.1.3'
PORT = 10000


def exitHandler(sock):
    sock.close()

def createSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (SERVER_ADDRESS, PORT)
    print 'starting up on', server_address[0], ' port', server_address[1]
    sock.bind(server_address)

    return sock

def processMessage(message):
    data = message.split()
    print "Type:", data[0], "SID:", data[1], "SEQ:", data[2], "\n"
    return True, int(data[0]), data[1], int(data[2])

def acknowledge(sock, sequenceNumber):
    acknowledgement = "0 " + str(sequenceNumber)
    sock.sendto(acknowledgement, (CLIENT_ADDRESS, PORT))
    print 'Sending', acknowledgement, "\n"

def main():
    atexit.register(exitHandler)
    sock = createSocket()

    awaitingSeq = 1

    while True:

        try:

            while True:
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

if __name__ == "__main__":
    main()
