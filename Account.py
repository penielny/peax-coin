import uuid
from database import database
from bson.objectid import ObjectId
from Block import Block


class Account():

	def __init__(self,db=database ,private_key=None,email=None,password=None):
		self.private_key=private_key
		self.db = db
		self.email=email
		self.password=password
		self.doc = self.get_user_doc()

	def is_valid(self):
		if self.doc:
			return True
		return False

	def get_info(self):
		self.doc['_id'] = str(self.doc['_id'])
		return self.doc

	def get_user_doc(self):
			return self.db.users.find_one({"$or":[{"email":self.email,"password":self.password},{"private_key":self.private_key,"password":self.password}]})

	def send_pxn(self,ammount=None , recv_wallet=None , comment="" ,blockchain=[]):
		if ammount and recv_wallet:
			if (ammount)+((ammount)*0.01) <= (self.doc['account']['tokens']):
				if(recv_wallet in self.doc['keys']):
					return "can't send PXN to yourself"
				sika = (ammount)+((ammount)*0.01)
				# desit charge to minners
				total=(self.doc['account']['tokens'])-sika
				print(total)
				block = Block(amount=ammount , from_=self.doc['keys'][-1],to_=recv_wallet,comment=comment,pv_=self.doc['private_key'])
				self.db.users.update_one({"private_key":self.get_user_doc()['private_key']},{"$set":{"account":{"tokens":round(total,7)}}})
				# put the block into the pendings chain
				blockchain.pending_blocks.append(block)
				# then persist it to the database
				block.makePersist()
				return "PXN sent succefully"
		return "You do not have enough PXN"
	def get_balance(self):
		return self.doc["account"]["tokens"]

	def transactions(self):
		transactions = []
		for key in self.doc['keys']:
			docs = self.db.transactions.find({"$or" :[{"recv_wallet":key},{"sender_wallet":key}]})
			if docs:
				for doc in docs:
					transactions.append(doc)
		return transactions
	def pendings(self):
		pendings = []
		for key in self.doc['keys']:
			docs = self.db.unconfirmed.find({"$or" :[{"recv_wallet":key},{"sender_wallet":key}]})
			if docs:
				for doc in docs:
					pendings.append(doc)
		return pendings

	def transaction(self,id_):
		docs = self.db.transactions.find({"id":id_}).limit(5)
		return docs

	def makeRecv_key(self):
		rcv_key = uuid.uuid4()
		rcv_key = str(rcv_key).split('-')
		rc =""
		for el in rcv_key:
			rc=rc+el
		rcv_key =rc
		prev_key = self.doc['keys']
		new_key=[]
		if prev_key:
			new_key = [key for key in prev_key]
		new_key.append(str(rcv_key))
		self.db.users.update_one({"private_key":self.doc['private_key']},{"$set" : {"keys":new_key}})
		self.doc = self.get_user_doc()
		return rcv_key

	def validate(self):
		return self.db.users.find_one({"$or":[{"email":self.email,},{"private_key":self.private_key,}]})

	def create(self):
		user = {
			"email":self.email,
			"password":self.password,
			"private_key":''.join(map(str, str(uuid.uuid4()).split('-'))),
			"account":{
			"tokens":0.00000000
			},
			"keys":[
				''.join(map(str, str(uuid.uuid4()).split('-')))
			],
		}
		self.db.users.insert_one(user)
		self.doc = self.get_user_doc()

	def __str__(self):
		try:
			return f"<Account : '{(self.doc['private_key'])}'>"
		except Exception as e:
			return f"<Account : '{None}'>"

# acc =Account(email="pe@mial.com",password="123456")
# print(f"{acc.get_balance()}PXN")
# print(acc.makeRecv_key())
# print(acc)