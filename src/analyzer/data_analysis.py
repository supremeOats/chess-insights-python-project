from ..data_manager.data_provider import get_profile, get_archive
from ..data_manager.models import Profile, Game, Archive

from datetime import date

class Analysis:
    games_count: int        = 0
    won_games: int          = 0
    win_rate: float         = 0
    average_accuracy: float = 0
    openings: list[str]     = []
    
    _player: str
    _start_date: date
    _end_date: date

    def __init__(self, games: list[Game], username: str, start_date: date, end_date: date) -> None:              
        self._player = username
        self._start_date = start_date
        self._end_date = end_date

        win_data = win_ratio(games, username)

        self.games_count = len(games)
        self.won_games = win_data[0]
        self.win_rate = win_data[1]
        self.average_accuracy = avg_accuracy(games, username)
        self.openings = openings(games)

def openings(games: list[Game]) -> list[str]:
    openings_count: dict[str, int] = {}
    
    for game in games:
        curr = parse_opening(game.eco)

        if not curr in openings_count:
            openings_count[curr] = 0
        else:
            openings_count[curr] += 1
    
    return sorted(openings_count, key=lambda k: openings_count[k])
    
def win_ratio(games: list[Game], username: str) -> tuple[int, float]:
    if not games:
        return (0,0)

    wins = 0
    
    for game in games:
        if game.white.username == username:
            wins += 1 if game.white.result == "win" else 0

        else:
            wins += 1 if game.black.result == "win" else 0

    percentage = round(wins/len(games) * 100, 2)

    return (wins, percentage)

def avg_accuracy(games: list[Game], username: str) -> float:
    if not games:
        return 0

    sum = 0
    count = 0

    for game in games:
        if game.white.accuracy >= 50:
            if(game.white.username == username):
                sum += game.white.accuracy
            else:
                sum += game.black.accuracy

            count += 1

    return round(sum / count, 2)

def parse_opening(opening_url: str) -> str:
    import re
    pattern = r"https://www.chess.com/openings/([^-]+(?:-[^-\d]+)*)"
    match = re.search(pattern, opening_url)
    
    if match:
        return match.group(1).replace('-', ' ')

    return opening_url
