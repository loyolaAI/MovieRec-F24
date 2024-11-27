import pandas as pd
import random
import heapq

# from model.build_colab_model import build_colab_model  # Comment if running locally
from build_colab_model import build_colab_model  # Uncomment if running locally


def get_top_recs(predictions, num_recs):
    """
    Get the top N recommendations from the predictions.

    Parameters:
    predictions (list): A list of predictions from the collaborative-based model.
    num_recs (int): The number of recommendations to return.

    Returns:
    list: A list of tuples containing the movie name and the predicted rating.
    """
    # top_n is a list of tuples that has the movie name and the predicted rating
    top_n = [(iid, est) for _, iid, _, est, _ in predictions]
    # Use heapq to find the top N recommendations more efficiently
    return heapq.nlargest(num_recs, top_n, key=lambda x: (x[1], random.random()))


def run_colab_model(algo, df, user_name, accuracy, num_recs=10, obscureness=5):
    """
    Run the collaborative-based model to get movie recommendations for a user.

    Parameters:
    algo (object): The collaborative-based model object.
    df (DataFrame): The DataFrame containing the user ratings data.
    user_name (str): The user name for which to get recommendations.
    accuracy (float): The accuracy of the model.
    num_recs (int): The number of recommendations to return.
    obscureness (int): The level of obscureness for the recommendations.

    Returns:
    list: A list of dictionaries containing the film_id, predicted_rating, and unclipped_rating.
    """

    # Filter out movies the user has already rated
    rated_movies = df[df["user_name"] == user_name]["film_id"].tolist()

    # Determine the rating threshold based on obscureness and accuracy
    popularity_thresholds_samples = [12, 20, 41, 61, 90, 123, 165, 206, 247, 288]
    rating_threshold = max(1, int(popularity_thresholds_samples[obscureness] * accuracy))

    # Create a review count DataFrame
    review_count_df = df["film_id"].value_counts().reset_index()
    review_count_df.columns = ["film_id", "review_count"]

    # Filter movies by review count and obscureness threshold
    review_count_df = review_count_df[review_count_df["review_count"] <= rating_threshold]

    # Identify unwatched movies by the user that are within the desired popularity range
    unwatched_movies = set(review_count_df["film_id"]) - set(rated_movies)

    # Prepare the prediction set for all unwatched movies
    prediction_set = [(user_name, film_id, 0) for film_id in unwatched_movies]

    # Get predictions
    predictions = algo.test(prediction_set)

    # Get top recommendations
    top_recs = get_top_recs(predictions, num_recs)

    # Define result list with film_id, predicted_rating, and unclipped_rating
    res = [{"film_id": x[0], "predicted_rating": x[1], "unclipped_rating": x[1]} for x in top_recs]

    # Adjust for ratings equal to 10
    for i, prediction in enumerate(res):
        if prediction["predicted_rating"] == 10:
            res[i]["unclipped_rating"] = float(
                algo.predict(user_name, prediction["film_id"], clip=False).est
            )

    # Sort the recommendations by unclipped rating in descending order
    res.sort(key=lambda x: x["unclipped_rating"], reverse=True)

    return res


# Sample use case
if __name__ == "__main__":
    # Define accuracy to something small, since this is a just a sample use case
    accuracy = 0.2

    # Load sample user ratings data (limit for faster testing)
    size_of_all_users_ratings = 1459852
    df = pd.read_csv(
        "./model/data/all_users_ratings.csv.gz",
        compression="gzip",
        nrows=int(size_of_all_users_ratings * accuracy),
    )

    # Load user data for model
    user_data = pd.read_csv("model/data/sample_user_data.csv")

    # Build the collaborative-based model
    algo, df = build_colab_model(df, user_data, "SVD")

    # Get recommendations for a specific user
    recs = run_colab_model(algo, df, "nathannjohnson", accuracy, 20, 3)

    # Print recommended movies for the user
    for rec in recs:
        movie_name = rec.get("film_id")
        rating = rec.get("unclipped_rating")
        print(f"{movie_name} {round(rating, 2)}")
