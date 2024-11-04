from model.get_user_data import get_movie_dataframe  # Comment below 4 to use method locally
from model.build_colab_model import build_colab_model
from model.run_colab_model import run_colab_model
from model.scraping import scrape_and_make_dataframe

# from get_user_data import get_movie_dataframe # Uncomment below 4 to use method locally
# from build_colab_model import build_colab_model
# from run_colab_model import run_colab_model
# from scraping import scrape_and_make_dataframe


def main():
    # Get the accuracy to see how much data we want to use for the model and recommendations.
    accuracy = float(input("How accurate do you want the model to be (range 0.01-1.0) "))

    # Call get_movie_dataframe to get all the user data and ratings to make recommendations.
    df = get_movie_dataframe(accuracy)

    # Get the users, letterbox'd username, to scrape ratings.
    username = input("What is your letterboxd username ")
    user_data = scrape_and_make_dataframe(username)

    # Ask the user for how many movies recommendations they want
    number_recs = int(input("How many recommendations do you want "))

    # build the collaborative based model and return
    algo = build_colab_model(df, user_data, accuracy)

    obscureness = int(
        input("How 'obscure' do you want the recommendations to be (0-9) 0 being obscure ")
    )

    # Run the collaborative based model and return the recommendations
    recs = run_colab_model(algo, user_data, df, accuracy, username, number_recs, obscureness)

    # Print the recommended items for the user
    for rec in recs:
        movie_name = rec.get("film_id")
        rating = rec.get("unclipped_rating")
        print(f"{movie_name} {round(rating, 2)}")


def get_recommendations(username, accuracy=0.01, number_recs=20, obscureness=9):
    # Call get_movie_dataframe to get all the user data and ratings to make recommendations.
    df = get_movie_dataframe(accuracy)
    print(f"Movie DataFrame:\n{df.head()}")  # Check the DataFrame

    # Scrape user data from Letterboxd
    user_data = scrape_and_make_dataframe(username)
    print(f"User Data:\n{user_data}")  # Check the user data

    # Build the collaborative model
    algo = build_colab_model(df, user_data, accuracy)
    print("Collaborative model built successfully.")

    # Run the collaborative model and return recommendations
    recs = run_colab_model(algo, user_data, df, accuracy, username, number_recs, obscureness)
    print(f"Recommendations:\n{recs}")  # Check the recommendations

    return recs


if __name__ == "__main__":
    main()
