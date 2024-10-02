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

def build_colab_model(df, user_data):
    """
    We need to add the users ratings into the entire dataset and 
    then create the .pkl file / model using SVD
    """
    # TODO
    
    # Step 1: Append user's ratings to the original dataframe
    # dataframe = CONCATENATE df with user_data and reset index
    
    # Step 2: Remove duplicate entries from the dataframe
    # REMOVE duplicates from dataframe
    
    # Step 3: Delete the temporary user_dataframe to free memory
    # DELETE user_dataframe
    
    # Step 4: Load data into the Surprise library's dataset with rating scale 1 to 10
    # reader = INITIALIZE rating reader with scale 1 to 10
    # dataset = LOAD dataset from dataframe using columns user_id, movie_id, rating_val and reader
    # Something like whats below
    # data = Dataset.load_from_df(df[["user_id", "movie_id", "rating_val"]], reader)

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
    algo = build_colab_model(df, user_data)
    dump_model_into_pickle(algo)