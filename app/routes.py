from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user  # type: ignore
from werkzeug.security import check_password_hash
from datetime import datetime

from app.functions.movie_recommender import movie_recommendation
from app.mockdata import data

from app.functions.user_actions import (
    get_user_by_email,
    create_user,
    create_reset_token,
    delete_reset_token,
    get_reset_token,
    update_password,
)
from app import db


def init_routes(app):
    @app.route("/")
    @login_required
    def home():
        return render_template("index.html", user=current_user)

    # ================== Authentication ==================
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
        does_user_exist = get_user_by_email(email)
        if does_user_exist:
            flash("Email address already exists")
            return redirect(url_for("signup"))

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
        user = get_user_by_email(email)
        if not user:
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

        # Check if password is correct
        if not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

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
        email = request.get_json()["email"]

        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            flash("User not found")

        reset_token = []

        # Check if there is already a reset password token
        # If there is, delete the existing one and create a new one
        if not user.reset_token:
            reset_token.append(create_reset_token(user))
        elif user.reset_token:
            if user.reset_token.expires_at > datetime.now():
                delete_reset_token(user.reset_token)
                reset_token.append(create_reset_token(user))
            elif user.reset_password_token.expires_at < datetime.now():
                reset_token.append(create_reset_token(user))

        db.session.add(reset_token[0])
        db.session.commit()

        return jsonify({"Status": 200, "token": reset_token[0].token})

    @app.route("/reset-password-token", methods=["POST"])
    def reset_password_token_post():
        token = request.get_json()["reset-token"]
        new_password = request.get_json()["password"]

        reset_token = get_reset_token(token)

        # Check if token exists
        if not reset_token:
            flash("Token not found")
            return jsonify({"Status": 404, "Message": "Token not found"})

        # Check if token is expired
        if reset_token.expires_at < datetime.now():
            flash("Token has expired")
            return jsonify({"Status": 400, "Message": "Token expired"})

        # Update user password
        update_password(reset_token.user, new_password)

        return jsonify({"Status": 200, "Message": "Password updated successfully"})

    # ================== Authentication ==================

    # Recommendation
    @app.route("/recommend", methods=["POST"])
    def recommend():
        data = request.json
        recommendation = movie_recommendation([data["input"]])  # Adjust based on your input format
        return jsonify({"recommendations": recommendation.tolist()})

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
