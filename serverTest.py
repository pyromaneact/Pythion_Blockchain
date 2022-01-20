import socket
import ooBlock

host = socket.gethostname()
port = 12345
clients=[]
start = input('are You the first server 1,0?:')

if start == 1:
    chain1.addBlock('192.168.0.13')
    chain1.addBlock('def')
    chain1.addBlock('keep trying')
else:
    s = socket.socket()
    s.connect(('192.168.0.77', port))
    s.send(b'request')
    chain1bytes = s.recv(1024)
    chain1 = ooBlock.Chain(byte=chain1bytes)
    s.close()

s = socket.socket()
s.bind((host, port))
s.listen(5)

while True:
    print('flag')
    c, addr = s.accept()
    conectionType = c.recv(1024)
    if conectionType == b'request':
        clients.append(addr[0])
        c.send(chain1.__get_chain_bytes__())
        c.close()


    elif conectionType == b'data':
        data = c.recv(1024)
        data = data.decode("utf-8")
        c.close()
        chain1.addBlock(data)
        newsocket = socket.socket()
        for ip in clients:  
            newsocket.connect((ip, port))
            newsocket.send(b'newChain')
            newsocket.send(chain1.__get_chain_bytes__())
            

    elif conectionType == b'newChain':
        newChainBytes = c.recv(1024)
        c.close()
        chain2 = Chain(byte=newChainBytes)
        if chain1.same_chain(chain2):
            chain1 = chain2.best_chain(chain1)
        for ip in clients:  
            newsocket.connect((ip, port))
            newsocket.send(b'newChain')
            newsocket.send(chain1.__get_chain_bytes__())
    c.close()