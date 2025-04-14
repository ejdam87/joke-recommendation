from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import pandas as pd

from utils.paths import JOKE_CONTENT

app = Flask(__name__)
CORS(app) # necessary only for the development


@app.route("/get_jokes", methods=["GET"])
def get_jokes() -> Response:
    df = pd.read_csv(JOKE_CONTENT)
    data = dict(zip(df["jokeId"], df["jokeText"]))
    return jsonify( {"data" : data} )


@app.route("/get_recommendation", methods=["POST"])
def get_recommendation() -> Response:
    data = request.get_json()
    profile = data["profile"]
    print(profile)
    return jsonify( {"data" : [5, 6, 7, 8, 12, 10]} )


if __name__ == '__main__':
    app.run(debug=True)
