from marshmallow import Schema, fields, validate
from flask_bcrypt import Bcrypt, generate_password_hash
from marshmallow import ValidationError
from json import *

class Users(Schema):
    first_name = fields.String()
    last_name = fields.String()
    username = fields.String()
    login = fields.String(validate=validate.Email())
    password = fields.String()
    role = fields.String(validate = validate.OneOf(['user', 'superuser']))
class Artists(Schema):
    artist_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    rating = fields.Integer(validate = validate.OneOf([1, 2, 3, 4, 5]))
class Categorys(Schema):
    schema_id = fields.Integer()
    name = fields.Integer()
class Songs(Schema):
    song_id = fields.Integer()
    category = fields.Nested(Categorys)
    title = fields.String()
    description = fields.String()
    lyrics = fields.String()
    rating = fields.Integer(validate = validate.OneOf([1, 2, 3, 4, 5]))
    duration = fields.Float()
class Albums(Schema):
    album_id = fields.Integer()
    album_name = fields.String()
    released = fields.Date()
    artist = fields.Nested(Artists)
    song = fields.Nested(Songs)
class Playlists(Schema):
    playlist_id = fields.Integer()
    user = fields.Nested(Users)
    artist = fields.Nested(Artists)
    song = fields.Nested(Songs)
    status =  fields.String(validate = validate.OneOf(['private', 'public']))

class CreateUsers(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String( required=True)
    username = fields.String(required = True)
    login = fields.String(required=True)
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True, required=True
    )
    role = fields.String(validate = validate.OneOf(['user', 'superuser']), required = True)

class CreateSong(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    lyrics = fields.String(required=True)
    rating = fields.String(validate=validate.OneOf(['1', '2', '3', '4', '5']), required=True)
    duration = fields.Float(required=True)
    category_id = fields.Integer(required=True)

class CreateArtist(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    rating = fields.String(validate=validate.OneOf(['1', '2', '3', '4', '5']), required=True)

class CreateCategory(Schema):
    name = fields.String()

class CreatePlaylist(Schema):
    user_id = fields.Integer(required=True)
    artist_id = fields.Integer(required=True)
    song_id = fields.Integer(required=True)
    status = fields.String(validate = validate.OneOf(['private', 'public']))

class CreateAlbum(Schema):
    name = fields.String(required=True)
    released = fields.DateTime(required=True)
    artist_id = fields.Integer(required=True)
    song_id = fields.Integer(required=True)

class GetUsers(Schema):
    first_name = fields.String()
    last_name = fields.String()
    username = fields.String()
    login = fields.String()
    password = fields.String()
    role = fields.String()

class GetArtists(Schema):
    first_name = fields.String()
    last_name = fields.String()
    rating = fields.String()

class GetCategory(Schema):
    name = fields.String()

class GetSongs(Schema):
    title = fields.String()
    description = fields.String()
    lyrics = fields.String()
    rating = fields.String()
    duration = fields.Float()
    category_id = fields.Integer()

class GetAlbums(Schema):
    name = fields.String()
    released = fields.DateTime()
    artist_id = fields.Integer()
    song_id = fields.Integer()

class GetPlaylist(Schema):
    user_id = fields.Integer()
    artist_id = fields.Integer()
    song_id = fields.Integer()
    status = fields.String()
