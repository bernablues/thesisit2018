import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5000))

while True:
    bundle, fromSocket = sock.recvfrom(1024)
    print bundle
    time.sleep(3)