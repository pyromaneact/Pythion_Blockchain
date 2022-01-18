import socket
import ooBlock
s = socket.socket()
host = '192.168.0.77'
port = 12345
clients=[]

chain1 = ooBlock.Chain()
chain1.addBlock('192.168.0.13')
chain1.addBlock('def')
chain1.addBlock('keep trying')


s.bind((host, port))
s.listen(5)
while True:
   print('flag')
   c, addr = s.accept()     # Establish connection with client.
   clients.append(addr[0])
   c.send(chain1.__get_chain_bytes__())
   c.close()  