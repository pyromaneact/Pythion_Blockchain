from datetime import datetime
import hashlib
import random

class Chain:
    
    chains=0
    
    def __init__(self, chain, fittness='''self.__fitness__('0')''', hashing = ('''self.__hashing__('''), notTemp=1):
        self.chain=chain
        self.length=len(chain)
        self.fitnessFunction=fittness
        self.hashingFunction=hashing
        Chain.chains += notTemp

    def addBlock(self, data):
        timestamp = self.__time__()
        fitness={'self':self}
        exec('check =' + self.fitnessFunction, globals(), fitness)
        if self.length == 0:
            lastHash = '0'
        else:
            hashed={}
            exec('Hash = ' + self.hashingFunction + 'self.chain[-1])', globals(), hashed)
            lastHash=hashed['Hash']
        self.chain.append(block(self.chain, data, timestamp, lastHash, fitness['check'], self.hashingFunction))

    def __time__(self):
        utc_time = datetime.utcnow()
        utc_timestamp = utc_time.timestamp()
        return utc_timestamp


    def __hashing__(self, unencrypted_string):
        unencrypted_bytes = unencrypted_string.__encode__()
        encrypted_bytes = hashlib.sha256(unencrypted_bytes)
        encrypted_block = encrypted_bytes.hexdigest()
        return encrypted_block

    def __check_chain__(self):
        valid = self.chain[-1].__checkBlock__()
        if valid == 1:
            if len(self.chain) !=1:
                tempchain=Chain(self.chain[0:-1], self.fitnessFunction,self.hashingFunction,0).__check_chain__()
                return tempchain
            else:
                return 1
        else:
            return 0
    
    def __get_partual_chain__(self, start, end):
        return self.chain[start,end]
    
    def __get_chain__(self):
        return self.chain
    
    def __fitness__(self, value):
        fit=self.__get_chain__()
        if len(fit)<1:
            return '0'
        else:
            return fit[-1][0]


   

class block(Chain):
    def __init__(self, thechain, data,time,previousHash,fitness, hashing):
        self.data = data
        self.thechain = thechain
        self.time = time
        self.previousHash = previousHash
        self.fitness = fitness
        self.hashing = hashing
        self.nonce = 0
        self.__generateNonce__()

    def __generateNonce__(self):
        while (self.__checkBlock__() != 1):
            new_nonce = random.randint(0, 2147483647)
            self.nonce = new_nonce

    def __checkBlock__(self):
        fitness={'self':self}
        exec('hashed_block =' + self.hashing + 'self)', globals(), fitness)
        if fitness['hashed_block'][0:len(self.fitness)] != self.fitness:
            return 0
        else:
            return 1
    
    def __encode__(self):
        data = ''
        data += str(self.data)
        data += str(self.time)
        data += str(self.previousHash)
        data += str(self.fitness)
        data += str(self.nonce)
        return bytes(data, 'utf-8')




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
