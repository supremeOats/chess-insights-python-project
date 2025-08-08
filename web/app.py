from . import create_app

app = create_app()

from src.data_manager.data_provider import get_profile, get_game, get_archive
from flask import render_template, request, redirect, url_for

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")

# @app.route("/user", methods=["GET", "POST"])
# def user():
#     return render_template("user_profile.html", username=request.form["username"])

@app.route("/to-profile-page", methods=["POST"])
def to_profile_page():
    username = request.form["username"]  # extract from submitted form
    return redirect(url_for("profiles", username=username))

@app.route("/profiles/<username>", methods=["GET", "POST"])
def profiles(username):
    profile = get_profile(username)

    if profile is None:
        return render_template("not_found.html")
    
    return render_template("user_profile.html", profile=profile)

@app.route("/profiles/<username>/<year>/<month>", methods=["GET", "POST"])
def archive(username, year: int, month: int):
    archive = get_archive(username, int(year), int(month))

    if archive is None:
        return render_template("not_found.html")

    return render_template("user_archive.html", archive=archive)
