from data_preprocessing import prepare_data, get_inverted_file, group_objects
from text_filters import jaccard_similarity, pos_filter, suf_filter
from ppjoin import verify, resultJSON
from space_utils import find_neighbors, construct_grid
from math import ceil
from collections import Counter
from geopy.distance import vincenty
import time

# -----------------------------------------------------------------------------------------------------------------------
def ppj_c(df, theta, epsilon):

    pairs = {}

    print "Grid contruction"
    grid_dict, grid_shape = construct_grid(df, epsilon)
    grid_cols = grid_shape[1]
    print "Grid: done"

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

    return resultJSON(df, pairs)

# -----------------------------------------------------------------------------------------------------------------------
def ppj_c_grouping(df, theta, epsilon):

    pairs = {}

    print "Grid contruction"
    grid_dict, grid_shape = construct_grid(df, epsilon)
    grid_cols = grid_shape[1]
    print "Grid: done"

    for cell in grid_dict:
        neighbor_cells = find_neighbors(cell, grid_cols)

        for neighbor_cell in neighbor_cells:
            df_cells = df.loc[grid_dict[neighbor_cell] + grid_dict[cell]]

            inverted_file_cells = get_inverted_file(df_cells)
            term_index = {t: [] for t in inverted_file_cells.keys()}

            group_dict = group_objects(df_cells, theta)

            for ppref in group_dict:
                group = group_dict[ppref]
                id_x = group[0]
                overlap_x = Counter()
                text_x = df.loc[id_x].text
                lat_x = df.loc[id_x].lat
                lng_x = df.loc[id_x].lng
                if len(text_x) == 0:
                    continue

                index_pref_len = len(text_x) - int(ceil(2 * theta * len(text_x)/ (theta+1))) + 1

                for pos_x in range(len(ppref)):
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

    return resultJSON(df, pairs)

# -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    df = prepare_data('data/miami1000.pkl')
    theta = 0.8
    epsilon = 50
    start_time = time.time()
    pairs = ppj_c(df, theta, epsilon)
    print "Time elapsed:", time.time() - start_time
    print pairs
    print 'Total: ', len(pairs)

    # start_time = time.time()
    # pairs = ppj_c_grouping(df, theta, epsilon)
    # print "Time elapsed:", time.time() - start_time
    # print pairs
    # print 'Total: ', len(pairs)