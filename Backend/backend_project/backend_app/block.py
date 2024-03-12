from hashlib import sha256
import datetime
import json
from .transaction import *
class Block : 
    def __init__(self, transaction ,  prevHash  ) :
        self.prevHash  = prevHash
        self.transaction = transaction 
        self.timestamp = datetime.datetime.now()
        self.nonce = 0 
        self.hash = self.calculateHash()
    
    def calculateHash(self) :
        data_string = json.dumps(self.transaction, default=lambda o: o.to_dict(), sort_keys=True)
        hash_object = data_string + str(self.prevHash) + str(self.timestamp) + str(self.nonce)
        block_hash = sha256(hash_object.encode('utf-8'))
        return block_hash.hexdigest()

    def proof_of_work(self ,difficulty ) :
        repeated_string = "0" * difficulty
        while not self.hash.startswith(repeated_string) :
            self.nonce += 1
            self.hash = self.calculateHash() 
    
    def valid_transactions(self) : 
        for trans in self.transaction : 
            if not trans.validate_signature() : 
                return False
        
        return True


    def print_contents(self):
        print (f"Block Hash: {self.hash}\nData: {self.transaction}\n PrevHash: {self.prevHash}\nMine : {self.nonce}")