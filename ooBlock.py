from datetime import datetime
import hashlib
import random

class block:
    def __init__(self, thechain, data,time,previousHash,fitness):
        self.data = data
        self.time = time
        self.previousHash = previousHash
        self.fitness = fitness
        self.nonce = 0
        self.__generateNonce__(thechain)

    def __generateNonce__( self, thechain):
        fitness={'self':self}
        exec('check =' + self.fitness, globals(), fitness)
        hashed_block = thechain.__hashing__(self)
        while (hashed_block[0:len(fitness['check'])] != fitness['check']):
            new_nonce = random.randint(0, 2147483647)
            self.nonce = new_nonce
            hashed_block = thechain.__hashing__(self)
    
    def __encode__(self):
        data = ''
        data += str(self.data)
        data += str(self.time)
        data += str(self.previousHash)
        data += str(self.fitness)
        data += str(self.nonce)
        return bytes(data, 'utf-8')

class Chain:
    
    chains=0
    
    def __init__(self, chain, fittness='''Chain.__fitness__(self, '0')'''):
        self.chain=chain
        self.length=len(chain)
        self.fitnessFunction=fittness
        Chain.chains += 1

    def addBlock(self, data):
        timestamp = self.__time__()
        if self.length == 0:
            lastHash = '0'
        else:
            lastHash = self.__hashing__(self.chain[-1])
        self.chain.append(block(self, data, timestamp, lastHash, self.fitnessFunction))

    def __time__(self):
        utc_time = datetime.utcnow()
        utc_timestamp = utc_time.timestamp()
        return utc_timestamp

    def __hashing__(self, unencrypted_string):
        unencrypted_bytes = unencrypted_string.__encode__()
        encrypted_bytes = hashlib.sha256(unencrypted_bytes)
        encrypted_block = encrypted_bytes.hexdigest()
        return encrypted_block
    
    def __fitness__(self, value):
        print(self.chain)
        return str(value)

def main():
    '''test function to check script Creates a blockchain'''
    #start_chain('data1')
    #begin_chain('thats a chain')
    #make_block('dom')
    chain1 = Chain([])
    chain1.addBlock('abc')


# Standard boilerplate code to call the main() function to begin
# the program if run as a script.
if __name__ == '__main__':
    main()
