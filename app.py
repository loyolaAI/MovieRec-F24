from app.__init__ import create_app, db
# from flask_migrate import Migrate

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
