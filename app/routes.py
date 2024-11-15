from flask import request, jsonify, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user, login_user, logout_user  # type: ignore
from werkzeug.security import check_password_hash
from datetime import datetime
from model.scraping import scrape_letterboxd_movie, scrape_letterboxd, scrape_recommended_movies
from model.main import get_recommendations
import csv
from math import ceil


# from model.main import get_recommendations

import sys

sys.path.append("..")

from app.functions.movie_recommender import movie_recommendation
from app.db_models.user import User
from app.db_models.password_reset_token import PasswordResetToken as Pass
from app.db_models.movie import Movie
from app.db_models.movie_rating import MovieRating

from app.functions.user_actions import (
    scrape_user_ratings,
    create_user,
    update_password,
    send_password_reset_email,
    update_user,
)
from app import db


def init_routes(app):
    @app.route("/")
    @login_required
    def home():
        return render_template("index.html", movies=User.get_rated_movies(current_user))

    @app.route("/discover", methods=["GET", "POST"])
    def discover():
        recommendations = []  # Initialize an empty list for recommendations
        if request.method == "POST":
            data = request.form
            username = data.get("username")
            accuracy = float(data.get("accuracy", 0.01))
            number_recs = int(data.get("number_recs", 10))
            obscureness = int(data.get("obscureness", 9))

            # Ensure the username is provided
            if not username:
                return jsonify({"error": "Username is required"}), 400

            try:
                # Get recommendations and extract only the film IDs
                recommendation_dicts = get_recommendations(
                    username, accuracy, number_recs, obscureness
                )
                recommendation_slugs = [rec["film_id"] for rec in recommendation_dicts]

                # Scrape data for each recommended movie using just the film_id
                recommendations = scrape_recommended_movies(recommendation_slugs)

            except Exception as e:
                print(f"Error generating recommendations: {e}")
                return jsonify({"error": "Failed to generate recommendations"}), 500

        return render_template(
            "discover.html", recommendations=recommendations, username=current_user.username
        )

    @app.route("/search", methods=["GET", "POST"])
    def search():
        query = request.form.get("query") if request.method == "POST" else request.args.get("query", "")
        page = int(request.args.get("page", 1))  # Current page, defaults to 1
        results_per_page = 5
        search_results = []

        # Read movies from CSV
        movies = []
        with open("model/data/movies.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movies.append(row)

        # Process query and filter movies
        if query:
            filtered_results = [
                movie
                for movie in movies
                if query.lower() in movie["movie_title"].lower()
                or query.lower() in movie["genres"].lower()
            ]

            # Pagination logic
            total_pages = ceil(len(filtered_results) / results_per_page)
            start = (page - 1) * results_per_page
            end = start + results_per_page
            paginated_results = filtered_results[start:end]

            # Fetch additional details for the paginated results
            try:
                for movie in paginated_results:
                    movie_data = scrape_letterboxd_movie(movie["film_id"])
                    movie["poster_url"] = movie_data.get("movie_image", "")
                    movie["rating"] = movie_data.get("rating", "")
                search_results = paginated_results
            except Exception as e:
                print(f"Error processing search query '{query}': {e}")
                return jsonify({"error": "Failed to process search query"}), 500

            return render_template(
                "search.html",
                search_results=search_results,
                query=query,
                page=page,
                total_pages=total_pages
            )



    # @app.route("/popular", methods=["GET"])
    # def popular():
    #     return render_template("popular.html")  # TODO

    @app.route("/recent", methods=["GET"])
    def recent():
        return render_template("recent.html", movies=User.get_rated_movies(current_user))

    @app.route("/movie_info/<movie_id>", methods=["GET"])
    def movie_info(movie_id):
        try:
            print("movie_id:", movie_id)

            movie_data = scrape_letterboxd_movie(movie_id)
            if not movie_data or not movie_data.get("title"):
                return render_template("error.html", error="Movie data not found")
            print("Final movie data:", movie_data)
            return render_template("movie_info.html", movie=movie_data)
        except Exception as e:
            print(e)
            print("movie_id:", movie_id)
            return render_template("error.html", error=e)

    # # Fetch Movie Data
    # @app.route("/movie/<int:movie_id>", methods=["GET"])
    # def fetch_movie_data(movie_id):
    #     # Validity Check
    #     # Fetch using 'movie_data' function
    #     # Throw exception if there is not movie data
    #     return

    # ================== Authentication Related ==================
    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html")

    @app.route("/profile", methods=["POST"])
    @login_required
    def profile_post():
        email = request.form.get("email")
        username = request.form.get("username")
        letterboxd = request.form.get("letterboxd")
        image = request.files.get("pfp", None)

        # Save Image
        if image:
            current_user.upload_image(image)

        # Update User
        update_user(current_user, username, email, letterboxd)

        return redirect(url_for("profile"))

    @app.route("/profile", methods=["DELETE"])
    @login_required
    def delete_image():
        User.get_by_email(current_user.email).delete_image()
        return jsonify({"Status": 200, "Message": "Image deleted successfully"})

    @app.route("/scrape-letterboxd", methods=["POST"])
    @login_required
    def scrape_letterboxd():
        scrape_user_ratings(current_user)
        db.session.commit()

        return redirect(url_for("home"))

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/signup", methods=["POST"])
    def signup_post():
        email = request.form.get("email")
        username = request.form.get("username")
        letterboxd = request.form.get("letterboxd")
        password = request.form.get("password")

        # Check if user already exists
        does_user_exist = User.get_by_email(email)
        if does_user_exist:
            flash("Error: Email address already exists")
            return redirect(url_for("signup"))

        # Create User
        new_user = create_user(email, username, password, letterboxd)

        # Scrape User Ratings, this function adds the ratings to the user object and DB
        scrape_user_ratings(new_user)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login_post():
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        # Check if user exists
        user = User.get_by_email(email)
        if not user:
            flash("Error: Please check your login details and try again.")
            return redirect(url_for("login"))

        # Check if password is correct
        if not check_password_hash(user.password, password):
            flash("Error: Please check your login details and try again.")
            return redirect(url_for("login"))

        # While we're at it, check if there are any expired reset tokens
        # If we find any, delete them
        token = user.reset_token
        if token is not None and token.expires_at < datetime.now():
            Pass.delete_reset_token(token)

        login_user(user, remember=remember)
        return redirect(url_for("home"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/reset-password")
    def reset_password():
        return render_template("reset-password.html")

    @app.route("/reset-password", methods=["POST"])
    def reset_password_post():
        email = request.form.get("email")

        # Check if user exists
        user = User.get_by_email(email)
        if user is None:
            flash("Error: User not found.")
            return redirect(url_for("reset_password"))

        reset_token = []

        # Check if there is already a reset password token
        # If there is, delete the existing one and create a new one
        if not user.reset_token:
            reset_token.append(Pass.create_reset_token(user))
        elif user.reset_token:
            if user.reset_token.expires_at > datetime.now():
                Pass.delete_reset_token(user.reset_token)
                reset_token.append(Pass.create_reset_token(user))
            elif user.reset_token.expires_at < datetime.now():
                reset_token.append(Pass.create_reset_token(user))

        db.session.add(reset_token[0])
        db.session.commit()

        # send_password_reset_email(user, reset_token[0])
        flash("Password reset email sent successfully.")
        return redirect(url_for("reset_password"))

    @app.route("/reset-password-token", methods=["POST"])
    def reset_password_token_post():
        token = request.form.get("reset-token")
        new_password = request.form.get("password")

        reset_token = Pass.get_reset_token(token)

        # Check if token exists
        if not reset_token:
            flash("Error: Token not found.")
            return redirect(url_for("reset_password"))

        # Check if token is expired
        if reset_token.expires_at < datetime.now():
            flash("Error: Token has expired.")
            return redirect(url_for("reset_password"))

        # Update user password
        update_password(reset_token.user, new_password)
        Pass.delete_reset_token(reset_token)

        flash("Password updated successfully.")
        return redirect(url_for("login"))

    # ================== Authentication Related ==================
