from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import pandas as pd

from utils.paths import JOKE_CONTENT, U, V, R
from recommendation.svd_recommender import SVDRecommender

app = Flask(__name__)
CORS(app) # necessary only for the development

recommender = SVDRecommender(U, V, R, 5)


@app.route("/get_jokes", methods=["GET"])
def get_jokes() -> Response:
    df = pd.read_csv(JOKE_CONTENT)
    data = dict(zip(df["jokeId"], df["jokeText"]))
    return jsonify( {"data" : data} )


@app.route("/get_profile", methods=["POST"])
def get_profile() -> Response:
    data = request.get_json()
    uid = data["uid"]
    profile = recommender.user_ratings(uid)
    if profile is not None:
        profile = { int(k) : round(v, 2) for k, v in profile.items() }
    return jsonify( {"profile" : profile} )


@app.route("/new_profile", methods=["GET"])
def new_profile() -> Response:
    uid = recommender.add_user()
    return jsonify( {"uid" : uid} )


@app.route("/get_recommendation", methods=["POST"])
def get_recommendation() -> Response:
    data = request.get_json()
    uid = data["uid"]
    result = [int(j) for j in recommender.recommend(uid, 6)]
    return jsonify( {"recommendation" : result} )


@app.route("/submit_rating", methods=["POST"])
def submit_rating() -> Response:
    data = request.get_json()
    uid = data["uid"]
    jid = data["jid"]
    rating = data["rating"]
    recommender.submit_rating(uid, jid, rating)
    return jsonify({'message': 'POST request successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
