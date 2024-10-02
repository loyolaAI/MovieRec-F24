# Most likely won't need all of these, but will need at least some
from collections import defaultdict

from surprise import Dataset
from surprise import SVD
from surprise import Reader
from surprise.model_selection import GridSearchCV
from surprise import SVD
from surprise.dump import load

import pickle
import pandas as pd
import random

import os


"""
FUNCTION get_top_recs(predictions, n=20):
    top_rec = CREATE list of tuples (movie_id, estimated_rating) from predictions
    SORT top_rec by estimated_rating and a random tiebreaker, in descending order
    RETURN the top n items from top_rec
"""

def run_colab_model(algo, user_data, movies, num_recs=25):
    """
    WE need to load the .pkl file and run the model on movies the given user has not seen
    """

    # Identify movies the user has not watched
    # Call get_unwatched_movies in get_user_data.py 
    # unwatched_movies = get_unwatched_movies(user_data)
    # prediction_set = CREATE list of tuples (username, movie_id, 0) for each movie in unwatched_movies

    # Get predictions from the algorithm
    # predictions = TEST algorithm using prediction_set
    # predictions = algo.test(prediction_set)
    # Call the get_top_recs to get the highest rated recommendations 
    # top_recs = get_top_recs(predictions, num_recommendations)

    # Get movie details from "movies.csv.gz" file
    # Using the movie name we got recommended, we can pull info from the csv we have 
    # to get the year, actors, ect
    # res = more_movie_info

    # Because the way scikit-learn SVD works we may need to adjust the ratings
    # Adjust the unclipped rating if necessary
    # FOR each prediction in return_object:
    #     IF predicted_rating == 10:
    #         ADJUST unclipped_rating using algorithm.predict with clipping disabled

    # Sort the return object by unclipped_rating in descending order
    # SORT res by unclipped_rating in descending order
    # RETURN return_object


if __name__ == "__main__":
    """
    algo = Open the model file (.pkl)
    movies = Open the list of movies (data/films.csv.gz)
    Get the movies the user has watched
    Normally we would scrap the data and then call the "get_movie_info" method
    Within get_user_data.py for this data, instead we use the sample data.
    user_data = pd.read_csv("./data/sample_user_data.csv")
    recommendations = run_colab_model(algo, user_data, movies)
    print(recommendatios)
    """
    