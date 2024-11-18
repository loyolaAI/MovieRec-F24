import pandas as pd


def get_movie_info(user_data: pd.DataFrame) -> pd.DataFrame:
    """
    Currently when we scrape someones letterboxd, we only get the movie name and rating.
    we also need to add the genre and other info for content based filtering. So that's
    what this method needs to do. You should be able to take the Movie_name_slug from the
    dataframe and search for the same title within the films.csv.gz and then get the technical
    name, instead of just the slug.
    """
    print("hello from get_movie_info")


def get_unwatched_movies(user_data: pd.DataFrame, movies: pd.DataFrame) -> list:
    """
    To actually recommend movies. we take all of the movies the user has not watched
    and put them into model that we built with the movies they have not watched. This method
    should be as simple as taking the .csv file with all the movies and getting only movies
    the user has not seen.
    """
    # get all movies have watched
    watched_movies = user_data['film_id'].tolist()

    # Filter out movies that have already been watched
    unwatched_movies = movies[~movies['film_id'].isin(watched_movies)]
    
    # Return the list
    return unwatched_movies['film_id'].tolist()

if __name__ == "__main__":
    movies = pd.read_csv("./data/all_users_ratings.csv.gz", compression="gzip")
    user_data = pd.read_csv("./data/sample_user_data.csv")
    unwatched_movies = get_unwatched_movies(user_data, movies)
    print(unwatched_movies[:50])
    
