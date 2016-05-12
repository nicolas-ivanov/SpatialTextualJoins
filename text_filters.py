


def jaccard_similarity(list1, list2):
    overlap = list(set(list1) & set(list2))
    join = list(set(list1 + list2))
    return 1.0 * len(overlap) / len(join)


