from .models import Profile, Archive, Game
from .api_client import fetch_profile_from_api, fetch_archive_from_api
from .database_manager import *

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
        
def get_game(game_id: int) -> Game:
    ...

