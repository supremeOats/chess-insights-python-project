from . import create_app, db

from flask import render_template, request, redirect, url_for
from datetime import date
from dateutil.relativedelta import relativedelta

from src.data_manager.data_provider import get_profile, get_archive, get_games, parse_date, get_game_id
from src.data_manager.database_manager import clear_cache
from src.analyzer.data_analysis import Analysis
from src.replay_system.pgn_parser import parse_pgn, list_moves
    
app = create_app()
with app.app_context():
    db.create_all()


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

@app.route("/to-replay", methods=["POST"])
def to_replay():
    url = request.form["url"]
    pgn = request.form["pgn"]
    
    id = get_game_id(url)
    
    return redirect(url_for("replay", id=id, pgn=pgn))


@app.route("/game-replay/<id>", methods=["GET", "POST"])
def replay(id: str):
    pgn = request.args.get("pgn")
    if pgn is None:
        return render_template("not_found.html")

    moves = list_moves(parse_pgn(pgn))
    
    return render_template("game_replay.html", moves=moves)


GAME = "[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"2025.07.01\"]\n[Round \"-\"]\n[White \"KATPAH\"]\n[Black \"Hikaru\"]\n[Result \"0-1\"]\n[CurrentPosition \"4Q3/5rk1/1p1P4/p3R1p1/PP6/8/2P2q2/5nK1 w - - 2 53\"]\n[Timezone \"UTC\"]\n[ECO \"B06\"]\n[ECOUrl \"https://www.chess.com/openings/Modern-Defense-Standard-Two-Knights-Variation...5.a4-b6-6.Bc4-e6-7.O-O\"]\n[UTCDate \"2025.07.01\"]\n[UTCTime \"14:47:40\"]\n[WhiteElo \"2825\"]\n[BlackElo \"3363\"]\n[TimeControl \"180\"]\n[Termination \"Hikaru won by resignation\"]\n[StartTime \"14:47:40\"]\n[EndDate \"2025.07.01\"]\n[EndTime \"14:53:20\"]\n[Link \"https://www.chess.com/game/live/145694969449\"]\n\n1. e4 {[%clk 0:03:00]} 1... g6 {[%clk 0:03:00]} 2. d4 {[%clk 0:02:59]} 2... Bg7 {[%clk 0:02:59.5]} 3. Nf3 {[%clk 0:02:58.3]} 3... d6 {[%clk 0:02:57.8]} 4. Bc4 {[%clk 0:02:57.5]} 4... e6 {[%clk 0:02:57]} 5. O-O {[%clk 0:02:54]} 5... a6 {[%clk 0:02:56.4]} 6. a4 {[%clk 0:02:52.8]} 6... b6 {[%clk 0:02:55.6]} 7. Nc3 {[%clk 0:02:51.2]} 7... Bb7 {[%clk 0:02:55]} 8. Bg5 {[%clk 0:02:47.8]} 8... Ne7 {[%clk 0:02:54.3]} 9. e5 {[%clk 0:02:45.3]} 9... h6 {[%clk 0:02:51.1]} 10. exd6 {[%clk 0:02:34.2]} 10... cxd6 {[%clk 0:02:47.9]} 11. Bf4 {[%clk 0:02:33.1]} 11... g5 {[%clk 0:02:45.8]} 12. Bg3 {[%clk 0:02:31.2]} 12... Nf5 {[%clk 0:02:45.2]} 13. Re1 {[%clk 0:02:26.6]} 13... O-O {[%clk 0:02:43.6]} 14. d5 {[%clk 0:02:23.9]} 14... e5 {[%clk 0:02:41.6]} 15. Bd3 {[%clk 0:02:17.9]} 15... Nxg3 {[%clk 0:02:39]} 16. hxg3 {[%clk 0:02:17.3]} 16... f5 {[%clk 0:02:38.7]} 17. Bc4 {[%clk 0:02:07.2]} 17... Nd7 {[%clk 0:02:33.6]} 18. g4 {[%clk 0:01:59.9]} 18... fxg4 {[%clk 0:02:32.7]} 19. Nh2 {[%clk 0:01:56.1]} 19... h5 {[%clk 0:02:30.4]} 20. Nf1 {[%clk 0:01:54.9]} 20... Nf6 {[%clk 0:02:24.9]} 21. Ne3 {[%clk 0:01:52.6]} 21... Bc8 {[%clk 0:02:18.4]} 22. Bd3 {[%clk 0:01:49.4]} 22... Ra7 {[%clk 0:02:17.5]} 23. Nf5 {[%clk 0:01:45.5]} 23... Kh8 {[%clk 0:02:11.8]} 24. Ng3 {[%clk 0:01:36.6]} 24... h4 {[%clk 0:02:08]} 25. Nge4 {[%clk 0:01:36]} 25... Nxe4 {[%clk 0:02:04]} 26. Nxe4 {[%clk 0:01:35.9]} 26... Raf7 {[%clk 0:01:59.7]} 27. Qd2 {[%clk 0:01:34.6]} 27... Rf4 {[%clk 0:01:55.3]} 28. g3 {[%clk 0:01:32.8]} 28... R4f5 {[%clk 0:01:49.5]} 29. Rf1 {[%clk 0:01:25.6]} 29... a5 {[%clk 0:01:45.9]} 30. Nc3 {[%clk 0:01:23.7]} 30... Rf3 {[%clk 0:01:44.3]} 31. Ne4 {[%clk 0:01:22.4]} 31... Bh6 {[%clk 0:01:40.1]} 32. Be2 {[%clk 0:01:18.4]} 32... R3f7 {[%clk 0:01:39]} 33. b4 {[%clk 0:01:16.3]} 33... Bf5 {[%clk 0:01:37.8]} 34. Bd3 {[%clk 0:01:12]} 34... Bd7 {[%clk 0:01:12.9]} 35. Nxd6 {[%clk 0:01:08.8]} 35... Rf3 {[%clk 0:01:12]} 36. Ne4 {[%clk 0:01:07.9]} 36... Bf5 {[%clk 0:01:11.2]} 37. d6 {[%clk 0:01:05.7]} 37... hxg3 {[%clk 0:01:08.9]} 38. fxg3 {[%clk 0:01:03.3]} 38... Qa8 {[%clk 0:01:06.4]} 39. Rxf3 {[%clk 0:01:01.6]} 39... gxf3 {[%clk 0:01:05.9]} 40. Nf2 {[%clk 0:00:59.1]} 40... e4 {[%clk 0:01:01.8]} 41. Bxe4 {[%clk 0:00:57.8]} 41... Bxe4 {[%clk 0:01:01.2]} 42. Re1 {[%clk 0:00:54.5]} 42... Qd5 {[%clk 0:00:57.2]} 43. Qc3+ {[%clk 0:00:52]} 43... Bg7 {[%clk 0:00:56.1]} 44. Qc7 {[%clk 0:00:51.7]} 44... Bd4 {[%clk 0:00:53.2]} 45. Qe7 {[%clk 0:00:34.8]} 45... Bxf2+ {[%clk 0:00:50.7]} 46. Kh2 {[%clk 0:00:34.3]} 46... Rf7 {[%clk 0:00:34.3]} 47. Qe8+ {[%clk 0:00:31.6]} 47... Kg7 {[%clk 0:00:33.3]} 48. Rxe4 {[%clk 0:00:29.6]} 48... Bxg3+ {[%clk 0:00:26.7]} 49. Kxg3 {[%clk 0:00:28.2]} 49... f2 {[%clk 0:00:26.6]} 50. Re5 {[%clk 0:00:15.6]} 50... Qf3+ {[%clk 0:00:25.7]} 51. Kh2 {[%clk 0:00:14]} 51... f1=N+ {[%clk 0:00:25.6]} 52. Kg1 {[%clk 0:00:13.3]} 52... Qf2+ {[%clk 0:00:25.2]} 0-1\n"
