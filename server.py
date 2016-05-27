import cPickle
import json
from flask import Flask, render_template, send_from_directory, request

from ppjoin import ppjoin

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route('/ppjoin', methods=['GET'])
def exec_ppjoin():
    theta = request.args.get('theta') or 0.33
    query = request.args.get('q')   # query from search string comes here
    theta = float(theta)

    f = open("data/miami1000.pkl", "rb")
    data = cPickle.load(f)

    res = ppjoin(data, theta).keys()

    return json.dumps([(str(t[0]), str(t[1])) for t in res])


if __name__ == "__main__":
    app.run(debug=True)