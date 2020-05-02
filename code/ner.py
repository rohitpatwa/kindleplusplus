from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
import pickle

# Read the corpus into a list, 
# each entry in the list is one sentence.


def ner(sent):	
	cess_sents = cess.tagged_sents()

	# Train the unigram tagger
	# uni_tag = ut(cess_sents)


	# Tagger reads a list of tokens.
	# uni_tag.tag(sent.split(" "))

	# Split corpus into training and testing set.
	# train = int(len(cess_sents)*90/100) # 90%

	# Train a bigram tagger with only training data.
	# bi_tag = bt(cess_sents[:train])

	# Evaluates on testing data remaining 10%
	# bi_tag.evaluate(cess_sents[train+1:])

	# Using the tagger.
	# bi_tag.tag(sent.split(" "))
	

	res = []
	common_word = pickle.load(open('spanish_words.pkl', 'rb'))
	for word in sent.split():
		if word in common_word:
			res.append([word, common_word[word]])
	return str(res)


