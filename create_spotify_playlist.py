# Justin Caringal
# Accesses the Spotify API

# this SEEMS like a good video --> https://www.youtube.com/watch?v=mBycigbJQzA
# connected github --> https://github.com/katiagilligan888/Spotify-Discover-Weekly/blob/main/discoverWeekly.py

import os
import json
from time import time
import spotipy # streamlines access to Spotify API
from spotipy.oauth2 import SpotifyOAuth # authenticates permissions

# sets up command line arguments
import argparse
DESCRIPTION = '''
'''
EPILOG = '''
'''

# initialized with dummy variables for scope resolution
URL = None
JSON = None
MAX_REPEAT_QUERIES = None

# custom libraries
from colorful_errors import error_exit, red, green, cyan
from extract_youtube_playlist import get_playlist, \
    process_playlist, process_playlist_multithreaded

# loads in private .env variables
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
FLASK_KEY = os.getenv('FLASK_KEY')
SPOTIFY_USER_ID = os.getenv('SPOTIFY_USER_ID')

# configures Flask app
from flask import Flask, request, url_for, session, redirect # accesses HTTP requests
app = Flask(__name__) # initializes Flask app
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie' # set name of session cookie
app.secret_key = FLASK_KEY # sets random key to sign cookie
TOKEN_INFO = 'token_info' # sets key for token info in session dict

VALID_PLAYLIST_URL = 'youtube.com/playlist?'
REQUIRED_KEYS = {'playlist_title', 'videos_info', 'errors'}


###
# FLASK APP RUNNING
###


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

    ### AUTH BOILERPLATE
    try: 
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])


    ### PLAYLIST CONVERSION

    # EXTRACTION
    # extracts dict based on user input
    playlist_dict = None
    if URL:
        # checks URL to see if valid
        if VALID_PLAYLIST_URL not in URL:
            print(red('URL not valid.'))
            return 'URL not valid.'
        
        # extracts playlist into dict
        print(cyan('Extracting from URL.'))
        playlist_dict = url_extraction(URL)

    elif JSON:
        # checks JSON path to see if valid
        _, extension = os.path.splitext(JSON)
        if extension.lower() != '.json':
            print(red('JSON path not valid.'))
            return 'JSON path not valid.'

        # extracts playlist into dict
        print(cyan('Extracting from JSON.'))
        playlist_dict = json_extraction(JSON)

    else:
        print(red('URL or JSON path not included.'))
        return 'URL or JSON path not included.'
    
    playlist_title = playlist_dict['playlist_title']
    extracted_songs = playlist_dict['videos_info']

    print(f'Extraction complete. Extracted {green(len(extracted_songs))} songs.')

    # checks to see if playlist already exists in current users playlists,
    # exits program to prevent override and unwanted appends
    current_playlists =  sp.current_user_playlists()['items']
    for playlist in current_playlists:
        if(playlist['name'] == playlist_title):
            print(f'Playlist \"{cyan(playlist_title)}\" already exists.')
            return f'Playlist \"{playlist_title}\" already exists.'

    print(cyan('Initiating Spotify API track queries.'))

    # QUERYING
    # iterates through video info to creacte search queries to Spotify API
    # URI - resource identifiers for objects in Spotify
    track_uris = []
    successful_queries = [] # not currently interacted with
    queries_not_found = []
    for song in extracted_songs:
        # creates query and executes API call
        search_query = f"{song['title']} {song['author']}"
        print(f'Querying: {cyan(search_query)}', end=' - Status - ')
        for attempt in range(1, MAX_REPEAT_QUERIES + 1):
            search_result = sp.search(search_query,
                                    limit=1,
                                    offset=0,
                                    type='track')
            
            print(f'Attempt {attempt}: ', end='')

            # examines search result, Exception created when bad result received
            # i.e. a query failed to return a even a single track
            try: # query successful
                track_uri = search_result['tracks']['items'][0]['uri']
                track_uris.append(track_uri)
                successful_queries.append(search_query)
                print(green('Success.'), end='')
                break
            except: # query not successful (list index out of range)
                queries_not_found.append(search_query)
                print(red('Failed.'), end='')
        print('') # prints newline

    not_found = len(extracted_songs) - len(track_uris)
    print(f'Track queries complete. {green(len(track_uris))} successes, {red(not_found)} failures.')

    # generates err file of unsuccessful queries if not_found > 0
    # i.e. if there ends up being a track that is not found
    if not_found:
        json_name, _ = os.path.splitext(JSON)
        err_name = f'NOTFOUND_{json_name}.err'
        with open(err_name, 'w') as errfile:
            print(f'Writing unsuccessful queries to {red(err_name)}')
            queries_not_found = list(set(queries_not_found)) # removes duplicates
            for query in queries_not_found:
                errfile.write(f'{query}\n')
    
    # removes duplicates while preserving order using list comprehension
    print(cyan('Removing duplicates.'))
    trimmed_uris = []
    [trimmed_uris.append(uri) for uri in track_uris if uri not in trimmed_uris]
    tracks_removed = len(track_uris) - len(trimmed_uris)
    print(f'{red(tracks_removed)} tracks removed. New length: {green(len(trimmed_uris))}')

    # creates playlist and extracts ID
    print(f'Creating playlist {cyan(playlist_title)}')
    sp.user_playlist_create(user=SPOTIFY_USER_ID,
                            name=playlist_title,
                            public=True,
                            collaborative=False,
                            description='This playlist was created by Jaq\'s YtS bot.')
    # finds new playlist created and extracts playlist ID
    current_playlists =  sp.current_user_playlists()['items']
    new_playlist_id = None
    for playlist in current_playlists:
        if(playlist['name'] == playlist_title):
            new_playlist_id = playlist['id']
            print(cyan(f'Successfully created and identified playlist.'))
            break
    
    # breaks up playlist appends to API to prevent overwhelming API
    size_of_sublist = 25
    for index in range(size_of_sublist,
                       len(trimmed_uris) + size_of_sublist,
                       size_of_sublist):
        start = index - size_of_sublist
        sublist_of_uris = trimmed_uris[start : index]
        sp.user_playlist_add_tracks(SPOTIFY_USER_ID,
                                    new_playlist_id,
                                    sublist_of_uris,
                                    None)
    
    end_str = f'Playlist {playlist_title} successfully created and populated! Thank you for using Jaq\'s YtS converter!'
    print(green(end_str))
    return end_str


# function to get the token info from the session
def get_token():
    """getter for token info
    
    A function which gets the token info from the session
    
    Returns:
        The token info to connect Flask and the Spotify API
    
    """
    
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
    """authenticates Spotify API
    
    Returns:
        SpotifyOAuth: A successful OAuth
        
    """
    
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )


def url_extraction(url):
    """Conducts URL extraction
    
    A function which performs full playlist URL extraction
    to use later

    Args:
        url (str): A URL to a YouTube playlist

    Returns:
        dict: A dictionary of a playlist and its videos

    
    """

    # gets playlist from URL
    playlist = get_playlist(url)

    # generates dictionary from playlist object
    if args.performance:
        print(cyan('Performance mode enabled. Playlist order will not be maintained.'))
        playlist_dict = process_playlist_multithreaded(playlist)
    else:
        print(cyan('Deep-copy extraction enabled. Playlist order will be maintained.'))
        playlist_dict = process_playlist(playlist)

    return playlist_dict


def json_extraction(json_path):
    """Conducts JSON extraction

    A function which uses a previously generated playlist JSON
    to use later

    Args:
        json_path (str): A relative path to a JSON file

    Returns:
        dict: A dictionary of a playlist and its videos

    """

    # checks existence of file
    if not os.path.exists(json_path):
        print(red(f'{json_path} does not exist.'))
        return None
    
    # opens JSON, populates dict
    with open(json_path, 'r') as infile:
        playlist_dict = json.load(infile)

    # checks to make sure dict keys are valid
    dict_keys = set(playlist_dict.keys())
    if dict_keys != REQUIRED_KEYS:
        error_exit('Dictionary keys do not align.')
    
    return playlist_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument('-u', '--url', help='YouTube playlist URL')
    parser.add_argument('-j', '--json', help='Relative JSON path')
    parser.add_argument('-m',
                        '--max-repeats',
                        default=3,
                        type=int,
                        help='Maximum times to allow failed query.')
    parser.add_argument('-p',
                        '--performance',
                        action='store_true',
                        help='Enables performance mode. Does not maintain playlist order.')
    args = parser.parse_args()
    URL = args.url
    JSON = args.json
    MAX_REPEAT_QUERIES = args.max_repeats

    if not URL and not JSON:
        error_exit('URL or JSON path not included.')
    app.run(debug=True)