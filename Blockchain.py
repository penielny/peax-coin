from hashlib import sha256
from Block import Block
from database import database
import pickle

class Chain():
	"""docstring for Chain"""
	def __init__(self, blocks=[] , difficulty=1 , pending_blocks=[],db=database):
		self.blocks = blocks
		self.difficulty = difficulty
		self.pending_blocks = pending_blocks
		self.db=db

	def sync(self):
		all_trans = self.db.transaction.find({})

		for tran in all_trans:
			self.blocks.append(pickle.load(open(f"blocks/{tran['id']}.ds","rb")))

		all_pendings = self.db.unconfirmed.find({})

		for pend in all_pendings:
			self.pending_blocks.append(pickle.load(open(f"blocks/{pend['id']}.ds","rb")))

	def addBlock(self,block):
		algo = sha256()
		algo.update(str(block.transaction).encode('utf-8'))
		temp_hash = algo.hexdigest()
		if block.intergriy_hash == temp_hash:
			if block.confirmation >= 3:
				block.prev_hash =  self.blocks[-1].current_hash
				if block in self.blocks:
					print("already added")
				else:
					block.makePersist() 
					self.blocks.append(block)
					print("block added")
			else:
				print(f"[{block.confirmation}] : block confirmation below approve number")
		else:
			print("integrity error block")


	def mineBlock(self,block):
		while True:
			cur_hash = block.makeHash()
			# print(f"hash : {cur_hash} ~ difficulty:{block.nonce}")
			if cur_hash[:self.difficulty] == "0"*self.difficulty:
				block.incr_confirmation()
				block.makePersist()
				if block.confirmation >=3:
					block.prev_hash=self.blocks[-1].current_hash
				self.addBlock(block)
				break






