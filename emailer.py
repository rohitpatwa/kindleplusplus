from sendMail import sendMail as mailer
from notesParser import MongoObject
from random import randint


def get_random_note():
	
	count = mongo.db['notes'].count_documents({})
	rand = randint(0,count-1)
	cursor = mongo.db['notes'].find().skip(rand).limit(1)
	for d in cursor:
		return d

mongo = MongoObject()
random_note = get_random_note()
book_name = mongo.db['books'].find_one({'_id':random_note['book_id']})['book_name']
mailer(book_name, random_note['note'])