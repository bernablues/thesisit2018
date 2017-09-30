import socket
import sys
import atexit

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('172.24.1.1', 10000)
print 'starting up on', server_address[0], ' port', server_address[1]
sock.bind(server_address)

# sock.listen(1)

def exit_handler():
    sock.close()

atexit.register(exit_handler)

while True:
    # print 'waiting for a connection'
    # connection, client_address = sock.accept()

    try:
        # print 'connection from', client_address

        while True:
            data = sock.recvfrom(16, ('172.24.1.3', 10000))
            if data:
                print 'received', data
            else:
                print 'Disconnected?'
    except:
        exit_handler()