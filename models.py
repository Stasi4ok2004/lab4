
{

    "title": "Wham! - Last Christmas I gave you my heart",
    "description": "lorem ipsum...",
    "lyrics": "Last Christmas I gave you my heart...",
    "rating": 1,
    "duration": 3.43,
    "category_id": 1
}

import enum
import datetime
import alembic
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import *

engine = create_engine("mysql://root:root@localhost:5900/playlists")
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    login = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum("user", "superuser"), default='user', nullable=False)


class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    rating = Column(Enum("1", "2", "3", "4", "5"), nullable=False)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(45), nullable=False)

class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key = True, autoincrement = True)
    status = Column(Enum("PRIVATE", "PUBLIC"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False, primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, primary_key=True)

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    lyrics = Column(String(10000), nullable=False)
    rating = Column(Enum("1", "2", "3", "4", "5"), nullable=False)
    duration = Column(Float(2), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, primary_key=True)

class Album(Base):
    __tablename__ = "album"

    id  = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(255), nullable=False)
    released = Column(DATETIME, nullable=False)
    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False, primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, primary_key=True)


#Base.metadata.create_all(engine)