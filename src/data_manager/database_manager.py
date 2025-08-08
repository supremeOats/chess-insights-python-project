from .models import db, Profile, Game, Archive
from datetime import date

def load_profile_from_db(username: str) -> Profile | None:
    """Retrun Profile object from database. If player not in DB return None object."""
    player = Profile.query.filter_by(username=username).first()
    return player

def load_archive_from_db(username: str, year: int, month: int) -> ...:
    """Retrun Archive object from database. If archive not in DB return None object."""
    
    archive_date = date(year, month, 1)
    archive = Archive.query.filter_by(username=username, period=archive_date).first() 
    return archive

def add_profile(player: Profile):
    """Store player profile to database"""
    db.session.add(player)
    db.session.commit()

def add_archive(archive: Archive) -> None:
    """Store player archive to database"""
    db.session.add(archive)
    db.session.commit()

def clear_cache() -> None:
    ...
