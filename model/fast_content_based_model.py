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
    movies["genres"] = movies["genres"].fillna("").str.replace(r'[\[\]"|,]', " ", regex=True)
    movies["combined_features"] = movies["genres"]  # Expand this as needed
    movies["movie_title"] = movies["movie_title"].fillna("Unknown Title").str.strip().str.lower()
    return movies

def create_tfidf_matrix(movies):
    """
    Create the TF-IDF matrix from the combined movie features.
    """
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)  # Limit to 5000 features for efficiency
    tfidf_matrix = tfidf.fit_transform(movies["combined_features"])
    return tfidf, tfidf_matrix

def get_recommendations(title, movies, tfidf_matrix, top_n=5):
    """
    Get top N movie recommendations based on the cosine similarity of the TF-IDF matrix.
    """
    # Normalize input title and dataset titles
    movies["movie_title"] = movies["movie_title"].str.strip().str.lower()
    title = title.strip().lower()

    # Check if the movie exists in the dataset
    if title not in movies["movie_title"].values:
        raise ValueError(f"Movie '{title}' not found in the dataset.")
    
    # Get the index of the movie
    idx = movies.index[movies["movie_title"] == title].tolist()[0]

    # Compute cosine similarity
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()

    # Get top N most similar movies (excluding the movie itself)
    related_docs_indices = cosine_similarities.argsort()[:-top_n-2:-1]
    recommendations = movies.iloc[related_docs_indices]["movie_title"]

    return recommendations


if __name__ == "__main__":
    # Load the dataset
    movies = load_data(file_path)

    # Preprocess the data
    movies = preprocess_data(movies)

    # Subsample for faster development (remove or increase limit for production)
    # movies = movies.sample(10000, random_state=42)

    # Create the TF-IDF matrix
    tfidf, tfidf_matrix = create_tfidf_matrix(movies)

    # Get recommendations for a specific movie
    movie_title = "Akira"  # Change this to test other titles
    try:
        recommendations = get_recommendations(movie_title, movies, tfidf_matrix, top_n=5)
        print(f"Top recommendations for '{movie_title}':")
        for movie in recommendations:
            print(movie)
    except ValueError as e:
        print(e)
