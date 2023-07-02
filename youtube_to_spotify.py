# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Standard Python Libraries
import os
import sys
import argparse
import logging

from time import time

# Youtube Library
import pytube

url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'

playlist = pytube.Playlist(url)

start = time()

print(f'Playlist - {playlist.title}')
for video in playlist.videos:
    print(f'Video - {video.title} - {video.author}')

elapsed = time() - start
print(f'Elapsed: {elapsed : .2f} secs')