import cPickle
import pandas as pd

from text_utils import preprocess_text, tokenizer, get_ordering, canonicalize
from space_utils import get_coordinates


def prepare_data(path):
	# read file
	with open(path, 'rb') as file:
		data = cPickle.load(file)
	# prepare index
	ids = [str(row['_id']) for row in data] # text ids 
	# prepare text
	raw_text = [row['payload']['text'] for row in data] # list of raw text data
	# prepare geo
	coordinates = [get_coordinates(row) for row in data] # [lat, lng] pairs
	lat = [c[0] for c in coordinates]
	lng = [c[1] for c in coordinates]
	# create df
	df = pd.DataFrame({
		'text': raw_text,
		'lat': lat,
		'lng': lng},
		index=ids)

	# text processing
	df.text = df.text.apply(lambda text: preprocess_text(text)) # text preprocessing
	df.text = df.text.apply(tokenizer) 
	ordering = get_ordering(df.text.values)
	df.text = df.text.apply(lambda text_list: canonicalize(text_list, ordering))

	return df
