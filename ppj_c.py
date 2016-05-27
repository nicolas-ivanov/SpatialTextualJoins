from data_preprocessing import prepare_data, get_inverted_file, group_objects
from text_filters import jaccard_similarity, pos_filter, suf_filter
from space_utils import find_neighbors
from math import ceil
from collections import Counter
from geopy.distance import vincenty
import time

# -----------------------------------------------------------------------------------------------------------------------
def ppj_c(df, theta, epsilon):

    pairs = {}

    grid_dict, grid_cols = construct_grid(df, epsilon)

    for cell in grid_dict:
        neighbor_cells = find_neighbors(cell, grid_cols)

        for neighbor_cell in neighbor_cells:
            df_cells = df.loc[grid_dict[neighbor_cell] + grid_dict[cell]]

            inverted_file_cells = get_inverted_file(df_cells)
            term_index = {t: [] for t in inverted_file_cells.keys()}

            for id_x in df_cells.index.values:
                overlap_x = Counter()
                text_x = df.loc[id_x].text
                lat_x = df.loc[id_x].lat
                lng_x = df.loc[id_x].lng
                if len(text_x) == 0:
                    continue

                probe_pref_len = len(text_x) - int(ceil(theta * len(text_x))) + 1
                index_pref_len = len(text_x) - int(ceil(2 * theta * len(text_x)/ (theta+1))) + 1

                for pos_x in range(probe_pref_len):
                    t = text_x[pos_x]
                    for (id_y, pos_y) in term_index[t]:
                        lat_y = df.loc[id_y].lat
                        lng_y = df.loc[id_y].lng

                        text_y = df.loc[id_y].text
                        if (len(text_y) < theta * len(text_x)) or (vincenty((lat_x, lng_x), (lat_y, lng_y)).km > epsilon):
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
    theta = 0.8
    group_dict = group_objects(df, theta)
    start_time = time.time()
    pairs = ppjoin_group(df, inverted_file, theta, group_dict)
    print "Time elapsed:", time.time() - start_time
    res = pairs.keys()
    print df.loc[res[0][0]].text
    print df.loc[res[0][1]].text
    print 'Total: ', len(res)