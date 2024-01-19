# Justin Caringal
# Based off code from the repo below:
# https://github.com/musikalkemist/spotifyplaylistgenerator

class Track:
    '''Represents individual piece on Spotiy'''

    def __init__(self, name, id, artist):
        self.name = name # name of track
        self.id = id # track ID
        self.artist = artist # artist/creator of track

    def create_spotify_url(self):
        return f'spotify:track:{self.id}'
    
    def __str__(self):
        return f'{self.name} by {self.artist}'