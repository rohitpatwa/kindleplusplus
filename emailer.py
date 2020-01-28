from sendMail import sendMail as mailer
from notesParser import MongoObject
from random import randint
from ner import ner


def get_random_note():
	
	count = mongo.db['notes'].find().count()
	rand = randint(0,count-1)
	cursor = mongo.db['notes'].find().skip(rand).limit(1)
	for d in cursor:
		return d

mongo = MongoObject()
random_note = get_random_note()
doc = mongo.db['books'].find_one({'_id':random_note['book_id']})
book_name, authors = doc['book_name'], ','.join(doc['authors'])
mailer(book_name, authors, random_note['note'])