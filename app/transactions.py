import requests
import datetime
from helper import small_file_hash, hash256, sha256, calculate_sha256
from keys import PrivateKey, Signature

NODE = "http://127.0.0.1:8000"

def get_tx_from_chain(tx_id):
	"""Returns transaction data from blockchain given transaction id"""
	chain = requests.get(f"{NODE}/chain").json()["chain"]
	for index in chain:
		if int(index["index"]) >= 1 and index["transactions"]["tx_id"] == str(tx_id):
			return True, index
	return False, None

class Transaction_In:
	def __init__(self, prev_tx, prev_idx):
		self.prev_tx = prev_tx
		self.prev_idx = prev_idx

	def __repr__(self):
		data = {
				"prev_idx": self.prev_idx,
				"prev_tx": self.prev_tx,
				}
		return f"{self.__dict__}"

	def data(self):
		bool, data = get_tx_from_chain(self.prev_idx)
		if not bool:
			return "No data found, please try again!"
		return data

	def value(self):
		"""Returns the amount involved in the transaction"""
		data = self.data()
		return data["transactions"]["output"]["amount"]

	def pubkey(self):
		"""Returns the public key of the recipient of the transaction"""
		data = self.data()
		return data["transactions"]["output"]["pubkey"]

	def verify(self):
		"""Returns True is transaction exist on the blockchain"""
		bool, data = get_tx_from_chain(self.prev_idx)
		return bool

class Transaction_Out:
	def __init__(self, data, amount, pubkey):
		self.data = data
		self.amount = amount
		self.pubkey = pubkey

	def __repr__(self):
		return f"{self.pubkey}: {self.data}"

	def data_id(self):
		return self.data.id()

class Transaction:
	"""This class represents a schema of the data we expect to be passed into the block"""
	def __init__(self, input_, output):
		self.input_ = input_
		self.output = output
		#self.signature = self.sign(secret = "")
		#self.timestamp = datetime.datetime.utcnow()

	def __repr__(self):
		#data = self.__dict__
		return f"{self.__dict__}"

	def id(self):
		data = {
				"input": self.input_,
				"output": self.output,
				}
		return calculate_sha256(data)

	def hash(self):
		pass
		#return hash256(self.input_.data)
		#The private key must not be part of the hash

	def verify_input(z, sig, secret, tx_id):
		'''Returns whether the input has a valid signature'''
		bool, data = get_tx_from_chain(tx_id)
		sigi = data["transactions"]["signature"]
		r,s = sig["r"], sig["s"]
		sig = Signature(r,s)
		private_k = PrivateKey(secret = secret)
		point = (private_k.point.x, private_k.point.y)
		px = point[0]
		py = point[1]
		ver = S256Point(px, py)
		return ver.verify(z, sig)

	def verify(self):
		pass

	def is_initial_tx(self):
		"""Returns whether this is the first transaction of the user"""
		#If sender and receiver address are same, then it can be assumed to be a first time item
		if self.input_.output.pubkey != self.output.pubkey:
			return False
		return True

	def sign(self, secret, z):
		private = PrivateKey(secret = secret)
		sig = private.sign(z)
		return sig