import cPickle
import pandas as pd

from text_utils import preprocess_text, tokenizer, get_ordering, canonicalize
from space_utils import get_coordinates
from math import ceil


def prepare_data(path):
    # read file
    with open(path, 'rb') as file:
        data = cPickle.load(file)
    # prepare index
    ids = [str(row['_id']) for row in data]  # text ids
    # prepare text
    raw_text = [row['payload']['text'] for row in data]  # list of raw text data
    # prepare geo
    coordinates = [get_coordinates(row) for row in data]  # [lat, lng] pairs
    lat = [c[0] for c in coordinates]
    lng = [c[1] for c in coordinates]
    # create df
    df = pd.DataFrame({
        'text': raw_text,
        'lat': lat,
        'lng': lng},
        index=ids)

    # text processing
    df.text = df.text.apply(lambda text: preprocess_text(text))  # text preprocessing
    df.text = df.text.apply(tokenizer)
    ordering = get_ordering(df.text.values)
    df.text = df.text.apply(lambda text_list: canonicalize(text_list, ordering))

    return df


def get_inverted_file(df):
    inv = {}
    for id in df.index.values:
        text = df.loc[id].text
        for word in text:
            if word in inv:
                inv[word].append(id)
            else:
                inv[word] = [id]
    return inv


def group_objects(df, theta):
    group_dict = {}
    for id in df.index.values:
        text = df.loc[id].text
        probe_pref_len = len(text) - int(ceil(theta * len(text))) + 1
        ppref = text[:probe_pref_len]
        if ppref in group_dict:
            group_dict[ppref].append(id)
        else:
            group_dict[ppref] = [id]

    return group_dict
