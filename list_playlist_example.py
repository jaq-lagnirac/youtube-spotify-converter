# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Youtube Library
import pytube

url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'

playlist = pytube.Playlist(url)

print(f'Playlist - {playlist.title}')
for video in playlist.videos:
    print(f'Title: {video.title} Author: {video.author}')