from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # necessary only for the development


@app.route("/example", methods=["GET"])
def example():
    return jsonify( {"data" : "Response from the server"} )

if __name__ == '__main__':
    app.run(debug=True)
