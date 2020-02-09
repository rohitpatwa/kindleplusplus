"""
get a random note and send an email through SendMail utility.
Update the last send info too.
"""


from sendMail import sendMail as mailer
from mongoOps import MongoObject
from random import randint
from ner import ner
import argparse
from time import time
import os, sys
from datetime import datetime
os.chdir(sys.path[0])


parser = argparse.ArgumentParser('Take input file paths')
parser.add_argument('-t', '--test', help='test run')
args = parser.parse_args()



def get_random_note():
	query = {'last_sent':{'$lte': int(time()) - 1296000}}
	count = mongo.db['notes'].find(query).count()
	rand = randint(0,count-1)
	cursor = mongo.db['notes'].find(query).skip(rand).limit(1)
	for d in cursor:
		mongo.update_last_sent(d['_id'])
		return d

mongo = MongoObject()
random_note = get_random_note()
book_doc = mongo.db['books'].find_one({'_id':random_note['book_id']})
book_name, authors = book_doc['book_name'], ','.join(book_doc['authors'])
mailer(book_name, authors, random_note['note'], args.test)
print(f'Email sent at {str(datetime.now()).split(".")[0]}')