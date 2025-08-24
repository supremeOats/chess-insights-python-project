from .models import db, Profile, Game, Archive, ColorPlayer
from datetime import date
from sqlalchemy.orm import Query, aliased
from typing import Callable

def load_profile_from_db(username: str) -> Profile | None:
    """Retrun Profile object from database. If player not in DB return None object."""
    player = Profile.query.filter_by(username=username).first()
    return player

def load_archive_from_db(username: str, year: int, month: int) -> Archive | None:
    """Retrun Archive object from database. If archive not in DB return None object."""
    
    archive_date = date(year, month, 1)
    archive = Archive.query.filter_by(username=username, period=archive_date).first() 
    return archive

def load_games_from_db(username: str, start_date: date, end_date: date) -> Query[Game]:
    """Get Query of games matching a player username and dates"""

    White = aliased(ColorPlayer)
    Black = aliased(ColorPlayer)

    games = (
        db.session.query(Game)
        .join(White, Game.white)    # type: ignore
        .join(Black, Game.black)    # type: ignore
        .filter(
            (White.username == username)
          | (Black.username == username),
            Game.end_time >= start_date,    # type: ignore
            Game.end_time <= end_date       # type: ignore
        )
    )

    return games

def add_profile(player: Profile):
    """Store player profile to database"""
    db.session.add(player)
    db.session.commit()

def add_archive(archive: Archive) -> None:
    """Store player archive to database"""
    db.session.add(archive)
    db.session.commit()

def clear_cache() -> None:
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

def filter_by_opponent(query: Query[Game], opponent: str) -> Query[Game]:    
    White = aliased(ColorPlayer)
    Black = aliased(ColorPlayer)
    
    query = query.join(White, Game.white).join(Black, Game.black).filter( # type: ignore
            (White.username == opponent)
          | (Black.username == opponent)
        )
    
    return query

def filter_by_min_accu(query: Query[Game], threshold: float, player: str):
    return filter_by_accuracy(query, threshold, player, lambda x,y : x >= y)

def filter_by_max_accu(query: Query[Game], threshold: float, player: str):
    return filter_by_accuracy(query, threshold, player, lambda x,y : x <= y)

def filter_by_accuracy(query: Query[Game], threshold: float, player: str, comparison):
    White = aliased(ColorPlayer)
    Black = aliased(ColorPlayer)
    
    query = query.join(White, Game.white).join(Black, Game.black) # type: ignore

    query = query.filter(
        (White.username == player) & comparison(White.accuracy, threshold)
      | (Black.username == player) & comparison(Black.accuracy, threshold)
    )
    
    return query

def filter_by_result(query: Query[Game], result: str, player: str):
    White = aliased(ColorPlayer)
    Black = aliased(ColorPlayer)

    query = query.join(White, Game.white).join(Black, Game.black) # type: ignore

    query = query.filter(
        (White.username == player) & (White.result == result)
      | (Black.username == player) & (Black.result == result)
    )

    return query
