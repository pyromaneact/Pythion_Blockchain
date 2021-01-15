'''
Script:    blockchain.py
Desc:    script to act as a poc python powered blockchain
last edited:    11/01/2021
Author:    Eliot Bolster Cyber_Coo
'''

from datetime import datetime
import hashlib
import json
import random


def start_chain(data):
    '''creates first block for blockfrom a pice of data'''
    temp_block = add_metadata(data, 0)
    full_block = generate_nonce(temp_block, 1)
    save_chain(full_block, 'the_chain.json')


def begin_chain(data):
    '''creates second block for blockfrom a pice of data'''
    chain = extract_chain('the_chain.json')
    prevous_hash = hashing(chain)
    temp_block = add_metadata(data, prevous_hash)
    full_block = generate_nonce(temp_block, 1)
    full_chain = [chain, full_block]
    save_chain(full_chain, 'the_chain.json')


def make_block(data):
    '''generates blockfrom a pice of data'''
    chain = extract_chain('the_chain.json')
    prevous_hash = hashing(chain[-1])
    temp_block = add_metadata(data, prevous_hash)
    full_block = generate_nonce(temp_block, 1)
    chain.append(full_block)
    save_chain(chain, 'the_chain.json')
    return full_block


def add_metadata(core_data, last_hash):
    '''adds necessery metadata to create block'''
    # option for extra metadata
    utc_time = datetime.utcnow()
    utc_timestamp = utc_time.timestamp()
    partual_block = {'nonce':0, 'data':core_data, 'time':utc_timestamp, 'prevous_hash':last_hash}
    return partual_block



def generate_nonce(partual_block, strength):
    '''bruteforces nonces to create a prof of work'''
    hashed_block = hashing(partual_block)
    while int(hashed_block[0:strength], 16) != 0:
        new_nonce = random.randint(0, 2147483647)
        partual_block['nonce'] = new_nonce
        hashed_block = hashing(partual_block)
    return partual_block


def hashing(unencrypted_block):
    '''preforms hash to ensure validity '''
    # try not a dict imported
    unencrypted_string = json.dumps(unencrypted_block)
    unencrypted_bytes = unencrypted_string.encode()
    encrypted_bytes = hashlib.sha256(unencrypted_bytes)
    encrypted_block = encrypted_bytes.hexdigest()
    return encrypted_block


def check_chain(chain):
    '''checks if new chain is valid'''
    last_hash = ''
    for block in chain:
        if last_hash != '':
            this_hash = block['prevous_hash']
            if this_hash != last_hash:
                return 0
        last_hash = hashing(block)
    return 1


def correct_chain(*chains):
    '''checks which chain cryptographicly is the longest'''
    chains = list(chains)
    long_chain = chains[0]
    for chain in chains:
        if len(long_chain) < len(chain):
            long_chain = chain
    correct = check_chain(long_chain)
    if correct == 0:
        chains.remove(long_chain)
        if len(chains) == 0:
            return 0
        correct_chain(*chains)
    return long_chain


def save_chain(chain, file):
    '''saves blockchain with new data'''
    try:
        with open(file, 'w') as json_file:
            json.dump(chain, json_file, indent=4)
    except TypeError:
        print('\n\ndata is not json compatable failed to make file')
    return json.dumps(chain)


def extract_chain(file):
    '''extracts blockchain from file'''
    # try fail to open
    with open(file, 'r') as json_file:
        current_chain = json.load(json_file)
    return current_chain

def main():
    '''test function to check script Creates a blockchain'''
    #start_chain('data1')
    #begin_chain('thats a chain')
    #make_block('dom')
    chain1 = extract_chain('the_chain.json')
    chain2 = extract_chain('the_chain2.json')
    print(correct_chain(chain1, chain2))


# Standard boilerplate code to call the main() function to begin
# the program if run as a script.
if __name__ == '__main__':
    main()
