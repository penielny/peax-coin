from hashlib import sha256
from datetime import datetime ,timedelta
import uuid
from database import database
from bson.objectid import ObjectId
import pickle

class Block():
	"""docstring for Coin"""
	pv=None
	def __init__(self, amount=0.0 , from_ =None, to_ =None , db=database ,comment="",pv_=None):
		self.amount = amount
		self.from_ = from_
		self.to_ = to_
		self.id_ = str(uuid.uuid4())
		self.prev_hash = None
		self.db = db
		self.comment=comment
		self.confirmation = 0
		self.timestamp = datetime.utcnow()
		self.nonce = 0
		global pv
		pv=pv_
		self.transaction = {"amount":self.amount , "from":self.from_, "to":self.to_ , "timestap":self.timestamp}
		algo = sha256()
		algo.update(str(self.transaction).encode('utf-8'))
		self.intergriy_hash = algo.hexdigest()
		self.current_hash = algo.hexdigest()

	def incr_confirmation(self):
		self.confirmation +=1

	def makeHash(self):
		algo = sha256()
		self.nonce += 1
		algo.update(str({"intergriy_hash": self.intergriy_hash, "nonce": self.nonce,"confirmation": self.confirmation,"current_hash": self.current_hash,"timestap":self.timestamp}).encode('utf-8'))
		self.current_hash = algo.hexdigest()
		return algo.hexdigest()

	def drop(self):
		sika = self.db.users.find_one({"private_key":self.private_key})['account']['tokens'] + self.amount
		global pv
		self.db.users.update_one({"private_key":self.pv},{"$set":{"account":{"tokens":sika}}})
		# remove from database
		chech= {
		"id": self.id_,
		"date":self.timestamp,
		"token" : self.amount,
		"recv_wallet": self.to_,
		"comment" : self.comment,
		"sender_wallet":self.from_
		}
		if self.confirmation >=3:
			self.db.transaction.delete_one(chech)
		else:
			self.db.unconfirmed.delete_one(chech)


	def makePersist(self):
		transaction = {
		"id": self.id_,
		"date":self.timestamp,
		"token" : self.amount,
		"recv_wallet": self.to_,
		"confirmation" : self.confirmation,
		"comment" : self.comment,
		"sender_wallet":self.from_,
		}
		chech= {
		"id": self.id_,
		"date":self.timestamp,
		"token" : self.amount,
		"recv_wallet": self.to_,
		"comment" : self.comment,
		"sender_wallet":self.from_
		}
		if self.confirmation >=3:
			if self.db.unconfirmed.find_one(chech):
				self.db.unconfirmed.delete_one(chech)
			if not self.db.transaction.find_one(chech):
				self.db.transaction.insert_one(transaction)
				am = self.db.users.find_one({"private_key":pv})["account"]['tokens']
				self.db.users.update_one({"private_key":pv},{"$set":{"account":{"tokens":round(am+self.amount,7)} }})
		else:
			if not self.db.unconfirmed.find_one(chech):
				self.db.unconfirmed.insert_one(transaction)
		pickle.dump(f"{self}",open(f"blocks/{self.id_}.ds","wb"))


	def getData(self):
		return {"nonce":self.nonce,"intergriy_hash":self.intergriy_hash ,"current_hash":self.current_hash ,"transaction":self.transaction,"prevhash": self.prev_hash,}

	def __str__(self):
		# return str({"confirms":self.confirmation ,"prevhash": self.prev_hash,"intergriy_hash":self.intergriy_hash ,"current_hash":self.current_hash,"timestap":str(self.timestamp)})
		return str(f"<Block {self.id_}>")