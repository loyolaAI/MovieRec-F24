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

from build_colab_model import build_colab_model
from get_user_data import get_unwatched_movies
from scraping import scrape_and_make_dataframe

"""
FUNCTION get_top_recs(predictions, n=20):
    top_rec = CREATE list of tuples (movie_id, estimated_rating) from predictions
    SORT top_rec by estimated_rating and a random tiebreaker, in descending order
    RETURN the top n items from top_rec
"""


def get_top_recs(predictions, num_recs):
    top_n = [(iid, est) for uid, iid, true_r, est, _ in predictions]
    top_n.sort(key=lambda x: (x[1], random.random()), reverse=True)

    return top_n[:num_recs]


def run_colab_model(algo, user_data, movies, accuracy: float, username, num_recs=25):
    """
    WE need to load the .pkl file and run the model on movies the given user has not seen
    """

    # Identify movies the user has not watched, type list.
    print("#### Get all the movies the user has not watched")
    unwatched_movies = get_unwatched_movies(user_data, movies, accuracy)
    print(unwatched_movies[:10])

    # Create the prediction set which will hold a given users film and the predicted rating for it.
    prediction_set = [(username, film_id, 0) for film_id in unwatched_movies]

    # predict!
    predictions = algo.test(prediction_set)
    print("#### Get all the movies rating predictions from the model")
    print("#### Sort and get the top recommendations")
    print("#### print out the recommendations")
    top_recs = get_top_recs(predictions, num_recs)
    # Print the recommended items for user
    for prediction in top_recs:
        print(f"{prediction[0]}: {round(prediction[1], 2)}")

    return "lol"

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
    print(recommendation)
    """

    accuracy = float(input("How accurate do you want the model to be (range 0.01-1.0) "))
    # Normally we would scrap the data and then call the "get_movie_info" method
    # Within get_user_data.py for this data, instead we use the sample data.
    username = input("What is your letterboxd username ")
    print("#### scraping User data")
    user_data = scrape_and_make_dataframe(username)
    print(user_data)
    print("#### Scraping user data completed")
    print("#### Loading in movies dataset")
    df = pd.read_csv("./data/ratings.csv.gz", compression="gzip")
    print(df.head(10))
    print("#### Done loading movies dataset")
    print("#### Build the colab model")
    algo = build_colab_model(df, user_data, accuracy)
    print("#### Run the colab model")
    recs = run_colab_model(algo, user_data, df, accuracy, username, 20)
