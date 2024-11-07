import pandas as pd

# Comment below 3 to use method locally
from model.build_colab_model import build_colab_model
from model.run_colab_model import run_colab_model
from model.scraping import scrape_and_make_dataframe

# Uncomment below 3 to use method locally
# from build_colab_model import build_colab_model
# from run_colab_model import run_colab_model
# from scraping import scrape_and_make_dataframe


def main():
    # Get the accuracy to see how much data we want to use for the model and recommendations.
    accuracy = float(input("How accurate do you want the model to be (range 0.01-1.0) "))

    # Call get_movie_dataframe to get all the user data and ratings to make recommendations.
    size_of_all_users_ratings = 1459852
    df = pd.read_csv(
        "./model/data/all_users_ratings.csv.gz",
        compression="gzip",
        nrows=int(size_of_all_users_ratings * accuracy),
    )

    # Get the users, letterbox'd username, to scrape ratings.
    username = input("What is your letterboxd username ")
    user_data = scrape_and_make_dataframe(username)

    # Ask the user for how many movies recommendations they want
    number_recs = int(input("How many recommendations do you want "))

    model_type = input("What type of model do you want to run, either 'SVD' or 'BaseLine' ")

    # build the collaborative based model and return
    algo, df = build_colab_model(df, user_data, model_type)

    obscureness = int(
        input("How 'obscure' do you want the recommendations to be (0-9) 0 being obscure ")
    )

    # Run the collaborative based model and return the recommendations
    recs = run_colab_model(algo, df, username, accuracy, number_recs, obscureness)

    # Print the recommended items for the user
    for rec in recs:
        movie_name = rec.get("film_id")
        rating = rec.get("unclipped_rating")
        print(f"{movie_name} {round(rating, 2)}")


def get_recommendations(
    username, accuracy=0.01, number_recs=20, obscureness=9, model_type="BaseLine"
):
    # Load in the movie ratings data to get all the user data and ratings to make recommendations.
    size_of_all_users_ratings = 1459852
    df = pd.read_csv(
        "./model/data/all_users_ratings.csv.gz",
        compression="gzip",
        nrows=int(size_of_all_users_ratings * accuracy),
    )
    print(f"Movie DataFrame:\n{df.head()}")  # Check the DataFrame

    # Scrape user data from Letterboxd
    user_data = scrape_and_make_dataframe(username)
    print(f"User Data:\n{user_data}")  # Check the user data

    # Build the collaborative model
    algo, df = build_colab_model(df, user_data, model_type)
    print("Collaborative model built successfully.")

    # Run the collaborative model and return recommendations
    recs = run_colab_model(algo, df, username, accuracy, number_recs, obscureness)
    print(f"Recommendations:\n{recs}")  # Check the recommendations

    return recs


def time_model(
    accuracy,
    number_recs,
    obscureness,
    model_type: str,
    number_of_runs: int = 10,
    print_recs: bool = False,
):
    import time

    # List that will store all the times for the model
    timers = []
    for i in range(number_of_runs):
        # Start the timer
        start_time = time.time()

        # Load the CSV with all the movies data into a DF.
        size_of_all_users_ratings = 1459852
        df = pd.read_csv(
            "./model/data/all_users_ratings.csv.gz",
            compression="gzip",
            nrows=int(size_of_all_users_ratings * accuracy),
        )

        # Get the sample user data
        user_data = pd.read_csv("./model/data/sample_user_data.csv")

        # build the collaborative based model and the updated movies dataframe that now has user data.
        algo, df = build_colab_model(df, user_data, model_type)

        # Run the collaborative based model and return the recommendations
        recs = run_colab_model(algo, df, "nathannjohnson", accuracy, number_recs, obscureness)

        # Print the recommended items for the user if told
        if print_recs:
            for rec in recs:
                movie_name = rec.get("film_id")
                rating = rec.get("unclipped_rating")
                print(f"{movie_name} {round(rating, 2)}")

        # Get the total time and report.
        tot_time = time.time() - start_time
        print(f"Run {i+1} | time = {tot_time}")
        # Add time to the list
        timers.append(tot_time)
        # Delete the old variables from each run.
        del algo, df, recs
    print(f"Average time for code = {sum(timers)/len(timers)}")


if __name__ == "__main__":
    main()
    # time_model(accuracy=0.5,
    #            number_recs=20,
    #            obscureness=9,
    #            model_type="baseline",
    #            number_of_runs=1,
    #            print_recs=True
    #            )
