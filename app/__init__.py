from flask import Flask  # type: ignore
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore

from app.routes import init_routes
from app.exceptions import init_exception_handler


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)

    from app.db_models.user import User
    from app.db_models.movie_rating import MovieRating

    with app.app_context():
        # db.drop_all()
        db.create_all()

        # ------------------------------------------  EXAMPLE OPERATIONS  ------------------------------------------
        # test_user = User(id="testID", username="test", email="test@test.test", password="testtest", ratings=[], profile_image_id="", profile_image_url="", letterbox_username="")
        # db.session.add(test_user)
        # db.session.commit()

        # user = User.query.get("testID")
        # test_rating = MovieRating(movie_title="Movie1", movie_id=2, _rating=4, user_id=user.id, user=user)

        # db.session.add(test_rating)
        # db.session.commit()
        # print(User.query.all())
        # ------------------------------------------  EXAMPLE OPERATIONS  ------------------------------------------

    init_routes(app)
    init_exception_handler(app)
    return app
