import json
import time
import hashlib
from uuid import uuid4
from distutils.log import debug
from flask import Flask, jsonify


class MyBlockchain(object):
    
    def __init__(self):
        
        # List of Blocks
        self.chain = [] 
        
        # List of Transactions --> memePool || memory pool
        self.current_trx = [] 
        
        self.new_block(nonce=100, previous_hash=1)
        
    
    def new_block(self, nonce, previous_hash=None):
        
        '''create a new Block'''
        
        block = {
            'BlockNumber': len(self.chain),
            'timestamp': time.time(),
            'trxDetails': self.current_trx,
            'proofOfWork': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        # Clear memePoll
        self.current_trx = []
        
        # Add the new block to our Blocks List
        self.chain.append(block)
        return block
    
    def new_trx(self, _from, _to, _amount):
        
        '''add new trx to memory pool (memepool)'''
        
        self.current_trx.append({'sender': _from, 'reciver': _to, 'amount': _amount})
        return last_block[index] + 1
        
    
    @staticmethod
    def hash(block):
        
        '''hash a block'''
        
        # Convert the block to a json string then encode
        block_str = json.dumps(block, sort_keys=True).encode()
        
        # hash bolck_str using sha256 algorithm
        hash_block_str = hashlib.sha256(block_str).hexdigest()
        return hash_block_str
    
    
    @property
    def last_block(self):
        
        '''return last block'''
        pass
    
    
    def create_nonce(self, last_nonce):
        
        '''implement proof-of-work mechanism and create a valid nonce'''
        # first, initial (nonce = 0) and while the nonce is not valid
        # we're going to continue (nonce += 1) to find a valid nonce
        
        nonce = 0
        while valid_nonce(last_nonce, nonce) == False:
            nonce += 1
        
        return nonce
    
    
    @staticmethod
    def valid_nonce(last_nonce, nonce):
        
        '''validate nonce for proof-of-work'''
        
        this_nonce = f'{last_nonce}{nonce}'.encode()
        hash_this_nonce = hashlib.sha256(this_nonce).hexdigest()
        
        return hash_this_nonce[:4] == '0000'
        
        
app = Flask(__name__)
node_ID = str(uuid4())    
blockchain = MyBlockchain()


@app.route('/mine')
def mine():
    
    '''we use this function to create/mine new block and add it to chain list'''
    
    return 'I will mine'


@app.route('/trx/new')
def new_transaction():
    
    '''we use this function to add a new transaction to memepool'''
    
    return 'I will add new trx'


@app.route('/chain')
def get_chain():
    
    '''this function return us chain list with json format'''
    
    full_chain = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    
    return jsonify(full_chain), 201


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6000)