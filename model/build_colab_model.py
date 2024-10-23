import pandas as pd
import numpy as np
import random

try:
    from surprise import Dataset
    from surprise import Reader
    from surprise import SVD
except ModuleNotFoundError:
    raise Exception(
        "You need to install the scikit-surprise library. \n"
        "Please refer to the 'install_surprise.md' under tutorials."
    )

## Not needed for now because we don't dump anything
# from surprise.dump import dump
# import pickle


def build_colab_model(df, user_data, accuracy=0.1):
    # Set random seed so that returned recs are always the same for same user with same ratings
    # Not necessary, but good for testing because we want to make sure all movie recs are the
    # same between runs
    my_seed = 7
    random.seed(my_seed)
    np.random.seed(my_seed)

    """ Based on how "accurate" the user wants the model to be is how much data we use.
    accuracy ranges from 0 < accuracy <= 1. Where the number is the percentage of the
    Dataset that we use to recommend movies. Default is set to 0.1 which gives good enough
    recommendations, but doesn't take too long """

    # concatenate all of the ratings with the users ratings
    df = pd.concat([df, user_data[["user_name", "film_id", "rating"]]], axis=0, ignore_index=True)

    # Load all of the data into the surprise Dataset library using the scale from
    # 1 to 10, 1 being a .5 star rating and 10 being a 5 star rating
    reader = Reader(rating_scale=(1, 10))

    # We now load the data from the dataframe into a scikit-learn Dataset object
    # This allows it be used by SVD
    data = Dataset.load_from_df(df[["user_name", "film_id", "rating"]], reader)

    # Initialize the singular value decomposition from scikit-learn surprise library.
    algo = SVD()

    # Fit the SVD algorithm onto the combined full-dataset with the users data
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)

    # Return the trained SVD algorithm
    return algo


## Don't need this currently, but might need it later, so i'm keeping it
# def dump_model_into_pickle(algo):
#     """
#     Method that takes the trained algorithm and dumps it into a .pkl file
#     """
#     dump("models/initial_model.pkl", predictions=None, algo=algo, verbose=1)


# Sample use case
if __name__ == "__main__":
    # just using sample accuracy and user data, for proof of concept
    accuracy = 0.05
    from get_user_data import get_movie_dataframe

    df = get_movie_dataframe(accuracy)
    user_data = pd.read_csv("./data/sample_user_data.csv")
    algo = build_colab_model(df, user_data, accuracy)
    print(f"algo = {algo}")
