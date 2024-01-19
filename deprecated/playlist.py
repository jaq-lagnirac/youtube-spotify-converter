# Justin Caringal
# Based off code from the repo below:
# https://github.com/musikalkemist/spotifyplaylistgenerator

class Playlist:
    '''Represents Spotify playlist'''

    def __init__(self, name, id):
        self.name = name # name of playlist
        self.id = id # playlist id

    def __str__(self):
        return f'Playlist: {self.name}'