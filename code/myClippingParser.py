from notesParser import Parser
import re
import pandas as pd
import hashlib
import numpy as np
import sys
import os

my_clippings_path = sys.argv[1]
f = open(my_clippings_path)


def create_df(book, authors):
	df = pd.DataFrame(columns=[1,2,3,4])
	df.loc[0] = "Your Kindle Notes For:", "", "", ""
	df.loc[1] = book, "", "", ""
	df.loc[3] = f"by {authors}", "", "", ""
	df.loc[4] = "Free Kindle instant preview:", "", "", ""
	df.loc[5] = "https://read.amazon.com/", "", "", ""
	df.loc[6] = "----------------------------------------------", "", "", ""
	df.loc[7] = "", "", "", ""
	df.loc[8] = "Annotation Type", "Location", "Starred?", "Annotation"
	return df
	


dict_of_dfs = {}
p = Parser()

book, authors, note, loc = "", "", "", ""
for line in f.readlines():
	
	if not line.strip():
		continue
	
	# Start of a new clipping
	if not book:
		book = line
		temp = re.split(r'\((?!.*\()', book)
		
		if len(temp)==2:  # author found
			book, authors = temp
		else:  # author not found
			book = temp[0]
		
		book = book.strip()
		book_hash = hashlib.md5(re.sub(r'\W+', '', book).encode('UTF-8')).hexdigest()
		
		if book_hash in dict_of_dfs:
			continue
				
		authors = re.sub(r'\)', '', authors)
		dict_of_dfs[book_hash] = create_df(book, authors)
	
	# Loc info in the highlight	
	elif re.search('- Your Highlight at location ', line):
		loc = re.sub(r'.*Your Highlight at location (.*\d) \|.*\n', r'\1', line)
	
	# End of a note
	elif "=========" in line:
		i = len(dict_of_dfs[book_hash]) + 1
		dict_of_dfs[book_hash].loc[i] = "Highlight (White)",loc, "", note
		book, authors, note, loc = "", "", "", ""

	# Actual note content
	else:
		note = line.strip()

# Create directory if not exists
if not os.path.isdir('parsed_notes'):
    os.mkdir('parsed_notes')

# Save separate .csv files for diffent books
for _hash in dict_of_dfs.keys():
	book_name = dict_of_dfs[_hash].loc[1, 1]
	book_name = f'parsed_{book_name}'
	book_name = re.sub('[\W|_]+', '_', book_name)
	dict_of_dfs[_hash].to_csv(f'parsed_notes/{book_name}.csv', header=None, index=None)