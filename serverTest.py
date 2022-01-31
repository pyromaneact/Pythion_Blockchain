import socket
import ooBlock
import threading

def chainNetwork(port, host):
    port=int(port)
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)



    while True:
        c, addr = s.accept()
        
        
        newRequestThread = threading.Thread(target=newRequest, args=(addr[0], c), name='newRequestThread')
        conectionType = c.recv(1024)
        if conectionType == b'request':
            newRequestThread.start()
    
    
        elif conectionType == b'data':
            data = c.recv(1024)
            data = data.decode("utf-8")
            c.close()
            newDataThread = threading.Thread(target=newData, args=(data,), name='newDataThread')
            newDataThread.start()
                
    
        elif conectionType == b'newChain':
            if newDataThread.is_alive():
                newDataThread.abort()
            newChainBytes = c.recv(1024)
            c.close()
            newChainThread = threading.Thread(target=newchains, args=(newChainBytes,), name='newChainThread')
            newChainThread.start()
        c.close()

def newRequest(ip, c):
    clients.append(ip)
    c.send(chain1.__get_chain_bytes__())
    c.close()
    

def newData(data):
    newsocket = socket.socket()
    for ip in clients:
        newsocket.connect((ip, port))
        newsocket.send(b'data')
        newsocket.send(data)
    chain1.addBlock(data)
    newsocket = socket.socket()
    for ip in clients:
        #print(ip)
        newsocket.connect((ip, port))
        newsocket.send(b'newChain')
        newsocket.send(chain1.__get_chain_bytes__())

def newchains(newChainBytes):
    chain2 = Chain(byte=newChainBytes)
    if chain1.same_chain(chain2):
        chain1 = chain2.best_chain(chain1)
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
        newsocket = socket.socket()
        for ip in clients:
            newsocket.connect((ip, port))
            newsocket.send(b'data')
            newsocket.send(data)
    else:
        print('incorrect input')