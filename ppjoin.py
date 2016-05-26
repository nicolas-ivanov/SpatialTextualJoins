from data_preprocessing import prepare_data, get_inverted_file
from text_filters import jaccard_similarity, pos_filter, suf_filter
from math import ceil
from collections import Counter

# -----------------------------------------------------------------------------------------------------------------------
def ppjoin(df, inverted_file, theta):

    pairs = {}
    term_index = {t:[] for t in inverted_file.keys()}
    
    for id_x in df.index.values:
        overlap_x = Counter()
        text_x = df.loc[id_x].text
        if len(text_x) == 0:
            continue

        probe_pref_len = len(text_x) - int(ceil(theta * len(text_x))) + 1
        index_pref_len = len(text_x) - int(ceil(2 * theta * len(text_x)/ (theta+1))) + 1

        for pos_x in range(probe_pref_len):
            t = text_x[pos_x]
            for (id_y, pos_y) in term_index[t]:
                text_y = df.loc[id_y].text
                if len(text_y) < theta * len(text_x):
                    continue
                elif (pos_filter(df, id_x, id_y, pos_x,pos_y, theta)) \
                        & (suf_filter(df, id_x, id_y, pos_x,pos_y, theta)):
                    overlap_x[id_y] += 1
                else:
                    overlap_x[id_y] = -10000
            if pos_x <= index_pref_len:
                term_index[t].append((id_x, pos_x))
        pairs = verify(df, pairs, id_x, overlap_x, theta)

    return pairs


# Supporting methods
def verify(df, pairs, id_x, overlap_x, theta):
    text_x = df.loc[id_x].text
    for id_y in overlap_x:
        if overlap_x[id_y] <= 0:
            continue
        text_y = df.loc[str(id_y)].text
        sim = jaccard_similarity(text_x, text_y)
        if sim >= theta:
            pairs[(id_x, id_y)] = 0
    return pairs

# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    df = prepare_data('data/miami1000.pkl')
    inverted_file = get_inverted_file(df)
    pairs = ppjoin(df, inverted_file, 0.33)
    res = pairs.keys()
    print 'Total: ', len(res)