from flask import Blueprint, jsonify, request, make_response
import db_utils
from db_utils import *
from schemas import *
from models import *
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = CreateUsers().load(request.json)
        if len(user_data) < 5:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response
        user = db_utils.create_entry(User, **user_data)

        if user == None:
            response = make_response("Uncorrect data")
            response.status_code = 405
            return response

        response = make_response(jsonify(CreateUsers().dump(user)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id:int):
    try:
        user = db_utils.get_entry_by_id(User, id)
        if user == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetUsers().dump(user)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id:int):
    try:
        user_data = GetUsers().load(request.json)
        if len(user_data) == 0:
            response = make_response(jsonify("Nothing changed"))
            response.status_code = 200
            return response

        if 'role' in user_data.keys():
            if user_data['role'] not in ('user', 'superuser'):
                response = make_response(jsonify("Role not valid value, must be user or superuser"))
                response.status_code = 405
                return response

        user = db_utils.update_entry(User, id, **user_data)
        if user == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetUsers().dump(user)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id:int):
    user = db_utils.delete_entry_by_id(User, id)
    if user == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetUsers().dump(user)))
    response.status_code = 200
    return response

@api_blueprint.route('/users/login', methods=['GET'])
def user_login():
    pass

@api_blueprint.route('/songs', methods=['POST'])
def create_song():
    try:
        song_data = CreateSong().load(request.json)
        if len(song_data) < 5:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response
        if 'rating' in song_data.keys():
            if song_data['rating'] not in ('1', '2', '3', '4', '5'):
                response = make_response(jsonify("Role not valid value, must be one of: 1, 2, 3, 4, 5"))
                response.status_code = 405
                return response

        song = db_utils.create_song(category_id_=song_data['category_id'], **song_data)
        if song == None:
            response = make_response(jsonify("Uncorrect data"))
            response.status_code = 405
            return response

        if song == 405:
            response = make_response(jsonify("Unknown category"))
            response.status_code = 405
            return response

        response = make_response(jsonify(CreateSong().dump(song)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/songs', methods=['GET'])
def get_songs():
    songs = db_utils.get_entry(Song)
    response = make_response(jsonify(GetSongs(many=True).dump(songs)))
    response.status_code = 200
    return response

@api_blueprint.route('/songs/<song_title>', methods=['GET'])
def get_songs_title(song_title):
    try:
        songs = db_utils.get_songs_by_name(Song, song_title)
        response = make_response(jsonify(GetSongs(many=True).dump(songs)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/songs/<int:id>', methods=['GET'])
def get_songs_id(id:int):
    try:
        song = db_utils.get_entry_by_id(Song, id)
        if song == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetSongs().dump(song)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/songs/<int:id>', methods=['PUT'])
def update_songs(id:int):
    try:
        song_data = GetSongs().load(request.json)
        if 'rating' in song_data.keys():
            if song_data['rating'] not in ('1', '2', '3', '4', '5'):
                response = make_response(jsonify("Role not valid value, must be one of: 1, 2, 3, 4, 5"))
                response.status_code = 405
                return response

        song = db_utils.update_entry(Song, id, **song_data)
        if song == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetUsers().dump(song)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/songs/<int:id>', methods=['DELETE'])
def delete_songs(id:int):
    song = db_utils.delete_entry_by_id(Song, id)
    if song == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetUsers().dump(song)))
    response.status_code = 200
    return response

@api_blueprint.route('/artists', methods=['POST'])
def create_artist():
    try:
        artist_data = CreateArtist().load(request.json)
        if len(artist_data) < 3:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response

        if 'rating' in artist_data.keys():
            if artist_data['rating'] not in ('1', '2', '3', '4', '5'):
                response = make_response(jsonify("Role not valid value, must be one of: 1, 2, 3, 4, 5"))
                response.status_code = 405
                return response

        artist = db_utils.create_entry(Artist, **artist_data)

        if artist == None:
            response = make_response("Uncorrect data")
            response.status_code = 405
            return response

        response = make_response(jsonify(CreateArtist().dump(artist)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/artists', methods=['GET'])
def get_all_artists():
    artists = db_utils.get_entry(Song)
    response = make_response(jsonify(GetArtists(many=True).dump(artists)))
    response.status_code = 200
    return response

@api_blueprint.route('/artists/<first_name>/<last_name>', methods=['GET'])
def get_artist(first_name, last_name):
    try:
        artists = db_utils.get_artists_by_name(first_name, last_name)
        response = make_response(jsonify(GetArtists(many=True).dump(artists)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/artists/<int:id>', methods=['GET'])
def get_artist_id(id:int):
    try:
        artist = db_utils.get_entry_by_id(Artist, id)
        if artist == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetArtists().dump(artist)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/artists/<int:id>', methods=['PUT'])
def update_artists(id:int):
    try:
        artist_data = GetSongs().load(request.json)
        if 'rating' in artist_data.keys():
            if artist_data['rating'] not in ('1', '2', '3', '4', '5'):
                response = make_response(jsonify("Role not valid value, must be "))
                response.status_code = 405
                return response

        artist = db_utils.update_entry(Song, id, **artist_data)
        if artist == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetArtists().dump(artist)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/artists/<int:id>', methods=['DELETE'])
def delete_artists(id:int):
    artist = db_utils.delete_entry_by_id(Artist, id)
    if artist == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetUsers().dump(artist)))
    response.status_code = 200
    return response

@api_blueprint.route('/category', methods=['POST'])
def create_category():
    try:
        category_data = CreateCategory().load(request.json)
        if len(category_data) < 1:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response

        category = db_utils.create_entry(Category, **category_data)

        if category == None:
            response = make_response("Uncorrect data")
            response.status_code = 405
            return response

        response = make_response(jsonify(CreateCategory().dump(category)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/category', methods=['GET'])
def get_all_category():
    category = db_utils.get_entry(Category)
    response = make_response(jsonify(GetCategory(many=True).dump(category)))
    response.status_code = 200
    return response

@api_blueprint.route('/category/<category_name>', methods=['GET'])
def get_category_name(category_name):
    try:
        categoryes = db_utils.get_category_by_name(name=category_name)
        response = make_response(jsonify(GetCategory(many=True).dump(categoryes)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/category/<int:id>', methods=['GET'])
def get_category(id:int):
    try:
        category = db_utils.get_entry_by_id(Category, id)
        if category == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetCategory().dump(category)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/category/<int:id>', methods=['PUT'])
def update_category(id:int):
    try:
        category_data = GetCategory().load(request.json)
        category = db_utils.update_entry(Category, id, **category_data)
        if category == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetCategory().dump(category)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id:int):
    category = db_utils.delete_entry_by_id(Category, id)
    if category == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetCategory().dump(category)))
    response.status_code = 200
    return response

@api_blueprint.route('/playlists', methods=['POST'])
def create_playlist():
    try:
        playlist_data = CreatePlaylist().load(request.json)
        if len(playlist_data) < 4:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response

        playlist = db_utils.create_playlist(user_id_=playlist_data['user_id'], artist_id_=playlist_data['artist_id'],
        song_id_=playlist_data['song_id'], **playlist_data)

        if playlist == 405:
            response = make_response(jsonify("Uncorrected fk values"))
            response.status_code = 200
            return response

        response = make_response(jsonify(CreatePlaylist().dump(playlist)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists', methods=['GET'])
def get_all_public_playlist():
    playlists = db_utils.get_entry(Playlist)
    response = make_response(jsonify(GetPlaylist(many=True).dump(playlists)))
    response.status_code = 200
    return response

@api_blueprint.route('/playlists/public/<int:id>', methods=['GET'])
def get_public_playlist(id:int):
    try:
        playlist = db_utils.get_entry_by_id(Playlist, id)
        if playlist == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetPlaylist().dump(playlist)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists/public/<int:id>', methods=['PUT'])
def update_playlist(id:int):
    try:
        playlist_data = GetPlaylist().load(request.json)
        if len(playlist_data) == 1 and 'status' in playlist_data.keys():
            playlist = db_utils.update_entry(Playlist, id, **playlist_data)
            if playlist == 404:
                response = make_response(jsonify("Not found"))
                response.status_code = 404
                return response

            response = make_response(jsonify(GetPlaylist().dump(playlist)))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify("Can`t change fk values"))
            response.status_code = 405
            return response


    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists/public/<int:id>', methods=['DELETE'])
def delete_playlist(id:int):
    playlist = db_utils.delete_entry_by_id(Playlist, id)
    if playlist == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetPlaylist().dump(playlist)))
    response.status_code = 200
    return response

@api_blueprint.route('/playlists/private', methods=['POST'])
def create_private_playlist():
    try:
        playlist_data = CreatePlaylist().load(request.json)
        if len(playlist_data) < 4:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response

        category = db_utils.create_entry(Playlist, **playlist_data)

        if category == None:
            response = make_response("Uncorrect data")
            response.status_code = 405
            return response

        response = make_response(jsonify(CreatePlaylist().dump(category)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists/private', methods=['GET'])
def get_all_private_playlists():
    playlists = db_utils.get_entry(Playlist)
    response = make_response(jsonify(GetPlaylist(many=True).dump(playlists)))
    response.status_code = 200
    return response

@api_blueprint.route('/playlists/private/<int:id>', methods=['GET'])
def get_private_playlist(id:int):
    try:
        playlist = db_utils.get_entry_by_id(Playlist, id)
        if playlist == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetPlaylist(many=True).dump(playlist)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists/private/<int:id>', methods=['PUT'])
def update_private_playlist(iid:int):
    try:
        playlist_data = GetPlaylist().load(request.json)
        if len(playlist_data) == 1 and 'status' in playlist_data.keys():
            playlist = db_utils.update_entry(Playlist, id, **playlist_data)
            if playlist == 404:
                response = make_response(jsonify("Not found"))
                response.status_code = 404
                return response

            response = make_response(jsonify(GetPlaylist().dump(playlist)))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify("Can`t change fk values"))
            response.status_code = 405
            return response


    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/playlists/private/<int:id>', methods=['DELETE'])
def delete_private_playlist(id:int):
    playlist = db_utils.delete_entry_by_id(Playlist, id)
    if playlist == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetPlaylist().dump(playlist)))
    response.status_code = 200
    return response

@api_blueprint.route('/albums', methods=['POST'])
def create_album():
    try:
        album_data = CreateAlbum().load(request.json)
        if len(album_data) < 4:
            response = make_response(jsonify("Missing required field"))
            response.status_code = 405
            return response

        album = db_utils.create_entry(Album, **album_data)

        if album == None:
            response = make_response("Uncorrect data")
            response.status_code = 405
            return response

        response = make_response(jsonify(CreateAlbum().dump(album)))
        response.status_code = 200
        return response
    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/albums', methods=['GET'])
def get_all_albums():
    albums = db_utils.get_entry(Album)
    response = make_response(jsonify(GetAlbums(many=True).dump(albums)))
    response.status_code = 200
    return response

@api_blueprint.route('/albums/<int:id>', methods=['GET'])
def get_album(id:int):
    try:
        album = db_utils.get_entry_by_id(Album, id)
        if album == 404:
            response = make_response(jsonify("Not found"))
            response.status_code = 404
            return response

        response = make_response(jsonify(GetAlbums().dump(album)))
        response.status_code = 200
        return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/albums/<int:id>', methods=['PUT'])
def update_album(id:int):
    try:
        album_data = GetAlbums().load(request.json)
        if len(album_data) == 1 and 'name' in album_data.keys():
            album = db_utils.update_entry(Album, id, **album_data)
            if album == 404:
                response = make_response(jsonify("Not found"))
                response.status_code = 404
                return response

            response = make_response(jsonify(GetAlbums().dump(album)))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify("Can`t change fk values"))
            response.status_code = 405
            return response

    except ValidationError as err:
        response = dict({"Uncorrect fields": err.normalized_messages()})
        return response, 400

@api_blueprint.route('/albums/<int:id>', methods=['DELETE'])
def delete_album(id:int):
    album = db_utils.delete_entry_by_id(Album, id)
    if album == 404:
        response = make_response(jsonify("Not found"))
        response.status_code = 404
        return response

    response = make_response(jsonify(GetAlbums().dump(album)))
    response.status_code = 200
    return response
