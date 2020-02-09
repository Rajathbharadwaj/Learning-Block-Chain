# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 15:18:28 2020

@author: Rajath
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify


#part 1 - build BC

class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')
        
    def create_block(self, proof, prev_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' :  str(datetime.datetime.now()),
                 'proof' : proof,
                 'prev_hash' : prev_hash}
        self.chain.append(block)
        return block
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, prev_proof):
        new_proof = 1
        check_proof = False
        while not(check_proof):
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            
            if hash_operation[:4]=='0000':
                check_proof = True
            else:
                new_proof = new_proof+1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def isChainValid(self, chain):
        prev_block = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]!= '0000':
                return False
            prev_block = block
            blockIndex += 1
        return True
    
    
app = Flask(__name__)

bc= BlockChain()

@app.route('/mine_block', methods = ['GET'])
def mineBlock():
    prev_block = bc.getPrevBlock()
    prev_proof = prev_block['proof']
    proof = bc.proofOfWork(prev_proof)
    prev_hash = bc.hash(prev_block)
    block = bc.create_block(proof,prev_hash)
    response = {'message' : 'Congrats', 
                'index' : block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'prev_hash' : block['prev_hash']}
    return jsonify(response), 200
    
@app.route('/get_chain', methods = ['GET'])
def getChain():
    response = {'chain':bc.chain,
                'length' : len(bc.chain)}
    return jsonify(response), 200
      
app.run(host='0.0.0.0', port = 5003)