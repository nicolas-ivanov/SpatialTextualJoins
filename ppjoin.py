import cPickle
import nltk
from text_processing import build_inverted_file, get_ordering, canonicalize, pos_filter, suf_filter, verify, jaccard_similarity
from math import ceil
from collections import Counter

# -----------------------------------------------------------------------------------------------------------------------
def ppjoin(data, theta):

    inv_index, id_dict = build_inverted_file(data)
    ordering = get_ordering(inv_index)
    pairs = {}

    term_index = {}
    for term in inv_index.keys():
        term_index[term] = []


    for id_x in id_dict.keys():
        overlap_x = Counter()

        # canonicalized list of words
        text_x = canonicalize(id_dict[id_x], ordering)
        if len(text_x) == 0:
            continue

        probe_pref_len = len(text_x) - int(ceil(theta * len(text_x))) + 1
        index_pref_len = len(text_x) - int(ceil(2 * theta * len(text_x)/ (theta+1))) + 1

        for pos_x in range(probe_pref_len):
            t = text_x[pos_x]

            for (id_y, pos_y) in term_index[t]:
                text_y = canonicalize(id_dict[id_y], ordering)
                if len(text_y) < theta * len(text_x):
                    continue
                elif (pos_filter(id_x, pos_x, id_y, pos_y, id_dict, ordering, theta)) \
                        & (suf_filter(id_x, pos_x, id_y, pos_y, id_dict, ordering, theta)):
                    overlap_x[id_y] += 1
                else:
                    overlap_x[id_y] = -10000

            if pos_x <= index_pref_len:
                term_index[t].append((id_x, pos_x))

        pairs = verify(id_x, overlap_x, id_dict, theta, pairs)

    return pairs


# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    f = open("data/miami1000.pkl", "rb")
    data = cPickle.load(f)
    inv_index, id_dict = build_inverted_file(data)
    pairs = ppjoin(data, 0.33)
    res = pairs.keys()
    print res
    print id_dict[res[0][0]]
    print id_dict[res[0][1]]
    print jaccard_similarity(id_dict[res[0][0]], id_dict[res[0][1]])