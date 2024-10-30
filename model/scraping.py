## Scraping for Letterboxd using BeautifulSoup and requests

# imports used
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Method to scrape a given users letterboxd profile and get information about the users movies and ratings
def scrap_letterboxd(username: str):
    # Given the username, create the letterboxd url so we can scrap the movies
    url = "https://letterboxd.com/" + username.strip() + "/films/by/rated-date-earliest/page/1"

    # Initialize the regular expressions which will scan the soup file
    # for all of the movie names and star ratings.
    regex_movie_names = re.compile(r'data-film-slug="([^"]+)"')
    regex_movie_ratings = re.compile(r"rated-(\d+)")

    # Make the soup to pull everything off the users letterboxd webpage.
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    # Now find everything from only the actual movie section of the webpage, not the other info
    film_html = soup.find_all("li", class_=re.compile(r"poster-container"))

    # Now, using regex, we get all the movie names and ratings from the HTML file.
    # This automatically creates a list for each variable.
    movie_names = re.findall(regex_movie_names, str(film_html))
    movie_ratings = re.findall(regex_movie_ratings, str(film_html))

    """ Now we're going to remove the movies from the users letterbox'd that don't
        have a rating associated with them. Because it won't add to the model and
        it will break when we try and create a dataframe.   """
    # We now get the url for the movies that don't have any reviews.
    url_no_reviews = "https://letterboxd.com/" + username.strip() + "/films/rated/none/"

    # Make the soup to pull everything off that webpage.
    soup = BeautifulSoup(requests.get(url_no_reviews).text, "html.parser")

    # Now scrap everything from only the reviews section. that is the 'list__...'
    film_html_no_reviews = soup.find_all("li", class_=re.compile(r"poster-container"))

    # Get the list of all the removed movies.
    removed_movie_names = re.findall(r'data-film-slug="([^"]+)"', str(film_html_no_reviews))

    """ Loop over all the movies we found, and remove them so that
    len(movie_names) == len(movie_ratings) and we don't have movies without ratings
    If the movie exists within the lists we should remove it
    We wont need this when we scrape all the movies instead of
    only the first page. """
    movie_names = [movie for movie in movie_names if movie not in removed_movie_names]

    # Return the results
    return movie_names, movie_ratings


# Method to scrape a given letterboxd username and return a dataframe with the movie names and the star ratings.
def scrape_and_make_dataframe(username: str) -> pd.DataFrame:
    # Scrap the movies and ratings from the given letterboxd username
    (movie_name, movie_rating) = scrap_letterboxd(username)

    # Convert the ratings from string to integer using list comprehension
    int_movie_ratings = [int(i.split()[0]) for i in movie_rating]

    # Make a list of size (movie_name) for the usernames, Not necessary just included it
    username_list = [username] * len(movie_name)

    # Return the results as a Pandas dataframe
    return pd.DataFrame(
        {"user_name": username_list, "film_id": movie_name, "rating": int_movie_ratings}
    )


if __name__ == "__main__":
    # Sample use
    username = input("Please type your letterboxd username : ")
    print(f"Now scraping : {username}")
    df = scrape_and_make_dataframe(username.strip())
    print(df)
