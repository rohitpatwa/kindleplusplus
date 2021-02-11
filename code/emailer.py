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



def get_random_note(test, mongo):
	query = {'last_sent':{'$lte': int(time()) - 1296000}}
	count = mongo.db['notes'].count_documents(query)
	rand = randint(0,count-1)
	cursor = mongo.db['notes'].find(query).skip(rand).limit(1)
	for d in cursor:
		if not test:
			mongo.update_last_sent(d['_id'])
		return d


def fire():
	mongo = MongoObject()
	random_note = get_random_note(args.test, mongo)
	book_doc = mongo.db['books'].find_one({'_id':random_note['book_id']})
	book_name, authors = book_doc['book_name'], ','.join(book_doc['authors'])
	mailer(book_name, authors, random_note['note'], args.test)
	print(f'Email sent at {str(datetime.now()).split(".")[0]}')


if __name__=="__main__":
	files = os.listdir()
	if 'mailer_logs.txt' in files:
		f = open('mailer_logs.txt', 'r')
		last_sent = datetime.strptime(f.readlines()[-1][14:-1], '%Y-%m-%d %H:%M:%S')
		now = datetime.now()
		if (now-last_sent).total_seconds()/3600 > 23:
			fire()
		else:
			pass

	else:
		fire()