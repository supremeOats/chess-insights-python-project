from flask import Flask
from src.data_manager.models import db
from flask_migrate import Migrate

migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chesscom.db"

    db.init_app(app)
    migrate.init_app(app, db)

    return app