from . import create_app

app = create_app()

from src.data_manager.data_provider import get_profile, get_archive, get_games, parse_date
from src.data_manager.database_manager import clear_cache
from flask import render_template, request, redirect, url_for
from src.analyzer.data_analysis import Analysis

from datetime import date
from dateutil.relativedelta import relativedelta
    
@app.route("/")
@app.route("/home")
def index():    
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


@app.route("/to-profile-page", methods=["POST"])
def to_profile_page():
    username = request.form["username"]
    return redirect(url_for("profiles", username=username))


@app.route("/profiles/<username>", methods=["GET", "POST"])
def profiles(username):
    profile = get_profile(username)

    if profile is None:
        return render_template("not_found.html")
    
    return render_template("user_profile.html", profile=profile)


@app.route("/profiles/<username>/<year>/<month>", methods=["GET", "POST"])
def archive(username, year, month):

    archive = get_archive(username, int(year), int(month))
    profile = get_profile(username)

    if archive is None:
        return render_template("not_found.html")

    # return render_template("user_archive.html", profile=profile, archive=archive)
    return render_template("user_archive.html", profile=profile, archive=archive)


@app.route("/profiles/<username>/games", methods=["GET", "POST"])
def games(username: str,):
    curr_date = date.today()
    last_month = curr_date-relativedelta(weeks=+1)
    
    start_date = parse_date(request.form.get("start_date")) 
    if start_date is None: start_date = last_month
    end_date   = parse_date(request.form.get("end_date"))
    if end_date is None: end_date = curr_date

    opponent   = request.form.get("opponent")
    min_accuracy    = request.form.get("min_accuracy", type=float)
    max_accuracy    = request.form.get("max_accuracy", type=float)
    result     = request.form.get("result")
    
    filters = {}
    if opponent:        filters["opponent"] = opponent
    if min_accuracy:    filters["min_accuracy"] = min_accuracy
    if max_accuracy:    filters["max_accuracy"] = max_accuracy
    if result:          filters["result"] = result

    games = get_games(username, start_date, end_date, **filters)
    
    analysis = Analysis(games, username, start_date, end_date)

    return render_template("user_games.html", username=username, games=games, analysis=analysis)


@app.route("/tables")
def tables():
    return render_template("tables_test.html")

@app.route("/admin/clear")
def clear():
    clear_cache()
    return render_template("admin.html")
