from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql://root:1234@localhost:3306/playlist-service', echo=False)
SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    login = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    role = Column(Enum("USER", "SUPERUSER"), default='USER', nullable=False)


class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    raiting = Column(Enum("1", "2", "3", "4", "5"), nullable=False)


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

    id  = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(255), nullable=False)
    lyrics = Column(String(10000), nullable=False)
    raiting = Column(Enum("1", "2", "3", "4", "5"), nullable=False)
    duration = Column(Float(2), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, primary_key=True)

class Album(Base):
    __tablename__ = "album"

    id  = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(255), nullable=False)
    released = Column(DATETIME, nullable=False)
    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False, primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, primary_key=True)


Base.metadata.create_all(engine)