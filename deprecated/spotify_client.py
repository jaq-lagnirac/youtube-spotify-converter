# Justin Caringal
# Based off code from the repo below:
# https://github.com/musikalkemist/spotifyplaylistgenerator

import json
import requests
from track import Track
from playlist import Playlist

class SpotifyClient:
    '''performs i/o ops using Spotify API'''

    def __init__(self, auth_token, user_id):
        self.auth_token = auth_token
        self.user_id = user_id

    def create_playlist(self, name, description):
        data = json.dumps({
            'name' : name,
            'description' : description,
            'public' : True
        })
        url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'
        response = self.place_post_api_request(url, data)
        response_json = response.json()

        playlist_id = response_json['id']
        playlist = Playlist(name, playlist_id)
        return playlist
    
    def place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data = data,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : f'Bearer {self.auth_token}'
            }
        )

    def populate_playlist(self, playlist, tracks):
        tracks_urls = [track.create_spotify_url() for track in tracks]
        data = json.dumps(tracks_urls)
        url = f'https://api.spotify.com/v1/playlists/{playlist.id}/tracks'
        response = self.place_post_api_request(url, data)
        response_json = response.json()
        return response_json