import nltk
import numpy as np
from collections import Counter

def preprocess_text(text, stemmer=nltk.PorterStemmer()):
    stemmed_list = []
    words = text.split()
    for word in words:
        word = word.strip('":,.;&!?+-\'')
        if word == '':
            continue
        # hashtags and usernames not stemmed
        if word[0] == '#' or word[0] == '@':
            stemmed_word = word
        else:
            stemmed_word = stemmer.stem(word.lower())
        stemmed_list.append(stemmed_word)
    return stemmed_list


def tokenizer(text_list):
	# each word becomes the unique token
	c = Counter()
	new_list = []
	for word in text_list:
		new_list.append(word + str(c[word]))
		c[word] += 1
	return new_list


def get_ordering(data):
	# data: numpy.ndarray ravel
	ordering = Counter()
	for words in data:
		ordering.update(words)
	return dict(ordering)


def canonicalize(text_list, ordering):
	return sorted(text_list, key= lambda x: ordering[x])

