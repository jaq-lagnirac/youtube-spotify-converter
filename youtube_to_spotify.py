# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Standard Python Libraries
import os
import sys
import argparse
import logging

# Youtube Library
import pytube

url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'

playlist = pytube.Playlist(url)

print(f'Playlist - {playlist.title}')
for video in playlist.videos:
    print(f'Video - {video.title} - {video.author}')