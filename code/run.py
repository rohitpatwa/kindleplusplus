from notesParser import Parser
from mongoOps import MongoObject
import sys


def process(path):
	parser = Parser(path)
	parser.parse()

	mongo = MongoObject()

	mongo.insert_document(parser.book_info, 'books')

	mongo.insert_document(parser.user, 'users')

	for h in parser.highlights:
	    mongo.insert_document(h, 'notes')


if __name__=='__main__':
	path = sys.argv[1]
	process(path)