from notesParser import Parser, MongoObject
import sys


path = sys.argv[1]

parser = Parser(path)
parser.parse()

mongo = MongoObject()

mongo.insert_document(parser.book_info, 'books')

for h in parser.highlights:
    mongo.insert_document(h, 'notes')