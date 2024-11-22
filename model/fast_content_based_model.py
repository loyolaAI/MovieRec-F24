import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# File path
file_path = "model/data/movies.csv"

def load_data(file_path):
    """
    Load the dataset from a CSV file.
    """
    movies = pd.read_csv(file_path)
    return movies

def preprocess_data(movies):
    """
    Preprocess the data by combining relevant columns into a single feature for TF-IDF analysis.
    """
    # Clean and process genres
    movies["genres"] = movies["genres"].fillna("").str.replace(r'[\[\]"|,]', " ", regex=True)
    
    # Combine genres and other features into a single feature
    movies["combined_features"] = movies["genres"]  # Expand this as needed
    
    # Ensure all movies have unique titles (optional but useful)
    movies["movie_title"] = movies["movie_title"].fillna("Unknown Title")
    
    return movies

def create_tfidf_matrix(movies):
    """
    Create the TF-IDF matrix from the combined movie features.
    """
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)  # Limit to 5000 features for efficiency
    tfidf_matrix = tfidf.fit_transform(movies["combined_features"])
    return tfidf, tfidf_matrix

def ensure_movie_in_dataset(movie_title, movies):
    """
    Ensure the input movie is present in the dataset.
    If not found, add a placeholder entry to the dataset.
    """
    if movie_title not in movies["movie_title"].values:
        print(f"'{movie_title}' not found in dataset. Adding placeholder entry.")
        placeholder = pd.DataFrame([{
            "film_id": "placeholder-id",
            "rating_count": 0,
            "genres": "",
            "imdb_link": "",
            "movie_title": movie_title,
            "original_language": "unknown",
            "year_released": None,
            "combined_features": ""
        }])  # Convert to DataFrame
        movies = pd.concat([movies, placeholder], ignore_index=True)  # Concatenate as DataFrame
    return movies

def get_recommendations(title, movies, tfidf_matrix, top_n=5):
    """
    Get top N movie recommendations based on the cosine similarity of the TF-IDF matrix.
    """
    try:
        idx = movies.index[movies["movie_title"] == title][0]
    except IndexError:
        raise ValueError(f"Movie '{title}' not found in the dataset.")
    
    # Compute cosine similarity for the target movie
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    
    # Get top N most similar movies (excluding the movie itself)
    related_docs_indices = cosine_similarities.argsort()[:-top_n-2:-1]  # Skip the self-match
    recommendations = movies.iloc[related_docs_indices]["film_id"]
    
    return recommendations

if __name__ == "__main__":
    # Load the dataset
    movies = load_data(file_path)

    # Preprocess the data
    movies = preprocess_data(movies)

    # Ensure the input movie is in the dataset
    movie_title = "Aha"  # Change this to test other titles
    movies = ensure_movie_in_dataset(movie_title, movies)

    # Subsample for faster development (remove or increase limit for production)
    # movies = movies.sample(10000, random_state=42)

    # Create the TF-IDF matrix
    tfidf, tfidf_matrix = create_tfidf_matrix(movies)

    # Get recommendations for a specific movie
    try:
        recommendations = get_recommendations(movie_title, movies, tfidf_matrix, top_n=5)
        print(f"Top recommendations for '{movie_title}' (film_id):")
        for film_id in recommendations:
            print(film_id)
    except ValueError as e:
        print(e)
