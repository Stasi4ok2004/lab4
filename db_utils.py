import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import *
from schemas import *

def create_entry(model ,*, commit=True, **kwargs):
    session = Session()
    entry = model(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    res = session.query(model).filter_by(**kwargs).all()

    return res[-1]

def update_entry(model, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404

    session.execute(update(model).where(model.id == id).values(**kwargs))
    if commit:
        session.commit()
    return get_entry_by_id(model, id, **kwargs)
def get_entry_by_id(model, id, *,commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404
    return session.query(model).filter_by(id=id).one()
def get_entry(model):
    session = Session()
    return session.query(model).all()
def delete_entry_by_id(model, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404
    session.query(model).filter_by(id=id).delete()
    if commit:
        session.commit()

def get_songs_by_name(model, name, *, commit=True, **kwargs):
    session = Session()
    return session.query(model).filter_by(title=name).all()

def get_artists_by_name(first_name, last_name, *, commit=True, **kwargs):
    session = Session()
    return session.query(Artist).filter_by(first_name=first_name, last_name=last_name).all()
def get_category_by_name(name, *, commit=True, **kwargs):
    session = Session()
    return session.query(Category).filter_by(name=name).all()
def get_album_by_name(name, *, commit=True, **kwargs):
    session = Session()
    return session.query(Album).filter_by(name=name).all()
def get_album_by_artist(name, *, commit=True, **kwargs):
    session = Session()
    return session.query(Album).filter_by(name=name).all()

def create_song(category_id_, *, commit=True, **kwargs):
    session = Session()
    if session.query(Category).filter_by(id=category_id_).all() == []:
        return 405
    new_song = Song(**kwargs)
    session.add(new_song)
    if commit:
        session.commit()
    return session.query(Song).filter_by(**kwargs).all()

def create_playlist(user_id_, artist_id_, song_id_, *, commit=True, **kwargs):
    session = Session()
    if session.query(User).filter_by(id=user_id_).all() == []:
        return 405
    if session.query(Artist).filter_by(id=artist_id_).all() == []:
        return 405
    if session.query(Song).filter_by(id=song_id_).all() == []:
        return 405
    entry = Playlist(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    res = session.query(Playlist).filter_by(**kwargs).all()

    return res[-1]
