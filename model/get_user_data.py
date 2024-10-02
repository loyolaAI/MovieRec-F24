import pandas as pd

def get_movie_info(user_data : pd.DataFrame) -> pd.DataFrame:
    """
    Currently when we scrap someones letterboxd, we only get the movie name and rating.
    we also need to add the genre and other info for content based filtering. So that's
    what this method needs to do. You should be able to take the Movie_name_slug from the 
    dataframe and search for the same title within the films.csv.gz and then get the technical
    name, instead of just the slug. 
    """


def get_unwatched_movies(user_data) -> list:
    """
    To actually recommend movies. we take all of the movies the user has not watched
    and put them into model that we built with the movies they have not watched. This method
    should be as simple as taking the .csv file with all the movies and getting only movies
    the user has not seen.
    """