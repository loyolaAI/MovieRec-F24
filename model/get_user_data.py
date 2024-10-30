import os
import pandas as pd

# Get the absolute path to the 'ratings' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RATINGS_DIR = os.path.join(BASE_DIR, "../model/data/ratings")


def get_movie_info(user_data: pd.DataFrame) -> pd.DataFrame:
    """
    When scraping someone's Letterboxd, we only get the movie name and rating.
    This method enriches that data by adding genre and other info for content-based filtering.
    It searches for the movie title in films.csv.gz to get the technical name instead of just the slug.
    """
    print("hello from get_movie_info")


def get_unwatched_movies(
    user_data: pd.DataFrame, movies: pd.DataFrame, accuracy: float
) -> list:
    """
    Recommends movies by taking all unwatched movies and putting them into a model.
    This function extracts movies the user hasn't seen from the CSV.
    """


def get_movie_dataframe(accuracy: float) -> pd.DataFrame:
    total_len = 18175545  # Total length of all the ratings data combined
    total_needed_rows = int(total_len * accuracy)  # Calculate needed rows

    # List of absolute paths to the ratings files
    zipped_csv_files = [
        os.path.join(RATINGS_DIR, f"ratings{i}.csv.gz") for i in range(1, 5)
    ]

    dfs = []  # Store each chunk of data
    rows_read = 0  # Track how many rows have been read

    # Read the CSV files in chunks
    for file in zipped_csv_files:
        rows_to_read = total_needed_rows - rows_read  # Rows still needed
        if rows_to_read > 0:
            chunk = pd.read_csv(file, compression="gzip", nrows=rows_to_read)
            rows_read += len(chunk)
            dfs.append(chunk)
        if rows_read >= total_needed_rows:
            break

    # Concatenate all chunks into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df
