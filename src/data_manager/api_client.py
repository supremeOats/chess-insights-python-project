import requests
from .models import Profile, Game, Archive
from .database_manager import *
from pathlib import Path
import datetime

PROFILE_URL_BASE = "https://api.chess.com/pub/player"

USER_AGENT_DATA = {"user-agent": "username: spinjitzu_grandmaster_wu, email: philip.lisichkov@gmail.com"}

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

def is_request_successful(status_code) -> bool:
    if status_code == 200:
        print("Request successful")
        return True
    else:
        print(f"Request failed: {status_code}")
        return False

def fetch_profile_from_api(username: str) -> Profile:
    response = requests.get(f'{PROFILE_URL_BASE}/{username}', headers=USER_AGENT_DATA)
    
    if response.status_code == 404:
        raise ValueError("Profile does not exist")
    elif not is_request_successful(response.status_code):
        raise ConnectionError(response.status_code)
    
    player = Profile(response.json())
    
    return player

def fetch_archive_from_api(username: str, year: int, month: int) -> Archive:
    #validate
    
    period = datetime.datetime(year, month, 1)

    archive_url = f'{PROFILE_URL_BASE}/{username}/games/{period.year}/'
    if month < 10:
        archive_url += f"0{period.month}"
    else:
        archive_url += f"{period.month}"

    response = requests.get(
        archive_url,
        headers=USER_AGENT_DATA)
    
    if response.status_code == 404:
        raise ValueError("Archive does not exist")
    elif not is_request_successful(response.status_code):
        raise ConnectionError(response.status_code)
    
    try:
        response.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError("Response conent contains invalid JSON syntax")

    # respone -> archive
    #throw "Archive not avaliable"

    return Archive(username, year, month, response.json())
