import pandas as pd


def get_movie_info(user_data: pd.DataFrame) -> pd.DataFrame:
    """
    Currently when we scrap someones letterboxd, we only get the movie name and rating.
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


def get_unwatched_movies(user_data: pd.DataFrame, movies: pd.DataFrame, accuracy: float) -> list:
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


def get_movie_dataframe(accuracy: float) -> pd.DataFrame:
    # Total length of all the ratings data, combined
    total_len = 18175545

    # Calculate the total number of rows needed
    total_needed_rows = int(total_len * accuracy)

    # List of CSV file paths
    zipped_csv_files = [
        "./data/ratings/ratings1.csv.gz",
        "./data/ratings/ratings2.csv.gz",
        "./data/ratings/ratings3.csv.gz",
        "./data/ratings/ratings4.csv.gz",
    ]

    # DataFrames list to store each chunk
    dfs = []

    # Track how many rows have been read so far
    rows_read = 0

    # Loop through the CSV files
    for file in zipped_csv_files:
        # Figure out how many rows we need to read
        rows_to_read = total_needed_rows - rows_read

        # If there are still rows to read
        if rows_to_read > 0:
            # Read the csv, this works because of rows_to_read > len(csv) it
            # stops reading, instead of throwing an error
            chunk = pd.read_csv(file, compression="gzip", nrows=rows_to_read)
            # Increment the counter with the number of rows read
            rows_read += len(chunk)

            # Append the chunk to the DataFrame list
            dfs.append(chunk)

        # Break if we've read enough rows
        if rows_read >= total_needed_rows:
            break

    # Concatenate all the chunks into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df

if __name__ == "__main__":
    user_data = pd.read_csv('./data/sample_user_data.csv')
    movie_info = get_movie_info(user_data)
    print(movie_info["genres"])
    print(movie_info.head())
