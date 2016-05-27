from text_filters import jaccard_similarity
from text_utils import preprocess_text, tokenizer
from ppjoin import resultJSON

def stTextSearch(df, text, theta):
    text = preprocess_text(text)
    text = tokenizer(text)
    d = df.text.apply(lambda x: jaccard_similarity(x, text)>theta)
    d = d.loc[d].index.values
    n = d.shape[0]
    pairs = []
    for i in xrange(n):
        pair = (d[i],)      # build a dummy pair
        pairs.append(pair)
    return resultJSON(df, pairs)