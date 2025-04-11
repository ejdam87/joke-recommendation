from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from utils.paths import JOKE_CONTENT

app = Flask(__name__)
CORS(app) # necessary only for the development


@app.route("/get_jokes", methods=["GET"])
def get_jokes():
    df = pd.read_csv(JOKE_CONTENT)
    data = dict(zip(df["jokeId"], df["jokeText"]))
    return jsonify( {"data" : data} )


if __name__ == '__main__':
    app.run(debug=True)
