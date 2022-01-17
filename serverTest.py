import socket  
s = socket.socket()
host = '192.168.0.77'
port = 12345
s.bind((host, port))
s.listen(5)
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from, '+ addr)
   c.send('Thank you for connecting')
   c.close()  