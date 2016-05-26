import pandas as pd

def jaccard_similarity(list1, list2):
    overlap = list(set(list1) & set(list2))
    join = list(set(list1 + list2))
    return 1.0 * len(overlap) / len(join)


def pos_filter(df, id_x, id_y, pos_x, pos_y, theta):
    text_x = df.loc[id_x].text
    text_y = df.loc[id_y].text
    max_overlap = min(len(text_x) - pos_x - 1, len(text_y) - pos_y - 1)
    max_overlap += len(list(set(text_x[:pos_x+1]) & set(text_y[:pos_y+1])))
    sim = 1.0 * max_overlap / (len(text_x) + len(text_y) - max_overlap)
    return sim > theta


def suf_filter(df, id_x, id_y, pos_x, pos_y, theta):
	# TODO: Add the filter
	return True