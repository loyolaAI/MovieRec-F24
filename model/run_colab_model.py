import pandas as pd
import random

# update

from model.build_colab_model import build_colab_model  # Comment if you want to run method locally

# from build_colab_model import build_colab_model # Uncomment if you want to run method locally
# from model.scraping import scrape_and_make_dataframe


# Define function to get top recommendations
def get_top_recs(predictions, num_recs):
    # top_n is a list of tuples that has the movie name and the predicted rating
    top_n = [(iid, est) for uid, iid, true_r, est, _ in predictions]
    # Sort top_n by the predicted rating, sorting from highest to lowest.
    top_n.sort(key=lambda x: (x[1], random.random()), reverse=True)
    # return the spliced list of the top_n recommendations
    return top_n[:num_recs]


def run_colab_model(algo, df, user_name, accuracy, num_recs=10, obscureness=5):
    # Filter out movies the user has already rated
    rated_movies = df[df["user_name"] == user_name]["film_id"].tolist()

    # Get the rating threshold, based on how obscure the user wants the movie
    # We need to take the max because for certain cases where a user wants really
    # obscure movies and they're running on a small amount of data (accuracy is small)
    # rating_threshold would = 0 and we would recommend no movies.
    popularity_thresholds_samples = [12, 20, 41, 61, 90, 123, 165, 206, 247, 288]
    rating_threshold = max(1, int(popularity_thresholds_samples[obscureness] * accuracy))

    # Calculate movie popularity with review count and filter by obscureness
    review_count_df = df["film_id"].value_counts().reset_index()
    review_count_df.columns = ["film_id", "review_count"]
    review_count_df = review_count_df[review_count_df["review_count"] <= int(rating_threshold)]

    # Identify movies the user hasn't seen but are not too obscure
    unwatched_movies = list(set(review_count_df["film_id"]) - set(rated_movies))

    # Create the prediction set for all the user's unwatched obscure movies
    prediction_set = [(user_name, film_id, 0) for film_id in unwatched_movies]

    # Feed the prediction_set into the model. This returns a list of type
    # 'surprise.prediction_algorithms.predictions.Prediction' which is basically a dictionary
    # With types | user: <val> item: <movie_name> r_ui = <true_r> est = <> {'was_impossible': True/False}
    predictions = algo.test(prediction_set)

    # We then feed that pseudo dictionary into get_top_recs, which basically takes the values that we care
    # about, and sorts them to get the highest rated predictions, it then returns n highest rated predictions
    top_recs = get_top_recs(predictions, num_recs)

    # Define the returns object which is a list of dictionaries, the dictionary stores the film_id, the initial
    # predicted rating, and then the unclipped rating, which is explained below
    res = [{"film_id": x[0], "predicted_rating": x[1], "unclipped_rating": x[1]} for x in top_recs]

    """ Because we clip the rating in the range 1-10, to match the star ratings, if we have a rating that is 
        equal to 10, we need to repredict to see what the unclipped rating is for the given movie. For most 
        cases, the predicted_rating == unclipped_rating. """
    for i, prediction in enumerate(res):
        if prediction["predicted_rating"] == 10:
            res[i]["unclipped_rating"] = float(
                algo.predict(user_name, prediction["film_id"], clip=False).est
            )

    # Sort by unclipped rating in descending order
    res.sort(key=lambda x: (x["unclipped_rating"]), reverse=True)

    return res


# Sample use case
if __name__ == "__main__":
    # Define accuracy to something small, since this is a just a sample use case
    accuracy = 0.05

    # Call get_movie_dataframe to get all the user data and ratings to make recommendations.
    size_of_all_users_ratings = 1459852
    df = pd.read_csv(
        "./model/data/all_users_ratings.csv.gz",
        compression="gzip",
        nrows=int(size_of_all_users_ratings * accuracy),
    )

    # using sample data
    user_data = pd.read_csv("model/data/sample_user_data.csv")

    # build the collaborative based model and return
    algo, df = build_colab_model(df, user_data, "SVD")

    # Run the collaborative based model and return the recommendations
    recs = run_colab_model(algo, df, "nathannjohnson", accuracy, 20, 3)

    # Print the recommended items for the user
    for rec in recs:
        movie_name = rec.get("film_id")
        rating = rec.get("unclipped_rating")
        print(f"{movie_name} {round(rating, 2)}")
