# youtube-spotify-converter

## Welcome to Jaq's YtS converter bot!

This is a tool to convert Youtube playlists into Spotify playlists. This `README.md` is a work-in-progress as this project is still in development. However, working prototypes have been developed and are located on the `main` branch. Please feel free to use this tool and provide feedback!

## Files and Scripts

### extract_spotify_playlist.py

This command-line script can be accessed and executed without any API key requirement and will generate a `JSON` file usable by the `create_spotify_playlist.py` script.

### create_spotify_playlist.py

In order to execute this command-line script, a Spotify API Developer Key is needed for the use of this bot as well as the public Spotify User ID (Username). For help in locating these entities, please refer to [Obtaining a Spotify API Developer key](#obtaining-a-spotify-api-developer-key) and [Locating your Spotify User ID](#locating-your-spotify-user-id).

### colorful_errors.py

A library of custom functions that are used throughout this project. This will hopefully and eventually be transformed into a full Python template library with no to minimal dependencies (name TBA but currently Jaq's Template Library) and will be linked here in the future.

### template.env

An example `.env` file with the required hidden or sensitive environment variables. The following block is a recreation of the file. When running the programs, please rename the file to `.env`.

```
CLIENT_ID = client-id-from-Spotify-API
CLIENT_SECRET = client-secret-from-Spotify-API
FLASK_KEY = custom-key-that-can-be-anything
SPOTIFY_USER_ID = Spotify-public-profile-user-ID
```

### requirements.txt

A standard list of dependencies which can be installed using the following command on terminals:

```
pip install -r requirements.txt
```

## Obtaining a Spotify API Developer key

1. Go to https://developer.spotify.com/ and log into your Spotify account. Navigate to the `Dashboard`.
2. Create an app and fill out the requisite information. While here, add `http://127.0.0.1:5000/redirect` to `Redirect URIs`.
3. Click `Save`, then click your newly created app and navigate to `Settings`.
4. Copy-and-paste your `Client ID` and `Client secret` into your `.env` file (into `CLIENT_ID` and `CLIENT_SECRET` respectively).

For more information, please refer to the [Spotify for Developers Documentation](https://developer.spotify.com/).

## Locating your Spotify User ID

1. Go to https://www.spotify.com/account/profile/ and log into your Spotfy account.
2. Find `Username` and copy the string underneath the header.
3. Paste the username into your `.env` flie (into `SPOTIFY_USER_ID` specifically).