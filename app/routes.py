from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user  # type: ignore
from werkzeug.security import check_password_hash
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

import model.data.ratings as ratings
from model.get_user_data import get_movie_dataframe
from model.build_colab_model import build_colab_model
from model.run_colab_model import run_colab_model
from model.scraping import scrape_and_make_dataframe

from app.functions.movie_recommender import movie_recommendation
from app.db_models.user import User
from app.db_models.password_reset_token import PasswordResetToken as Pass

from app.functions.user_actions import (
    create_user,
    update_password,
    send_password_reset_email,
    update_user,
)
from app import db

# from app.model.scraping import scrap_letterboxd


def init_routes(app):
    @app.route("/")
    # @login_required
    def home():
        return render_template("base.html")

    # Recommendation
    @app.route("/recommend", methods=["POST"])
    def recommend():
        try:
            # Extract JSON data from the request
            data = request.json
            accuracy = float(data.get("accuracy", 0.5))  # Default accuracy 0.5 if not provided
            username = data["username"]
            number_recs = int(data.get("count", 10))  # Default to 10 recommendations

            # Fetch the user movie data and scrape additional ratings
            df = get_movie_dataframe(accuracy)
            user_data = scrape_and_make_dataframe(username)

            # Build and run the collaborative model
            algo = build_colab_model(df, user_data, accuracy)
            recommendations = run_colab_model(algo, user_data, df, accuracy, username, number_recs)

            # Prepare the response with movie names and ratings
            rec_list = [
                {
                    "movie_name": rec["film_id"],
                    "rating": round(rec["unclipped_rating"], 2),
                }
                for rec in recommendations
            ]

            return jsonify({"recommendations": rec_list})

        except Exception as e:
            # Handle errors and return a message
            return jsonify({"error": str(e)}), 500

    # Fetch Movie Data
    @app.route("/movie/<int:movie_id>", methods=["GET"])
    def fetch_movie_data(movie_id):
        # Validity Check
        # Fetch using 'movie_data' function
        # Throw exception if there is not movie data
        return

    # Search For Movie(s)
    @app.route("/search", methods=["GET"])
    def search():
        # Validity Check
        # Movie Search
        # Throw exception if there is no movie, or give similar
        return

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

        # Fetch user ratings from letterbox
        # movie_names, movie_ratings = scrap_letterboxd(letterboxd)

        # Create User
        new_user = create_user(email, username, password, letterboxd)

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

    @app.route("/send-reset-email", methods=["POST"])
    def send_reset_email():
        email = request.form.get("email")
        user = User.get_by_email(email)
        if user is None:
            flash("Error: User not found.")
            return redirect(url_for("reset_password"))
        reset_token = []
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
        send_password_reset_email(user, reset_token[0])
        flash("Password reset email sent successfully.")
        return redirect(url_for("reset_password"))

    # ================== Authentication Related ==================
