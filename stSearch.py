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
    for i in xrange(n / 2):
        pair = (d[i], d[i+1])
        pairs.append(pair)
    if n % 2:
        pairs.append((d[-1],))
    return resultJSON(df, pairs)