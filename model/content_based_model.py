import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psutil


def has_enough_ram(required_ram_gb):
    """
    Checks if the system has enough RAM.

    Args:
      required_ram_gb: The required RAM in gigabytes.

    Returns:
      True if the system has enough RAM, False otherwise.
    """

    # Get the total physical memory in bytes.
    total_ram = psutil.virtual_memory().total
    # Convert bytes to gigabytes.
    total_ram_gb = total_ram / (1024**3)

    return total_ram_gb >= required_ram_gb


def load_data(file_path="./model/data/movies.csv.gz"):
    """
    Load the dataset from a CSV file.
    """
    if file_path.split(".")[-1] == ".gz":
        movies = pd.read_csv(file_path, compression="gzip")
    else:
        movies = pd.read_csv(file_path)
    return movies


def preprocess_data(movies: pd.DataFrame):
    """
    Combine genres, director, actors, and writes into a single feature for each movie.
    """
    # Removing the bars ("|") and whitespaces
    movies["Genres"] = movies["Genres"].astype(str).apply(lambda x: " ".join(x.split("|")).strip())
    movies["Stars"] = movies["Stars"].astype(str).apply(lambda x: " ".join(x.split("|")).strip())
    movies["Writers"] = (
        movies["Writers"].astype(str).apply(lambda x: " ".join(x.split("|")).strip())
    )
    movies["Directors"] = (
        movies["Directors"].astype(str).apply(lambda x: " ".join(x.split("|")).strip())
    )
    # Create the combined column
    movies["combined_features"] = (
        movies["Genres"]
        + " "
        + movies["Directors"]
        + " "
        + movies["Stars"]
        + " "
        + movies["Writers"]
    )
    # Drop unncessesary columns
    movies = movies.drop(columns=["Genres", "Directors", "Stars", "Writers"])
    # Avoids errors like "numpy._core._exceptions._ArrayMemoryError: Unable to allocate 53.6 GiB for an array with shape (7197683643,) and data type int64"
    if not has_enough_ram(54):
        rows = 20000
        print(
            "System does not have enough RAM allocated to process the full dataset. Falling back to a small portion of the dataset with "
            + str(rows)
            + "/{0:2d} items that takes ~5 GB".format(len(movies))
        )
        movies = movies.iloc[:rows]
    return movies


def create_tfidf_matrix(movies):
    """
    Create the TF-IDF matrix from the combined movie features.
    """
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["combined_features"])
    return tfidf, tfidf_matrix


def compute_cosine_similarity(tfidf_matrix):
    """
    Compute cosine similarity between movies based on the TF-IDF matrix.
    """
    # For RAM errors, try to send only a snippet of the full movies data. The final version will use all of the data on a more beefy computer
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_recommendations(title, movies, cosine_sim):
    """
    Get the top 5 movie recommendations based on the title.
    """
    idx = movies[movies["Title"] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Skip the first one (self match)
    movie_indices = [i[0] for i in sim_scores]
    return movies["Title"].iloc[movie_indices]


# The methods below were written by chatGPT and will be used for a later implementation
"""
def get_movies_user_likes(user : pd.DataFrame):



def get_recommendations_for_user(user_movies, movies, cosine_sim, top_n=5):
    Get movie recommendations based on multiple movies the user liked.
    
    :param user_movies: List of movie titles the user likes.
    :param movies: The movie DataFrame.
    :param cosine_sim: Cosine similarity matrix.
    :param top_n: Number of recommendations to return.
    :return: Top N recommended movies.

    # Get indices for all movies the user liked
    movie_indices = [movies[movies['title'] == movie].index[0] for movie in user_movies]
    
    # Sum cosine similarities for each movie in user's list
    sim_scores = np.zeros(cosine_sim.shape[0])
    for idx in movie_indices:
        sim_scores += cosine_sim[idx]
    
    # Sort movies based on the combined similarity scores
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Exclude movies already seen by the user
    sim_scores = [score for score in sim_scores if movies.iloc[score[0]]['title'] not in user_movies]
    
    # Get the top N movie recommendations
    sim_scores = sim_scores[:top_n]
    movie_indices = [i[0] for i in sim_scores]
    
    return movies['title'].iloc[movie_indices]
"""


# Main workflow
if __name__ == "__main__":
    # Load the data
    movie_data_file = "./model/data/movies.csv.gz"  # Path to your dataset
    movies = load_data(movie_data_file)

    # Preprocess the data
    movies = preprocess_data(movies)

    # Create TF-IDF matrix
    tfidf, tfidf_matrix = create_tfidf_matrix(movies)

    # Compute cosine similarity
    cosine_sim = compute_cosine_similarity(tfidf_matrix)

    # Get recommendations for a sample movie
    movie_title = "Akira"  # Change this to any movie in your dataset
    recommendations = get_recommendations(movie_title, movies, cosine_sim)

    # Print recommendations
    print(f"Top recommendations for '{movie_title}':")
    for movie in recommendations:
        print(movie)
