import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os

# File path
file_path = "model/data/movies.csv.gz"


def load_data(file_path):
    """
    Load the dataset from a CSV file.
    """
    movies = pd.read_csv(file_path, compression="gzip")
    return movies


def preprocess_data(movies):
    """
    Preprocess the data by combining relevant columns into a single feature for TF-IDF analysis.
    """
    # Clean and process genres
    movies["genres"] = movies["genres"].fillna("").str.replace(r'[\[\]"|,]', " ", regex=True)

    # Clean and process spoken languages
    movies["spoken_languages"] = (
        movies["spoken_languages"].fillna("").str.replace(r'[\[\]"|,]', " ", regex=True)
    )

    # Clean and process production countries
    movies["production_countries"] = (
        movies["production_countries"].fillna("").str.replace(r'[\[\]"|,]', " ", regex=True)
    )

    # Fill missing original language
    movies["original_language"] = movies["original_language"].fillna("")

    # Combine genres, spoken languages, production countries, and original language into a single feature
    movies["combined_features"] = (
        movies["genres"]
        + " "
        + movies["spoken_languages"]
        + " "
        + movies["production_countries"]
        + " "
        + movies["original_language"]
    )

    # Ensure all movies have unique titles (optional but useful)
    movies["movie_title"] = movies["movie_title"].fillna("Unknown Title")

    return movies


def create_tfidf_matrix(movies):
    """
    Create the TF-IDF matrix from the combined movie features.
    """
    tfidf = TfidfVectorizer(
        stop_words="english", max_features=50000
    )  # Limit to 5000 features for efficiency
    tfidf_matrix = tfidf.fit_transform(movies["combined_features"])
    return tfidf, tfidf_matrix


def ensure_movie_in_dataset(movie_title, movies):
    """
    Ensure the input movie is present in the dataset.
    If not found, add a placeholder entry to the dataset.
    """
    if movie_title not in movies["movie_title"].values:
        print(f"'{movie_title}' not found in dataset. Adding placeholder entry.")
        placeholder = pd.DataFrame(
            [
                {
                    col: None
                    for col in movies.columns  # Ensure placeholder matches movies DataFrame structure
                }
            ]
        )
        placeholder["movie_title"] = movie_title  # Set the title
        placeholder["film_id"] = "placeholder-id"  # Add unique ID
        placeholder["combined_features"] = ""  # Default empty features
        movies = pd.concat([movies, placeholder], ignore_index=True)
    return movies


def get_recommendations(title, movies, tfidf_matrix, top_n=10):
    """
    Get recommendations by computing cosine similarity on demand.

    Parameters:
    title (str): The movie title for which to get recommendations.
    movies (DataFrame): The preprocessed movie DataFrame.
    tfidf_matrix (sparse matrix): The TF-IDF matrix.
    top_n (int): The number of recommendations to return.

    Returns:
    list: Recommended movies as a list of dictionaries.
    """
    try:
        idx = movies[movies["movie_title"] == title].index[0]
    except IndexError:
        raise ValueError(f"Movie '{title}' not found in the dataset.")

    # Compute cosine similarity for the given movie
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()

    # Get top N recommendations (excluding the movie itself)
    sim_scores = cosine_similarities.argsort()[: -top_n - 2 : -1]
    recommendations = movies.iloc[sim_scores][["film_id", "movie_title"]]

    return recommendations.to_dict(orient="records")


def make_and_save_model(model_save_path="model/models/tfidf_model.pkl"):
    """
    Save the TF-IDF model to a file and compute similarities on demand.
    """
    # Load the dataset
    movies = load_data("model/data/movies.csv.gz")

    # Preprocess the data
    movies = preprocess_data(movies)

    # Create the TF-IDF matrix
    _, tfidf_matrix = create_tfidf_matrix(movies)

    # Save only the TF-IDF vectorizer and matrix
    with open(model_save_path, "wb") as f:
        pickle.dump({"tfidf_matrix": tfidf_matrix}, f)

    print(f"TF-IDF model saved successfully to {model_save_path}")


def get_movie_recommendations(
    movie_title,
    file_path="model/data/movies.csv.gz",
    model_path="model/models/tfidf_model.pkl",
    top_n=5,
):
    """
    Get movie recommendations based on the TF-IDF model.
    If the model exists, load it; otherwise, create it from scratch.

    Parameters:
    movie_title (str): The title of the movie to get recommendations for.
    file_path (str): Path to the dataset file.
    model_path (str): Path to the saved TF-IDF model.
    top_n (int): Number of recommendations to return.

    Returns:
    list or str: A list of recommended movies or an error message.
    """
    # Load the dataset
    movies = load_data(file_path)

    # Preprocess the data
    movies = preprocess_data(movies)

    # Ensure the input movie is in the dataset
    movies = ensure_movie_in_dataset(movie_title, movies)

    # Try to load the saved TF-IDF model and matrix
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            data = pickle.load(f)
            tfidf_matrix = data["tfidf_matrix"]
    else:
        _, tfidf_matrix = create_tfidf_matrix(movies)

    # Get recommendations for the movie
    try:
        recommendations = get_recommendations(movie_title, movies, tfidf_matrix, top_n=top_n)
        return recommendations
    except ValueError as e:
        return str(e)


if __name__ == "__main__":
    # Sample use case
    import time

    start_time = time.time()
    movie_title = "Parasite"
    recommendations = get_movie_recommendations(movie_title)
    print(f"Top 5 recommendations for '{movie_title}':")
    for film_id in recommendations:
        print(film_id)
    # Uncomment if you want to make and save a new tfidf matrix
    # make_and_save_model()
