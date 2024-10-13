# Might not need all of imports or you might need more than this
import pandas as pd
import pickle

from surprise import Dataset
from surprise import Reader
from surprise import SVD

from surprise.model_selection import cross_validate
from surprise.dump import dump

import random
import numpy as np


def build_colab_model(df: pd.DataFrame, user_data: pd.DataFrame, accuracy: float = 0.1):
    """
    We need to add the users ratings into the entire dataset and
    then create the .pkl file / model using SVD
    """

    # Based on how "accurate" the user wants the model to be is how much data we use.
    # accuracy ranges from 0 < accuracy <= 1. Where the number is the percentage of the
    # Dataset that we use to recommend movies. Default is set to 0.1 which gives good recs
    # But does not take too long
    truncate = len(df) * accuracy

    # Remove accuracy amount of the data, to make recommendation faster.
    print("#### Splice the movies dataset")
    df = df.head(int(truncate))

    # Rename the columns so we can append to entire dataframe
    user_data.rename(
        columns={"username": "user_name", "Movie_name_slug": "film_id", "star_rating": "rating"},
        inplace=True,
    )

    # concatenate df1 and df2
    df = pd.concat([df, user_data[["user_name", "film_id", "rating"]]], axis=0, ignore_index=True)
    print("#### Combine the movies dataset and the users movies")
    # Delete the user_data to free up memory
    # del user_data

    # Delete and duplicated that are in the file
    df.drop_duplicates(inplace=True)

    print(df.tail())

    # Load all of the data into the surprise Dataset library using a scale from
    # 1 to 10, 1 being a .5 star rating and 10 being a 5 star rating
    reader = Reader(rating_scale=(1, 10))
    print("#### Load data into scikit Dataset")
    data = Dataset.load_from_df(df[["user_name", "film_id", "rating"]], reader)
    print(data)
    # Delete the df to free up memory
    del df

    # Configure algorithm
    print("#### Configure the algorithm")
    algo = SVD()
    print(algo)

    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)

    print("#### Fit the algorithm onto the dataset")
    print(algo)

    return algo

    # Step 5: Delete the dataframe to free memory
    # DELETE dataframe

    # Step 6: Initialize the SVD algorithm
    # algorithm = INITIALIZE SVD algorithm
    # something like
    # algo = SVD()
    # cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)

    # Step 7: Prepare the dataset for training
    # training_set = BUILD full training set from dataset
    # something like
    # trainingSet = data.build_full_trainset()

    # Step 8: Train the algorithm with the training set
    # FIT algorithm using training_set
    # something like
    # algo.fit(trainingSet)

    #  Step 9: Return the trained algorithm
    # RETURN algorithm


def dump_model_into_pickle(algo):
    """
    Method that takes the trained algorithm and dumps it into a .pkl file
    """
    dump("models/initial_model.pkl", predictions=None, algo=algo, verbose=1)


if __name__ == "__main__":
    df = pd.read_csv("./data/ratings.csv.gz", compression="gzip")
    # Normally we would scrap the data and then call the "get_movie_info" method
    # Within get_user_data.py for this data, instead we use the sample data.
    user_data = pd.read_csv("./data/sample_user_data.csv")
    algo = build_colab_model(df, user_data, 0.05)
    # dump_model_into_pickle(algo)
