import cPickle
from flask import Flask

from ppjoin import ppjoin

app = Flask(__name__)

@app.route('/ppjoin', methods=['POST'])
def exec_ppjoin(theta=0.33):
    f = open("data/miami1000.pkl", "rb")
    data = cPickle.load(f)
    return ppjoin(data, theta)
