import joblib

# Recommendation Model
model = joblib.load("model.pkl")


def movie_recommendation(data):
    return model.recommend([data])
