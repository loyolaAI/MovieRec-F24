import pandas as pd


def get_movie_info(user_data: pd.DataFrame) -> pd.DataFrame:
    """
    Currently when we scrap someones letterboxd, we only get the movie name and rating.
    we also need to add the genre and other info for content based filtering. So that's
    what this method needs to do. You should be able to take the Movie_name_slug from the
    dataframe and search for the same title within the films.csv.gz and then get the technical
    name, instead of just the slug.
    """
    print("hello from get_movie_info")


def get_unwatched_movies(user_data: pd.DataFrame, movies: pd.DataFrame, accuracy: float) -> list:
    """
    To actually recommend movies. we take all of the movies the user has not watched
    and put them into model that we built with the movies they have not watched. This method
    should be as simple as taking the .csv file with all the movies and getting only movies
    the user has not seen.
    """


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
