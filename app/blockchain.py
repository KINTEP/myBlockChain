import time
import datetime
from helper import calculate_sha256
from transactions import Transaction_In, Transaction_Out, Transaction

class Data:
	"""This class represents a schema of the data we expect to be passed into the block"""
	def __init__(self, title, content):
		self.title = title
		self.content = content
		#self.timestamp = datetime.datetime.utcnow()
		#self.time = time.time()

	def __repr__(self):
		return str(self.__dict__)
	
	def id(self):
		"""This function return the hash of the data passed into the class"""
		data = self.__dict__
		return calculate_sha256(data)

	def data_hash(self):
		"""This function returns the hash of the content and title. 
		These are the most essential features of the data"""
		data = {
			"title": self.title,
			"content": self.content
		}
		return calculate_sha256(data)

	def sign():
		"""To prove ownership of this document, you have to sign it with your private key"""
		pass

	def verify():
		"""We should have a way to verify the data the user is pasing."""
		#We may have to implement this function in the Block class
		pass

class Mempool:
	"""This class contains all transactions before they are passed into the block.
	However, the class will only return the unconfirmed data."""
	def __init__(self, data):
		self.data = data
		self.unconfirmed_data = []

	def add(self):
		self.unconfirmed_data.append(self.data)
		return True
		

	

class Block:
	"""The class contains a schema of the block that will be passed into the blockchain"""
	#diff = 1

	def __init__(self, transactions, index = 0, prev_hash = "0", nonce = 0):
		self.index = index
		self.transactions = transactions
		self.id = self.compute_hash()
		self.prev_hash = prev_hash
		self.nonce = nonce
		#self.timestamp = datetime.datetime.utcnow()
	
	#def __repr__(self):
		#return str(self.__dict__)

	def compute_hash(self):
		data = self.__dict__
		return calculate_sha256(data)

	def proof_of_work(self):
		"""This function computes the proof of work which will be used to mine the block"""
		diff = 1
		self.nonce = 0
		Hash = self.compute_hash()
		while Hash[:diff] != "0"*diff:
			Hash = self.compute_hash()
			self.nonce += 1
		self.id = Hash
		return True

	def add_data(data):
		pass

class Blockchain:
	def __init__(self):
		self.chain = []
		self.genesis_block()
		self.diff = 1

	def genesis_block(self):
		block = Block(index = 0, transactions = [], prev_hash = "0")
		block.proof_of_work()
		self.chain.append(block)
		
	@property
	def last_block(self):
		return self.chain[-1]

	def add_block(self, block):
		proof = block.proof_of_work()
		if not proof:
			return "Invalid block"
		if proof:
			block.index = self.last_block.index + 1
			block.prev_hash = self.last_block.id
			self.chain.append(block)
		return True

	def is_chain_valid(self):
		for i in range(len(self.chain)-1):
			first_block = self.chain[i]
			second_block = self.chain[i+1]
			if first_block.id != second_block.prev_hash:
				return False
			if not first_block.proof_of_work() and not second_block.proof_of_work():
				return False
		return True

#d1 = Data(title = "First One", content = "This is our first post we are making.")
#d2 = Data(title = "First Two", content = "This is our second post we are making.")
#d3 = Data(title = "First Three", content = "This is our third post we are making.")

#In1 = Transaction_In(prev_tx = "0", prev_idx = 0)


#Out = Transaction_Out(amount = 10, data = [d1,d2], pubkey = "mnH7gGb9aeSEwrv8V4vK5VkNnn4UtN6uRs")
#Tx1 = Transaction(input_ = In1, output = Out)


#print(Tx1)
#s1 = sign(Tx1.id(), secret = 123344455)
#d1 = Data(title = "First One", content = "This is our first post we are making.")
#e8312fa1099c614fa5c14e4d44375a13bbb791c204d48f89489b9bfecfc9dd0d
#98de7871ec807d282f2545fb8aafd8a7e2112a5ef14caeb521298b0ede0db0ab
#print(d1.id())
#print(d1.data_hash())

#Mem = Mempool(d1)
#print(Mem.add())
"""
#a79abab8f0a070c63e409b93d284450fb28c6c205e283624ddbea06105f1a3a1
d2 = Data(title = "First One", content = "This is our first post we are making.")
print(d2.data_hash())
print(d2.id())
blockchain = Blockchain()
B1 = Block(data = [d1])
B2 = Block(index = 2, data = [d1], prev_hash = "1")
print(B1.id)
#print(B1.data)


print(B1.id)
print(B1.nonce)

print(20*"==")
print(B1.proof_of_work())
#blockchain = Blockchain()
print(blockchain.add_block(B1))
#blockchain.chain.append(B2)


#print(blockchain.chain)
print(len(blockchain.chain))
#print(blockchain.chain)
#print(blockchain.last_block)
print(blockchain.is_chain_valid())

Data = Data(title = "title", content = "content")
Mem = Mempool(Data.__dict__)
print(Mem.add())
unconfirmed_data = Mem.unconfirmed_data
block = Block(data = unconfirmed_data)
print(type(block))

import json

print(json.dumps(block.__dict__))

"""

#blockchain = Blockchain()
#print(blockchain.add_block(block))
#print(blockchain.chain)
#print(blockchain.is_chain_valid())

