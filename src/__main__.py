from data_manager.data_provider import get_profile, get_archive, clear_cache
from data_manager.models import db
from flask import Flask


# def main():

#     print(get_archive("erik", 2022, 9))

# if __name__ == "__main__":
#     main()

# if __name__ == "__main__":
#     app = Flask(__name__)

#     with app.app_context():
#         app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chesscom.db"
#         db.init_app(app)
#         db.create_all()

#         main()
