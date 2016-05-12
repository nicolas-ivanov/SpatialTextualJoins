import cPickle
import nltk
from math import ceil

# -----------------------------------------------------------------------------------------------------------------------
def verify(id_x, overlap_x, id_dict, theta, pairs):
    text_x = id_dict[id_x]
    for id_y in overlap_x:
        if overlap_x[id_y] <= 0:
            continue
        text_y = id_dict[id_y]
        sim = jaccard_similarity(text_x, text_y)
        if sim >= theta:
            pairs[(id_x, id_y)] = 0
    return pairs

# -----------------------------------------------------------------------------------------------------------------------
def pos_filter(id_x, pos_x, id_y, pos_y, id_dict, ordering, theta):
    text_x = canonicalize(id_dict[id_x], ordering)
    text_y = canonicalize(id_dict[id_y], ordering)
    max_overlap = min(len(text_x) - pos_x - 1, len(text_y) - pos_y - 1)

    for word in text_x[:pos_x+1]:
        if word in text_y[:pos_y+1]:
            max_overlap += 1

    sim = 1.0 * max_overlap / (len(text_x) + len(text_y) - max_overlap)
    if sim > theta:
        return True
    else:
        return False

# -----------------------------------------------------------------------------------------------------------------------
def suf_filter(id_x, pos_x, id_y, pos_y, id_dict, ordering, theta):
    text_x = canonicalize(id_dict[id_x], ordering)
    text_y = canonicalize(id_dict[id_y], ordering)
    min_hamming = len(text_x) - pos_x + len(text_y) - pos_y - 2

    for word in text_x[pos_x+1:]:
        if word in text_y[pos_y+1:]:
            min_hamming -= 1

    if min_hamming < 2 * (len(text_y)) - int(ceil(2 * theta * (len(text_x) + len(text_y)/ (theta+1)))) - \
                                                      int(ceil(theta * (len(text_x) + len(text_y)))):

        return True
    else:
        return False


# -----------------------------------------------------------------------------------------------------------------------
def build_inverted_file(data):
    stemmer = nltk.PorterStemmer()
    inv_index = {}
    id_dict = {}

    for tweet in data:
        text = get_text(tweet)
        stemmed_list = preprocess_text(text, stemmer)
        id_dict[tweet[u'_id']] = stemmed_list
        for word in stemmed_list:
            if word in inv_index:
                inv_index[word].append(tweet[u'_id'])
            else:
                inv_index[word] = [tweet[u'_id']]

    return inv_index, id_dict


# -----------------------------------------------------------------------------------------------------------------------
def jaccard_similarity(list1, list2):
    overlap = list(set(list1) & set(list2))
    join = list(set(list1 + list2))
    return 1.0 * len(overlap) / len(join)


# -----------------------------------------------------------------------------------------------------------------------
def get_ordering(inv_index):
    ordered_words = sorted(inv_index, key=lambda w: len(inv_index[w]))
    ordering = {ordered_words[i]:i for i in xrange(len(ordered_words))}
    return ordering

# -----------------------------------------------------------------------------------------------------------------------
def canonicalize(stemmed_list, ordering):
    return sorted(stemmed_list, key=lambda w: ordering[w])


# -----------------------------------------------------------------------------------------------------------------------
def preprocess_text(text, stemmer):
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
            stemmed_word = stemmer.stem(word)
        stemmed_list.append(stemmed_word)

    return stemmed_list


# -----------------------------------------------------------------------------------------------------------------------
def get_text(tweet):
    return tweet[u'payload'][u'text']


# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    f = open("data/miami1000.pkl", "rb")
    data = cPickle.load(f)
    inv_index, id_dict = build_inverted_file(data)
    ordering = get_ordering(inv_index)
    print ordering
    print inv_index
    print jaccard_similarity([u'@EliasibNavarro'], [u'@EliasibNavarro', u'hola'])
