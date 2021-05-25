from time import time
import json
from random import randint
import hashlib


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash='0'*64, proof=100)

    # Create a new block listing key/value pairs of block 
    # information in a JSON object. Reset the list of pending
    # transactions & append the newest block to the chain.

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    #Search the blockchain for the most recent block.

    @property
    def last_block(self):
 
        return self.chain[-1]

    # Add a transaction with relevant info to the 'blockpool' - list of pending tx's. 

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    # receive one block-> to a string->Unicode 
    #  Hash with SHA256 encryption->
    # translate the Unicode into a hexidecimal string.

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


totalMinerNodes = 10

# creating the miner nodes
print ('\n----------')
minerNodes = [('M'+str(i)) for i in range(totalMinerNodes)]
print ('Miner Nodes: ', minerNodes)
print ('----------\n')

# reading the transactions pool
inputFile = open('transaction.txt', 'r')
trans = inputFile.readlines()
inputFile.close()

currTrans = 0
transPerNode = int(len(trans)/len(minerNodes))


#create the blockchain
blockchain = Blockchain()

# for each miner node creating the blocks and assigning the transactions
for node in minerNodes:
  for t in trans[currTrans:currTrans+transPerNode]:
    values = t.split()
    blockchain.new_transaction(values[0], values[1], values[2] + ' BTC')

  blockchain.new_block(node + "_" + str(randint(1, 50)))

    
# printing the final block chain schedule
print("Root block: ")

for block in blockchain.chain:
  print (block)
  print ('----------\n')
