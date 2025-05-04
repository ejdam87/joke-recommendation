from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS
import pandas as pd

from utils.paths import JOKE_CONTENT, JOKE_LABELS, JOKES_LABELED, RATING_MATRIX, U, V, R
from recommendation.svd_recommender import SVDRecommender
from recommendation.cb_recommender import ContentBasedRecommender
from recommendation.random_recommender import RandomRecommender


PRODUCTION = True


if PRODUCTION:
    app = Flask(__name__, static_folder="../frontend/jokes-ui/output")
else:
    app = Flask(__name__)

if not PRODUCTION:
    CORS(app) # necessary only for the development


svd_recommender = SVDRecommender(U, V, R, 1)
cb_recommender = ContentBasedRecommender(JOKE_LABELS, JOKES_LABELED, RATING_MATRIX)
random_recommender = RandomRecommender(RATING_MATRIX)

recommenders = [svd_recommender, cb_recommender, random_recommender]


@app.route("/", methods=["GET"])
def get_index() -> Response:
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/<path:path>")
def get_static(path: str) -> Response:
    return send_from_directory(app.static_folder, path)


@app.route("/get_jokes", methods=["GET"])
def get_jokes() -> Response:
    df = pd.read_csv(JOKE_CONTENT)
    data = dict(zip(df["jokeId"], df["jokeText"]))
    return jsonify( {"data" : data} )


@app.route("/get_profile", methods=["POST"])
def get_profile() -> Response:
    data = request.get_json()
    uid = data["uid"]
    profile = svd_recommender.user_ratings(uid) # should be same for all systems
    if profile is not None:
        profile = { int(k) : round(v, 2) for k, v in profile.items() }
    return jsonify( {"profile" : profile} )


@app.route("/new_profile", methods=["GET"])
def new_profile() -> Response:
    uid = -1
    for recommender in recommenders:
        uid = recommender.add_user()

    assert uid != -1
    return jsonify( {"uid" : uid} )

# --- Recommendation
@app.route("/get_recommendation_cb", methods=["POST"])
def get_recommendation_cb() -> Response:
    data = request.get_json()
    uid = data["uid"]
    result = [int(j) for j in cb_recommender.recommend(uid, 6)]
    return jsonify( {"recommendation" : result} )

@app.route("/get_recommendation_svd", methods=["POST"])
def get_recommendation_svd() -> Response:
    data = request.get_json()
    uid = data["uid"]
    result = [int(j) for j in svd_recommender.recommend(uid, 6)]
    return jsonify( {"recommendation" : result} )

@app.route("/get_recommendation_random", methods=["POST"])
def get_recommendation_random() -> Response:
    data = request.get_json()
    uid = data["uid"]
    result = [int(j) for j in random_recommender.recommend(uid, 6)]
    return jsonify( {"recommendation" : result} )
# ---

@app.route("/submit_rating", methods=["POST"])
def submit_rating() -> Response:
    data = request.get_json()
    uid = data["uid"]
    jid = data["jid"]
    rating = data["rating"]

    for recommender in recommenders:
        recommender.submit_rating(uid, jid, rating)

    return jsonify({'message': 'POST request successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
