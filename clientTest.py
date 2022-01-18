import socket               # Import socket module
import ooBlock
s = socket.socket()         # Create a socket object
host = '192.168.0.77' # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
bytechain=s.recv(1024)
chain1=ooBlock.Chain(byte=bytechain)
print(bytechain)
print(chain1.chain[0].data)
s.close()                     # Close the socket when done