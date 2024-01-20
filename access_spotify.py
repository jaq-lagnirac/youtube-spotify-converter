# Justin Caringal
# Accesses the Spotify API

# this SEEMS like a good video --> https://www.youtube.com/watch?v=mBycigbJQzA
# connected github --> https://github.com/katiagilligan888/Spotify-Discover-Weekly/blob/main/discoverWeekly.py

import os
from time import time
import spotipy # streamlines access to Spotify API
from spotipy.oauth2 import SpotifyOAuth # authenticates permissions
from flask import Flask, request, url_for, session, redirect # accesses HTTP requests

# loads in private .env variables
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
FLASK_KEY = os.getenv('FLASK_KEY')


app = Flask(__name__) # initializes Flask app
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie' # set name of session cookie
app.secret_key = FLASK_KEY # sets random key to sign cookie

TOKEN_INFO = 'token_info' # sets key for token info in session dict


# route to handle logging in
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)


# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the convert_youtube_to_spotify route
    return redirect(url_for('convert_youtube_to_spotify',_external=True))


# route to convert a Youtube playlist into a Spotify playlist
@app.route('/YouTubeToSpotify')
def convert_youtube_to_spotify():
    try: 
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))
    
    # check if the token is expired and refresh it if necessary
    now = int(time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )


app.run(debug=True)