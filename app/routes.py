from flask import request, jsonify, render_template

from app.functions.movie_recommender import movie_recommendation
from app.mockdata import data


def init_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html", data=data)

    @app.route("/get-movies", methods=["GET"])
    def getMovies():
        return jsonify(data)

    @app.route("/set-rating", methods=["POST"])
    def setRating():
        newData = request.json
        data[int(newData["id"])]["personalRating"] = newData["rating"]

        return jsonify(data)

    # Recommendation
    @app.route("/recommend", methods=["POST"])
    def recommend():
        data = request.json
        recommendation = movie_recommendation([data["input"]])  # Adjust based on your input format
        return jsonify({"recommendations": recommendation.tolist()})

    # Fetch Movie Data
    @app.route("/movie/<int:movie_id>", methods=["GET"])
    def fetch_movie_data(movie_id):
        # Validity Check
        # Fetch using 'movie_data' function
        # Throw exception if there is not movie data
        return

    # Search For Movie(s)
    @app.route("/search", methods=["GET"])
    def search():
        # Validity Check
        # Movie Search
        # Throw exception if there is no movie, or give similar
        return
