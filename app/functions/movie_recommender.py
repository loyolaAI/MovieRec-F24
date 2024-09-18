import joblib

# Recommendation Model
model = joblib.load("model.pkl")


def movie_recommendation(data):  # Adjust
    return model.recommend([data])

