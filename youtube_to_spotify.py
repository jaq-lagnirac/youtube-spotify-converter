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

def extract_info(video):
    info_dict = {
        'title' : video.title,
        'author' : video.author
    }
    return info_dict

start = time()

videos_info = []
print(f'Playlist - {playlist.title}')
for video in playlist.videos:
    try:
        video.check_availability()
        print(f'Extracting:\tTitle: {video.title}\n\t\tAuthor: {video.author}')
        videos_info.append(extract_info(video))
    except Exception as e:
        print(f'Exception occured:\t{e}\n\t\tMessage: {e.message}')
        continue

elapsed = time() - start
print(f'Elapsed: {elapsed : .2f} secs')

for info in videos_info:
    print(info)
