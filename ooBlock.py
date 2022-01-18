from datetime import datetime
import hashlib
import random

class Chain:
    
    chains=0
    
    def __init__(self, chain = [], fittness='''self.__fitness_function__()''', fittnessValue = '''self.__fitness_value__()''', hashing = ('''self.__hashing__('''), byte=b'' ,notTemp=1):
        Chain.chains += notTemp
        self.chain=chain
        if  byte == b'':
            self.fitnessFunction=fittness
            self.hashingFunction=hashing
            self.fittnessValue=fittnessValue
        else:
            self.__get_chain_from_bytes__(byte)

    def addBlock(self, data):
        timestamp = self.__time__()
        fitness={'self':self}
        exec('check =' + self.fitnessFunction, globals(), fitness)
        if len(self.chain) == 0:
            lastHash = '0'
        else:
            hashed={'self':self}
            exec('Hash = ' + self.hashingFunction + 'self.chain[-1])', globals(), hashed)
            lastHash=hashed['Hash']
        self.chain.append(block(data, timestamp, lastHash, fitness['check'], self.hashingFunction))

    def __time__(self):
        utc_time = datetime.utcnow()
        utc_timestamp = utc_time.timestamp()
        return utc_timestamp


    def __hashing__(self, unencrypted_string):
        unencrypted_bytes = unencrypted_string.__encode__()
        encrypted_bytes = hashlib.sha256(unencrypted_bytes)
        encrypted_block = encrypted_bytes.hexdigest()
        #print(encrypted_block)
        return encrypted_block

    def __check_chain__(self):
        valid = self.chain[-1].__checkBlock__()
        if valid == 1:
            if len(self.chain) !=1:
                tempchain=Chain(chain = self.chain[0:-1], fittness = self.fitnessFunction, fittnessValue = self.fittnessValue,  hashing = self.hashingFunction,notTemp = 0).__check_chain__()
                return tempchain
            else:
                return 1
        else:
            return 0
    
    def __get_partual_chain__(self, start, end):
        return self.chain[start,end]
    
    def __get_chain_bytes__(self):
        byte=b''
        byte += bytes(self.fitnessFunction + '"], ["', 'utf-8')
        byte += bytes(self.fittnessValue + '"], ["', 'utf-8')
        byte += bytes(self.hashingFunction + '"], ["', 'utf-8')
        for ablock in self.chain:
            byte += ablock.__encode__()
        return byte


    def __get_chain_from_bytes__(self, byte):
        string = byte.decode("utf-8")
        chainparts = string.split('"], ["')
        self.fitnessFunction = chainparts[0]
        self.fittnessValue = chainparts[1]
        self.hashingFunction = chainparts[2]
        blocks = chainparts[3][0:-1].split('";; "')
        for each in blocks:
            items = each.split('", "')
            fitness={'self':self}
            exec('check =' + self.fitnessFunction, globals(), fitness)
            self.chain.append(block( items[0], items[1], items[2], fitness['check'], self.hashingFunction))
            
        
    
    def __fitness_function__(self):
        fit=self.chain
        if len(fit)<1:
            return '0'
        else:
            return fit[-1].previousHash[0]

    def __fitness_value__(self):
        return len(self.chain)


    def same_chain(self, chain2):
        if self.fitnessFunction == chain2.fitnessFunction and self.fittnessValue == chain2.fittnessValue and self.hashingFunction == chain2.hashingFunction:
            return 1
        else:
            return 0


    def best_chain(self, chain2):
        chain1valid = self.__check_chain__()
        chain2valid = chain2.__check_chain__()
        if chain2valid and chain1valid:
            chain1value = self.__fitness_value__()
            chain2value = chain2.__fitness_value__()
            if chain1value < chain2value:
                return chain2
            else:
                 return self
        if chain1valid == 1:
            return self
        elif chain2valid == 1:
            return chain2
        else:
            return 0




class block(Chain):
    def __init__(self, data,time,previousHash,fitness, hashing, nounce=-1):
        self.data = data
        self.time = time
        self.previousHash = previousHash
        self.fitness = fitness
        self.hashing = hashing
        self.nonce = nounce
        if nounce == -1:
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
        data += '", "' + str(self.time)
        data += '", "' + str(self.previousHash)
        data += '", "' + str(self.nonce) + '";; "'
        #print(bytes(data, 'utf-8'))
        return bytes(data, 'utf-8')




def main():
    '''test function to check script Creates a blockchain'''
    #start_chain('data1')
    #begin_chain('thats a chain')
    #make_block('dom')
    chain1 = Chain()
    chain1.addBlock('abc')
    chain1.addBlock('def')
    chain1.addBlock('keep trying')
    sending=chain1.__get_chain_bytes__()
    #print(sending)
    chain2 = Chain(byte=sending)
    chain2.addBlock('ghi')
    if chain1.same_chain(chain2):
        chain1 = chain2.best_chain(chain1)
    sending=chain1.__get_chain_bytes__()
    print(sending)


# Standard boilerplate code to call the main() function to begin
# the program if run as a script.
if __name__ == '__main__':
    main()
