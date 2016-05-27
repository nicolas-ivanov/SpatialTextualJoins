from data_preprocessing import prepare_data, get_inverted_file, group_objects
from text_filters import jaccard_similarity, pos_filter, suf_filter
from math import ceil
from collections import Counter
import time
import itertools
import json

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
    return resultJSON(df, pairs)


# -----------------------------------------------------------------------------------------------------------------------
def ppjoin_group(df, inverted_file, theta, group_dict):

    pairs = {}
    term_index = {t:[] for t in inverted_file.keys()}

    for ppref in group_dict:
        group = group_dict[ppref]
        id_x = group[0]
        overlap_x = Counter()
        text_x = df.loc[id_x].text
        if len(text_x) == 0:
            continue

        index_pref_len = len(text_x) - int(ceil(2 * theta * len(text_x)/ (theta+1))) + 1

        for pos_x in range(len(ppref)):
            t = ppref[pos_x]
            for (id_y, pos_y) in term_index[t]:
                text_y = df.loc[id_y].text
                if len(text_y) < theta * len(text_x):
                    continue
                elif (pos_filter(df, id_x, id_y, pos_x, pos_y, theta)) \
                        & (suf_filter(df, id_x, id_y, pos_x,pos_y, theta)):
                    overlap_x[id_y] += 1
                else:
                    overlap_x[id_y] = -10000
            if pos_x <= index_pref_len:
                for id_gr in group:
                    term_index[t].append((id_gr, pos_x))

        for id_gr in group:
            pairs = verify(df, pairs, id_gr, overlap_x, theta)

        for pair in itertools.combinations(group, 2):
            pairs = verify(df, pairs, pair[0], {pair[1]:len(ppref)}, theta)

    return resultJSON(df, pairs)


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


def resultJSON(df, pairs):
    pairs = pairs.keys()
    result = []
    for pair in pairs:
        cell = []
        for id_ in pair:
            obj = df.loc[id_]
            json_ = {
                "id": id_,
                "long": str(obj.lng),
                "lat": str(obj.lat),
                "text": obj.raw_text
            }
            cell.append(json_)
        result.append(cell)
    return json.dumps(result)

# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    df = prepare_data('data/miami1000.pkl')
    inverted_file = get_inverted_file(df)
    theta = 0.8

    start_time = time.time()
    pairs = ppjoin(df, inverted_file, theta)
    print "Time elapsed:", time.time() - start_time
    print pairs[0]
    print 'Total: ', len(pairs)
    for pair in pairs:
        id1 = pair[0]["id"]
        id2 = pair[1]["id"]
        print jaccard_similarity(df.loc[id1].text, df.loc[id2].text)

    group_dict = group_objects(df, theta)
    start_time = time.time()
    pairs = ppjoin_group(df, inverted_file, theta, group_dict)
    print "Time elapsed:", time.time() - start_time
    print pairs[0]
    print 'Total: ', len(pairs)
    for pair in pairs:
        id1 = pair[0]["id"]
        id2 = pair[1]["id"]
        print jaccard_similarity(df.loc[id1].text, df.loc[id2].text)