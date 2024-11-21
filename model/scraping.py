## Scraping for Letterboxd using BeautifulSoup and requests

# imports used
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def scrape_letterboxd(username: str) -> dict:
    # Define the return dictionary
    user_data_dict = {"names": [], "slugs": [], "ratings": [], "images": []}
    # Define the regex patterns for name, slug, and rating which will
    # look for there respective Strings to collect.
    regex_patterns = {
        "name": re.compile(r'alt="([^"]+)"'),
        "slug": re.compile(r'data-film-slug="([^"]+)"'),
        "rating": re.compile(r"rated-(\d+)"),
    }

    page_number = 1
    # Scrape movies with ratings
    while True:
        url = f"https://letterboxd.com/{username.strip()}/films/page/{page_number}/"
        # Make the soup object
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        # Take the section from the soup that has the actual movies
        film_html = soup.find_all("li", class_=re.compile(r"poster-container"))

        # Break if no films are found on the page
        if not film_html:
            break

        # Extract data using regex on the HTML snippet for names, slugs, and ratings
        page_names = regex_patterns["name"].findall(str(film_html))
        page_slugs = regex_patterns["slug"].findall(str(film_html))
        page_ratings = [int(r) for r in regex_patterns["rating"].findall(str(film_html))]

        # Add data from the page to the main list
        user_data_dict["names"].extend(page_names)
        user_data_dict["slugs"].extend(page_slugs)
        user_data_dict["ratings"].extend(page_ratings)
        # Move onto the next page
        page_number += 1

    # Scrape movies without ratings to exclude from results, We need this because it will offset
    # the ratings column and then we won't know if the movie[i] actually equals rating[i]
    url_no_reviews = f"https://letterboxd.com/{username.strip()}/films/rated/none/"
    soup = BeautifulSoup(requests.get(url_no_reviews).text, "html.parser")
    film_html_no_reviews = soup.find_all("li", class_=re.compile(r"poster-container"))

    # Use sets for efficient removal of unrated movies
    removed_names = set(regex_patterns["name"].findall(str(film_html_no_reviews)))
    removed_slugs = set(regex_patterns["slug"].findall(str(film_html_no_reviews)))

    # Filter out unrated movies from the main data. We don't need to
    # remove the ratings because the user never rated it.
    user_data_dict["names"] = [
        name for name in user_data_dict["names"] if name not in removed_names
    ]
    user_data_dict["slugs"] = [
        slug for slug in user_data_dict["slugs"] if slug not in removed_slugs
    ]

    # Fetch images for rated movies using the slug
    for slug in user_data_dict["slugs"]:
        film_url = f"https://letterboxd.com/film/{slug}/"
        # Make the soup object to scrap the websites html
        film_soup = BeautifulSoup(requests.get(film_url).text, "html.parser")
        # Get the url data
        script_data = film_soup.select_one('script[type="application/ld+json"]')

        # If we have a url, we format it and add to the list.
        if script_data:
            json_data = json.loads(script_data.text.split(" */")[1].split("/* ]]>")[0])
            user_data_dict["images"].append(json_data.get("image", ""))

    # Return the users letterboxd data as a dictionary
    return user_data_dict


def scrape_letterboxd_movie(movie_slug: str):
    """
    Scrapes details of a specific movie from Letterboxd using its slug.

    Args:
    - movie_slug: The slug part of the movie URL on Letterboxd (e.g., 'joker-folie-a-deux' for 'letterboxd.com/film/joker-folie-a-deux/')

    Returns:
    - Dictionary containing movie title, release year, genres, director, rating, actors (with Wikipedia URLs), poster image URL, summary, and reviews.
    """
    url = f"https://letterboxd.com/film/{movie_slug}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract JSON-LD data which contains movie details
    script_data = soup.select_one('script[type="application/ld+json"]')
    if not script_data:
        raise ValueError("Movie data not found on the page.")

    # Get the content of the script and strip the CDATA tags
    raw_data = script_data.string
    cleaned_data = re.sub(r"/\* <!\[CDATA\[ \*/|/\* \]\]> \*/", "", raw_data).strip()

    # Parse JSON data
    try:
        movie_data = json.loads(cleaned_data)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return None

    # Extract details from the JSON data
    title = movie_data.get("name", "Unknown Movie")
    year_element = soup.find("a", href=re.compile(r"/films/year/\d{4}/"))
    year = year_element.text if year_element else "N/A"

    genres = movie_data.get("genre", [])
    director = movie_data.get("director", [{}])[0].get("name", "N/A")
    rating = movie_data.get("aggregateRating", {}).get("ratingValue", 0.0)

    # Make the soup object to scrap the websites html
    film_soup = BeautifulSoup(requests.get(url).text, "html.parser")
    image_script_data = film_soup.select_one('script[type="application/ld+json"]')
    json_data = json.loads(image_script_data.text.split(" */")[1].split("/* ]]>")[0])
    poster_url = json_data.get("image", "")

    # Extract actors and create Wikipedia links for each
    actors = [
        {
            "name": actor["name"],
            "wiki_url": f"https://en.wikipedia.org/wiki/{actor['name'].replace(' ', '_')}",
        }
        for actor in movie_data.get("actors", [])
    ]

    # Extract the summary
    summary_tag = soup.find("meta", property="og:description")
    summary = summary_tag["content"] if summary_tag else "No summary available"

    reviews = []
    review_elements = soup.find_all("li", class_="film-detail")

    for review in review_elements:
        reviewer_name = (
            review.find("strong", class_="name").text.strip()
            if review.find("strong", class_="name")
            else "Unknown"
        )

        # Check for hidden-spoiler text first, then fallback to main body-text div
        review_content_div = review.find(
            "div", class_="hidden-spoilers expanded-text"
        ) or review.find("div", class_="body-text -prose collapsible-text")

        # Get all paragraphs within the selected review content and join them
        if review_content_div:
            paragraphs = review_content_div.find_all("p")
            review_content = " ".join(p.text.strip() for p in paragraphs)
        else:
            review_content = "No content available"

        like_count = (
            review.find("p", class_="like-link-target").get("data-count", "0")
            if review.find("p", class_="like-link-target")
            else "0"
        )

        # Append each review to the list
        reviews.append({"reviewer": reviewer_name, "content": review_content, "likes": like_count})

    # Return the results in a dictionary
    return {
        "id": movie_slug,
        "title": title,
        "year": year,
        "genres": genres,
        "director": director,
        "rating": rating,
        "actors": actors,
        "movie_image": poster_url,
        "summary": summary,
        "reviews": reviews,
    }


def search_movies_from_csv(query):
    df = pd.read_csv("model/data/movies.csv")
    filtered = df[df["movie_title"].str.contains(query, case=False, na=False)]
    return filtered.to_dict("records")


def scrape_recommended_movies(movie_slugs):
    movie_data = []  # List to hold data for each recommended movie

    for movie_slug in movie_slugs:
        # Construct the URL for each recommended movie
        url = f"https://letterboxd.com/film/{movie_slug}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the JSON-LD data for each movie
        script_with_data = soup.select_one('script[type="application/ld+json"]')

        if script_with_data:  # Ensure that script_with_data is not None
            try:
                json_obj = json.loads(script_with_data.text.split(" */")[1].split("/* ]]>")[0])

                # Extract movie title, ID (slug), and image URL
                movie_title = json_obj["name"]
                movie_image = json_obj["image"]
                movie_id = movie_slug
                try:
                    movie_rating = json_obj["aggregateRating"]["ratingValue"]
                except KeyError:
                    movie_rating = ""

                # Append data to list as a dictionary
                movie_data.append(
                    {
                        "title": movie_title,
                        "movie_id": movie_id,
                        "image": movie_image,
                        "rating": movie_rating,
                    }
                )
            except Exception as e:
                print(f"Error parsing JSON-LD for {movie_slug}: {e}")
        else:
            print(f"Warning: No JSON-LD data found for {movie_slug}")

    return movie_data


# Method to scrape a given letterboxd username and return a dataframe with the movie names and the star ratings.
def scrape_and_make_dataframe(username: str) -> pd.DataFrame:
    # Scrape the movies and ratings from the given letterboxd username
    user_data_dict = scrape_letterboxd(username)

    # Make a list of size (movie_name) for the usernames, Not necessary just included it
    username_list = [username] * len(user_data_dict["names"])

    # Return the results as a Pandas dataframe
    return pd.DataFrame(
        {
            "user_name": username_list,
            "film_id": user_data_dict["slugs"],
            "Movie_name": user_data_dict["names"],
            "rating": user_data_dict["ratings"],
            "image": user_data_dict["images"],
        }
    )


if __name__ == "__main__":
    # Sample use
    # username = input("Please type your letterboxd username : ")
    # print(f"Now scraping : {username}")
    # df = scrape_and_make_dataframe(username.strip())
    # print(df)
    scrape_letterboxd_movie("joker-folie-a-deux")
