# Mission Statement

The goal of the **Movie Recommendation System** project is to provide personalized movie recommendations to users based on their preferences and the content of movies through a given users letterboxd account. By leveraging machine learning techniques such as collaborative filtering, and content-based filtering, this system aims to deliver accurate and relevant recommendations that enhance the user's movie-watching experience, by giving them unexpected movies that they would not typically be recommended or find without our model.

This project has two main forms of recommendations that are exposed on a hosted front-end through Heroku. This front-end allows for a user to create an account and input there letterboxd. We then scrape the letterboxd movies from the users letterboxd and store them within the database. The first model we use to recommend in a collaborative based model using other user data. We have 1.5 million rows of data with around 5000 users movie ratings. We use this dataset to recommend other movies for the given user using a singular value decomposition matrix vectorization method to make relationships between a given user and all the users within the dataset. The second model is a content-based model that uses datasets containing movie information, such as genres, ratings, and metadata, and applies a  TF-IDF vectorization and cosine similarity algorithms to suggest movies. We aim to improve the user experience with an intuitive and efficient recommendation system that helps users discover movies aligned with their interests.

### Key Objectives:
- Build a scalable recommendation system that processes large movie datasets.
- Provide correct recommendations no matter the use case
- Provide a stable website that can be used anywhere and anytime
- Use machine learning and natural language processing to match users with movies.
- Continuously improve the recommendation accuracy based on user feedback and data.

