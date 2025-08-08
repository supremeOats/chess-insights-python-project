from flask_sqlalchemy import SQLAlchemy

from enum import Enum
from typing import Any
import datetime as dt

db = SQLAlchemy()

class MasterTitle(Enum):
    GM = "GM"
    WGM = "WGM"
    IM = "IM"
    WIM = "WIM"
    FM = "FM"
    WFM = "WFM"
    NM = "NM"
    WNM = "WNM",
    CM = "CM"
    WCM = "WCM"
    NONE = "N/A"

    def __str__(self):
        return self.name

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String, unique=True)
    name = db.Column("name", db.String)

    title = db.Column("title", db.String)
    rating = db.Column("rating", db.Integer)

    pfp_url = db.Column("pfp_url", db.String)
    country = db.Column("country", db.String)
    joined = db.Column("joined", db.DateTime)

    api_url = db.Column("api_url", db.String, unique=True)
    url = db.Column("url", db.String, unique=True)

    def __init__(self, player: dict[str, Any]) -> None:
        #validate_json
        self.username = player["username"]
        self.name = player.setdefault("name", "N/A")
        self.id = player["player_id"]
        self.title = player.setdefault("title", str(MasterTitle.NONE))
        self.pfp_url = player.setdefault("avatar", "N/A")
        self.country = player["country"]
        self.joined = dt.datetime.fromtimestamp(player["joined"])
        self.api_url = player["@id"]
        self.url = player["url"]

    def to_json(self):
        return {
            "@id": self.api_url,
            "url": self.url,
            "username": self.username,
            "player_id": self.id,
            "title": self.title.__str__(),
            "name": self.name,
            "avatar": self.pfp_url,
            "country": self.country,
            "joined": self.joined.timestamp()
        }
    
    def __str__(self):
        return f"""
            {self.username}'s profile:\n
            \t@id: {self.api_url}\n
            \turl: {self.url}\n
            \tplayer_id: {self.id}\n
            \ttitle: {self.title}\n
            \tname: {self.name}\n
            \tavatar: {self.pfp_url}\n
            \tcountry: {self.country}\n
            \tjoined: {self.joined.date}
        """

class ColorPlayer(db.Model):
    username = db.Column(db.String, db.ForeignKey('profiles.username'), primary_key=True)
    rating = db.Column("rating", db.Integer)
    result = db.Column("result", db.String)

    def __init__(self, username: str, rating: int, result: str) -> None:
        self.username = username
        self.rating = rating
        self.result = result
        
DEFAULT_STR = "N/A"

class Archive(db.Model):
    __tablename__ = 'archives'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, db.ForeignKey('profiles.username'))
    period = db.Column("period", db.Date)

    games = db.relationship('Game', back_populates='archive', cascade="all, delete-orphan")
   
    def __init__(self, username: str, year: int, month: int, json_obj: dict[str, Any]) -> None:
        self.username = username
        self.period = dt.datetime(year, month, 1)
        self.games = json_obj["games"]

    def to_json(self):
        return {
            "username": self.username,
            "year": self.period.year,
            "month": self.period.month
            #"games": ...?
        }

class Game(db.Model):
    __tablename__ = 'games'

    #Basic information
    url = db.Column("url", db.String, primary_key=True)
    start_time = db.Column("start_time", db.DateTime) #optional
    end_time = db.Column("end_time", db.DateTime)
    time_control = db.Column("time_control", db.String)
    rules = db.Column("rules", db.String)

    #Play info
    fen = db.Column("fen", db.String)
    pgn = db.Column("pgn", db.String)
    accuracy_white = db.Column("accu_white", db.Float)
    accuracy_black = db.Column("accu_black", db.Float)
    eco = db.Column("eco", db.String)

    #Players info
    white = db.Column("white", db.String) #ColorPlayer
    black = db.Column("black", db.String) #ColorPlayer

    tournament = db.Column("tournament_url", db.String) #optional
    match = db.Column("match_url", db.String) #optional

    #Archive
    archive_id = db.Column(db.Integer, db.ForeignKey(Archive.id, name="game_archive"), nullable=False)
    archive = db.relationship('Archive', back_populates='games')

    def __init__(self, game: dict[str, Any]):
        self.url = game["url"]
        self.start_time = game.setdefault("start_time", 0)
        self.end_time = game["end_time"]
        self.time_control = game["time_control"]
        self.rules = game["rules"]

        self.fen = game["fen"]
        self.pgn = game["pgn"]
        self.accuracies = game["accuracies"]
        self.eco = game.setdefault("eco", DEFAULT_STR)

        self.white = game["white"]
        self.black = game["black"]

        self.tournament = game.setdefault("tournament", DEFAULT_STR)
        self.match = game.setdefault("match", DEFAULT_STR)

    def result(self) -> str:
        return "white wins" if self.white.result == "win" else "black wins" if self.black.result == "win" else "draw"
