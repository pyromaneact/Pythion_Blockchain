import socket
import ooBlock
import threading

def chainNetwork(port, host):
    port=int(port)
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    
    newRequestThread = threading.Thread(target=newRequest, name='newChainThread')
    newDataThread = threading.Thread(target=newData, name='newChainThread')
    newChainThread = threading.Thread(target=newchains, name='newChainThread')
    while True:
        c, addr = s.accept()
        conectionType = c.recv(1024)
        if conectionType == b'request':
            newRequestThread.start()
    
    
        elif conectionType == b'data':
            newDataThread.start()
                
    
        elif conectionType == b'newChain':
            if newDataThread.is_alive():
                newDataThread.abort()
            newChainThread.start()
        c.close()

def newRequest():
    clients.append(addr[0])
    c.send(chain1.__get_chain_bytes__())
    c.close()
    

def newData():
    data = c.recv(1024)
    data = data.decode("utf-8")
    c.close()
    newsocket = socket.socket()
    for ip in clients:  
        newsocket.connect((ip, str(port)))
        newsocket.send(b'data')
        newsocket.send(data)
    chain1.addBlock(data)
    newsocket = socket.socket()
    for ip in clients:  
        newsocket.connect((ip, str(port)))
        newsocket.send(b'newChain')
        newsocket.send(chain1.__get_chain_bytes__())

def newchains():
    newChainBytes = c.recv(1024)
    c.close()
    chain2 = Chain(byte=newChainBytes)
    if chain1.same_chain(chain2):
        chain1 = chain2.best_chain(chain1)
    return chain1
    newsocket = socket.socket()
    for ip in clients:  
        newsocket.connect((ip, port))
        newsocket.send(b'newChain')
        newsocket.send(chain1.__get_chain_bytes__())

global chain1
global  clients
host = socket.gethostname()
port = 12345
clients=[]
start = input('are You the first server 1,0?:')

if start == '1':
    chain1 = ooBlock.Chain()
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

networkingThread = threading.Thread(target=chainNetwork, args=(port, host), name='networkingThread')
networkingThread.start()
flag =0

while flag == 0 :
    print('1: add data \n 2:see blockChain \n 3: quit')
    option = input('pick an option:')
    if int(option) == 3:
        flag=1
    elif int(option) == 2:
        print(chain1.__get_chain_bytes__().decode("utf-8"))
    elif int(option) == 1:
        data=input("what data do you want to transmit: ")
        for ip in clients:
            newsocket.connect((ip, port))
            newsocket.send(b'data')
            newsocket.send(data)
    else:
        print('incorrect input')