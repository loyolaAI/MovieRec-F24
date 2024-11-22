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
            col: None for col in movies.columns  # Ensure placeholder matches movies DataFrame structure
        }])
        placeholder["movie_title"] = movie_title  # Set the title
        placeholder["film_id"] = "placeholder-id"  # Add unique ID
        placeholder["combined_features"] = ""  # Default empty features
        movies = pd.concat([movies, placeholder], ignore_index=True)
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

def get_movie_recommendations(movie_title, file_path="model/data/movies.csv", top_n=5):
    # Load the dataset
    movies = load_data(file_path)

    # Preprocess the data
    movies = preprocess_data(movies)

    # Ensure the input movie is in the dataset
    movies = ensure_movie_in_dataset(movie_title, movies)

    # Create the TF-IDF matrix
    tfidf, tfidf_matrix = create_tfidf_matrix(movies)

    # Get recommendations for a specific movie
    try:
        recommendations = get_recommendations(movie_title, movies, tfidf_matrix, top_n=top_n)
        return recommendations
    except ValueError as e:
        return str(e)
    
movie_title = "Aha"
recommendations = get_movie_recommendations(movie_title)
print(f"Top 5 recommendations for '{movie_title}':")
for film_id in recommendations:
    print(film_id)