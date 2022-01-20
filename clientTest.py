import socket               # Import socket module
import ooBlock
import time
s = socket.socket()         # Create a socket object
host = '192.168.0.77' # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
s.send(b'1')
print(s.recv(1024))
s.close()                     # Close the socket when done