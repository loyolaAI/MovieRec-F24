import joblib

# Recommendation Model
model = joblib.load('model.pkl')

def make_prediction(data):
    return model.predict([data])