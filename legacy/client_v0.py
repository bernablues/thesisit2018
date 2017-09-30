import socket
import os
import sys
import time
import atexit

hostname = '172.24.1.1'
port = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def exit_handler():
    sock.close()

def ping(time):
    response = os.system("timeout " + str(time) + " ping -c 1 " + hostname + " > /dev/null 2>&1")

    if response == 0:
        return True
    else:
        print "Not nearby"
        return False

def connectSocket():
    server_address = (hostname, port)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

def main():
    atexit.register(exit_handler)

    seq = 1
    openSocket = False
    while True:
        inRange = ping(1)
        if inRange:
            if not openSocket:
                connectSocket()
                openSocket = True
            while True:
                time.sleep(2)
                # if ping(0.1):
                # try:
                message = "SID: 1, SEQ:" + str(seq)
                print >> sys.stderr, 'sending', message
                sock.send(message)

                seq += 1
                
                # except: 
                #     exit_handler()
                    # break
                # else:
                    # break
    
        
if __name__ == "__main__":
    main()