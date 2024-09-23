from flask import request, jsonify, render_template
from app.functions.movie_recommender import movie_recommendation

data = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "generalRating": 4.8,
        "personalRating": 0,
    },
    {
        "id": 2,
        "title": "The Godfather",
        "generalRating": 4.7,
        "personalRating": 0,
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "generalRating": 4.6,
        "personalRating": 0,
    },
    {
        "id": 4,
        "title": "The Lord of the Rings: The Return of the King",
        "generalRating": 4.5,
        "personalRating": 0,
    },
    {
        "id": 5,
        "title": "Pulp Fiction",
        "generalRating": 4.4,
        "personalRating": 0,
    },
    {
        "id": 6,
        "title": "Schindler's List",
        "generalRating": 4.3,
        "personalRating": 0,
    },
]


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
