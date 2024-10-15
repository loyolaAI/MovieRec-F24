import pandas as pd
import random

from build_colab_model import build_colab_model
from scraping import scrape_and_make_dataframe


def get_top_recs(predictions, num_recs):
    # top_n is a list of tuples that has the movie name and the predicted rating
    top_n = [(iid, est) for uid, iid, true_r, est, _ in predictions]
    # Sort top_n by the predicted rating, sorting from highest to lowest.
    top_n.sort(key=lambda x: (x[1], random.random()), reverse=True)
    # return the spliced list of the top_n recommendations
    return top_n[:num_recs]


def run_colab_model(algo, user_data, movies, accuracy, username, num_recs=25):
    """We need to get all the movies the user has not watched"""
    # Get a set of movie IDs that the user has already watched
    watched_movies = set(user_data["film_id"].unique())

    # Get a set of all movie IDs
    all_movies = set(movies["film_id"].unique())

    # Get the difference: movies the user hasn't watched
    unwatched_movies = list(all_movies - watched_movies)

    # Create the prediction set which will hold a given users film and the predicted rating for it.
    prediction_set = [(username, film_id, 0) for film_id in unwatched_movies]

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
                algo.predict(username, prediction["movie_id"], clip=False).est
            )

    # Sort the return array by the unclipped rating, and then return
    res.sort(key=lambda x: (x["unclipped_rating"]), reverse=True)

    return res


# Sample use case
if __name__ == "__main__":
    # Define accuracy to something small, since this is a just a sample use case
    accuracy = 0.05

    # Call get_movie_dataframe to get all the user data and ratings to make recommendations.
    from get_user_data import get_movie_dataframe

    df = get_movie_dataframe(accuracy)

    # using sample data
    user_data = pd.read_csv("./data/sample_user_data.csv")

    # build the collaborative based model and return
    algo = build_colab_model(df, user_data, accuracy)

    # Run the collaborative based model and return the recommendations
    recs = run_colab_model(algo, user_data, df, accuracy, "nathannjohnson", 20)

    # Print the recommended items for the user
    for rec in recs:
        movie_name = rec.get("film_id")
        rating = rec.get("unclipped_rating")
        print(f"{movie_name} {round(rating, 2)}")
