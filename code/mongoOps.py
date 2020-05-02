from pymongo import MongoClient
from config import mongo
from time import time

class MongoObject():
	def __init__(self):
		# create Mongo connection

		# client = MongoClient(f"mongodb+srv://rohit:{mongo['password']}@rohit-mongo-scv25.mongodb.net/test?retryWrites=true&w=majority")
		client = MongoClient(mongo['serveraddr'])

		self.db = client[mongo['dbname']]

	def insert_document(self, doc, coll):
		if coll=='books':
			resp = self.db[coll].find_one({'_id':doc['_id']})
			if not resp:
				self.db[coll].insert_one(doc)
			else:
				contributors = resp['contributors']
				# print(contributors)
				# TODO : add user to the list of contributors if the user is a new contributor

		elif coll=='users':
			resp = self.db[coll].find_one({'_id':doc['_id']})
			if not resp:
				self.db[coll].insert_one(doc)
			else:
				contributions = list(set(resp['contributions'] + doc['contributions']))
				self.db[coll].update_one({'_id':doc['_id']}, { "$set": { "contributions": contributions } })
		
		elif coll=="notes":
			resp = self.db[coll].find_one({'_id':doc['_id']})
			if not resp:
				self.db[coll].insert_one(doc)
			else:
				updated_contributors = list(set(resp['contributors'] + doc['contributors']))
				if len(updated_contributors)>len(resp['contributors']):
					
					self.db[coll].update_one({'_id':doc['_id']}, { "$set": { "contributors": updated_contributors } })
					
					significance = resp['significance']
					self.db[coll].update_one({'_id':doc['_id']}, { "$set": { "significance": significance+1 } })
		
	def update_last_sent(self, _id):
		try:
			self.db['notes'].update_one({'_id':_id}, { "$set": { "last_sent": int(time()) } })
		except Exception as e:
			print('Problem in saving last_sent' + e)