from .models import Profile, Archive, Game, ColorPlayer
from .api_client import fetch_profile_from_api, fetch_archive_from_api
from .database_manager import *
from datetime import date, timedelta, datetime
from dateutil import relativedelta as rd
from typing import Callable
from sqlalchemy.orm import joinedload

def get_profile(username: str) -> Profile | None:
    player = load_profile_from_db(username)
    
    if player is None:
        try:
            player = fetch_profile_from_api(username)
            add_profile(player)
        except(ValueError or ConnectionError):
            return None

    return player

def get_archive(username:str, year: int, month: int) -> Archive | None:
    profile = get_profile(username)
    if profile is None:
        return None
    
    archive = load_archive_from_db(username, year, month)
    
    if archive is None:
        try:
            archive = fetch_archive_from_api(username, year, month)
            add_archive(archive)
        except(ValueError or ConnectionError):
            return None
        
    return archive

def get_games_alt(username:str, start_date: date, end_date: date) -> list[Game]:
    if start_date > end_date:
        return []

    archives = [
        get_archive(username, date.year, date.month)
        for date in daterange(start_date, end_date, rd.relativedelta(months=1))
    ]

    games = [
        game
        for archive in archives
        if archive is not None
        for game in archive.games
        if start_date <= game.end_time <= end_date
    ]

    return games

def get_games(username:str, start_date: date, end_date: date, **filters) -> list[Game]:
    
    if not load_archive_range(username, start_date, end_date):
        return []

    game_rows = load_games_from_db(username, start_date, end_date)

    if "opponent" in filters:
        game_rows = filter_by_opponent(game_rows, filters["opponent"])
    
    if "min_accuracy" in filters:
        game_rows = filter_by_min_accu(game_rows, filters["min_accuracy"], username)

    if "max_accuracy" in filters:
        game_rows = filter_by_max_accu(game_rows, filters["max_accuracy"], username)

    if "result" in filters:
        game_rows = filter_by_result(game_rows, filters["result"], username)

    return [game for game in game_rows]

def daterange(start: date, stop: date, step = rd.relativedelta(days=1)) -> list[date]:
    dates = []
    curr: date = start
    while curr <= stop:
        dates.append(curr)
        curr += step

    return dates

def load_archive_range(username:str, start_date: date, end_date: date) -> bool:
    if start_date > end_date:
        return False

    archives = [
        get_archive(username, date.year, date.month)
        for date in daterange(start_date, end_date, rd.relativedelta(months=1))
    ]

    return True

def parse_date(date_str: str | None) -> date | None:
    if not date_str:
        return None
    
    (y, m, d) = date_str.split('-')
    return date(int(y), int(m), int(d))

def get_game_id(game_url: str) -> str:
    """
    Return the game id, proved the chess.com url for that game.
    The return value is a string.
    """

    import re
    pattern = r"https://www\.chess\.com/game/live/(\d+)"
    match = re.search(pattern, game_url)

    if match is None:
        raise ValueError("Invalid game link")
    
    return match.group(1)

