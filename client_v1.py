import socket
import os
import sys
import time
import atexit

hostname = '172.24.1.1'
port = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    sock.settimeout(5)
    while True:
        time.sleep(2)
        # try:
        message = "SID: 1, SEQ:" + str(seq)
        print >> sys.stderr, 'sending', message
        sock.sendto(message, (hostname,port))
        print "test"
        seq += 1
        
        # except: 
        #     exit_handler()
        #     break
    
        
if __name__ == "__main__":
    main()