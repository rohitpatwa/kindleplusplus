import pandas as pd
import re
import hashlib
from pymongo import MongoClient
from config import mongo
import numpy as np

# parse csv

class Parser():
	def __init__(self, path=None):
		if path:
			self.path = path
			self.notes = pd.read_csv(path)


	def parse(self):
		self.book_info = self.get_book_info()
		self.user = self.process_user()
		self.highlights = self.process_highlights()

	def get_book_info(self):
		book_name = self.notes.loc[0][0]
		book_hash = hashlib.md5(book_name.lower().encode('UTF-8')).hexdigest()
		
		authors = self.notes.loc[1][0]
		authors = self.clean_authors(authors)
		
		book = {
			'_id':book_hash,
			'book_name':book_name,
			'authors':authors,
			'contributors':[],
			'subscribers':[],
			'notes':[],
			'genre':[]
		}
		return book

	def clean_authors(self, authors):
		a = re.sub(r'\bwritten by\.?\b(.*)', r'\1', authors, flags=re.IGNORECASE)
		a = re.sub(r'\bby\.?\b(.*)', r'\1', a, flags=re.IGNORECASE)
		a = re.sub(r'(.*)\band\b(.*)', r'\1,\2', a, flags=re.IGNORECASE)
		a = a.split(',')
		a = [x.strip() for x in a]
		return a

	def get_note_hash(self, note):
		note = re.sub(r'(.*\w)[^a-zA-Z0-9]+', r'\1', note)
		note = re.sub(r'^[^a-zA-Z0-9]+(\w.*)', r'\1', note)
		note_hash = hashlib.md5(note.encode('UTF-8')).hexdigest()
		return note_hash
		

	def process_highlights(self):
		highlights = self.notes[7:]
		res = []
		for i in highlights.index:
			row = highlights.loc[i]
			page_no, note = row[1], row[3]

			if not isinstance(note, str) or not note.strip():
				continue
			note_hash = self.get_note_hash(note)

			res.append({
					'_id':note_hash,
					'book_id':self.book_info['_id'],
					'note':note,
					'page_no':page_no,
					'curculate':True,
					'significance':0,
					'last_sent' : 0,
					'contributors' : [self.user['_id']],
					'genre' : []
				})
		return res

	def process_user(self):
		if '___' in self.path:
			user_info = re.sub(r'.*___(.*)', r'\1', self.path)
			name, email = user_info.split('<')
			name = re.sub(r'\s+', ' ', name)
			email = re.sub(r'(.*)>.*', r'\1', email)
			email_hash = hashlib.md5(email.lower().encode('UTF-8')).hexdigest()
			
			user = {
				'_id':email_hash,
				'email':email,
				'name':name,
				'contributions':[self.book_info['_id']],
				'subscriptions':[],
				'reading_quality': 0,
				'frequency':0
			}
			return user
		return {}



class MongoObject():
	def __init__(self):
		# create Mongo connection
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
				
				