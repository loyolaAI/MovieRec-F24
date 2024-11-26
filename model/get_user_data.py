import pandas as pd


def get_movie_info(user_data: pd.DataFrame) -> pd.DataFrame:
    """
    Currently when we scrape someones letterboxd, we only get the movie name and rating.
    we also need to add the genre and other info for content based filtering. So that's
    what this method needs to do. You should be able to take the Movie_name_slug from the
    dataframe and search for the same title within the films.csv.gz and then get the technical
    name, instead of just the slug.
    """
    # load the film metadata 
    movies_df = pd.read_csv("./data/movies.csv")

    # merge with user data based on the 'movie_name_slug column'
    #movie_info = pd.merge(user_data, movies_df, left_on="film_id", right_on="film_id", how="left")
    movie_info = pd.merge(user_data, movies_df[['film_id', 'movie_title', 'genres', 'rating_count', 'original_language', 'year_released']], on="film_id", how="left")

    movie_info['film_id'] = movie_info['film_id'].fillna('0')
    movie_info['rating_count'] = movie_info['rating_count'].fillna('Unknown')
    movie_info['genres'] = movie_info['genres'].fillna('Unknown')
    movie_info['movie_title'] = movie_info['movie_title'].fillna('Unknown')
    movie_info['original_language'] = movie_info['original_language'].fillna('Unknown')
    movie_info['year_released'] = movie_info['year_released'].fillna('Unknown')

    return movie_info


def get_unwatched_movies(user_data: pd.DataFrame, movies: pd.DataFrame) -> list:
    """
    To actually recommend movies. we take all of the movies the user has not watched
    and put them into model that we built with the movies they have not watched. This method
    should be as simple as taking the .csv file with all the movies and getting only movies
    the user has not seen.
    """
    # get all movies have watched
    watched_movies = user_data["film_id"].tolist()

    # Filter out movies that have already been watched
    unwatched_movies = movies[~movies["film_id"].isin(watched_movies)]

    # Return the list
    return unwatched_movies["film_id"].tolist()


if __name__ == "__main__":
    # Sample use case for unwatched_movies
    movies = pd.read_csv("./data/all_users_ratings.csv.gz", compression="gzip")
    user_data = pd.read_csv("./data/sample_user_data.csv")
    unwatched_movies = get_unwatched_movies(user_data, movies)
    print(unwatched_movies[:50])
    print()

    # Sample use case for get_movie_info
    user_data = get_movie_info(user_data)
    print(user_data)
