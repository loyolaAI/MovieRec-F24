import pandas as pd
import numpy as np
import random

from surprise import Dataset
from surprise import Reader


def build_colab_model(df, user_data, model_type: str):
    """
    Method to build the collaborative based filtering model
    Takes in
    df : pd.dataframe, the dataframe of all the movies we're recommending
    user_data : pd.dataframe, the dataframe with all the users data

    returns
    algo : the SVD algorithm
    """

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

    # user_data is now in the main movie df so we don't need it, i.e. delete it
    del user_data

    # Load all of the data into the surprise Dataset library using the scale from
    # 1 to 10, 1 being a .5 star rating and 10 being a 5 star rating
    reader = Reader(rating_scale=(1, 10))

    # We now load the data from the dataframe into a scikit-learn Dataset object
    # This allows it be used by SVD
    data = Dataset.load_from_df(df[["user_name", "film_id", "rating"]], reader)

    # Load the model if a valid argument
    if model_type.lower() == "svd":
        # Initialize the singular value decomposition from scikit-learn surprise library.
        from surprise import SVD

        algo = SVD()
    elif model_type.lower() == "baseline":
        # Initialize the BaseLineOnly model from scikit-learn surprise library.
        from surprise import BaselineOnly

        algo = BaselineOnly()
    else:
        # You can only run the model with two types, SVD and BaseLine
        # so if the type is invalid throw an error.
        raise ValueError("Invalid model type. Choose 'SVD' or 'BaseLine'.")

    # Fit the SVD algorithm onto the combined full-dataset with the users data
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)

    # Return the trained SVD algorithm
    return algo, df


# Sample use case
if __name__ == "__main__":
    # just using sample accuracy and user data, for proof of concept
    accuracy = 0.05
    size_of_all_users_ratings = 1459852
    df = pd.read_csv(
        "model/data/all_users_ratings.csv.gz",
        compression="gzip",
        nrows=int(size_of_all_users_ratings * accuracy),
    )
    user_data = pd.read_csv("model/data/sample_user_data.csv")
    algo, _ = build_colab_model(df, user_data, "SVD")
    print(f"algo = {algo}")
