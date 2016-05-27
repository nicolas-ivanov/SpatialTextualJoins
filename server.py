import cPickle
import json
import re

from flask import Flask, render_template, send_from_directory, request

from data_preprocessing import prepare_data, get_inverted_file
from ppj_c import ppj_c
from ppjoin import ppjoin
from stSearch import stTextSearch

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route('/ppjoin', methods=['GET'])
def exec_ppjoin():
    def parse_query(query):
        pattern = re.compile('-sim (0\.\d+) -dist (\d+)(.*)')
        m = pattern.match(query)

        if m:
            sim = float(m.group(1))
            dist = int(m.group(2))
            text = m.group(3)
            return dist, sim, text
        else:
            return None,None,query

    query = request.args.get('q')   # query from search string comes here

    df = prepare_data('data/miami1000.pkl')
    inverted_file = get_inverted_file(df)

    if query:
        theta, epsilon, text = parse_query(query)

        if not theta:
            theta = 0.1
            epsilon = 100

        if text:
            res = stTextSearch(df, text, theta)
        else:
            res = ppj_c(df, theta, epsilon)
    else:
        theta = 0.5
        epsilon = 100
        res = ppj_c(df, theta, epsilon)

    return res

# @app.route('/ppjoin', methods=['GET'])
# def exec_ppjoin():
#     # theta = request.args.get('theta') or 0.33
#     # theta = float(theta)
#     query = request.args.get('q')   # query from search string comes here
#
#     df = prepare_data('data/miami1000.pkl')
#     inverted_file = get_inverted_file(df)
#     theta = 0.5
#     epsilon = 100
#
#     res = stTextSearch(df, text, theta)
#
#     return res


if __name__ == "__main__":
    app.run(debug=True)