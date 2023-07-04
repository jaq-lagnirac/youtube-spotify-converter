# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Standard Python Libraries
import os
import sys
import argparse
import logging
from time import time, sleep

# Youtube Library
import pytube

# Regular expressions
import re

url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'

playlist = pytube.Playlist(url)

def extract_info(video):
    # cleans input
    title = (video.title).lower()
    author = (video.author).lower()
    title.replace('official', '')
    title.replace('lyric', '')
    title.replace('audio', '')
    title.replace('video', '')
    title.replace('animated', '')

    re.sub('\(\s*\)', '', title)

    # assembles info into a dict
    info_dict = {
        'title' : title,
        'author' : author
    }
    return info_dict

start_time = time()

# Extracts video title and author from Youtube playlist
videos_info = []
print(f'Extracting video info from playlist - {playlist.title}')
sleep(3)
for video in playlist.videos:
    try:
        video.check_availability()
        print(f'Extracting:\tTitle: {video.title}\n\t\tAuthor: {video.author}')
        videos_info.append(extract_info(video))
    except Exception as e:
        print(f'Exception occured:\t{e}\n\t\tMessage: {e.message}')
        continue

extraction_chkpt = time()
extraction_elapsed = extraction_chkpt - start_time
print(f'Extraction complete.')
print(f'Videos extracted: {len(videos_info)}')
print(f'Extraction elapsed time: {extraction_elapsed : .3f} secs')
sleep(3)

print('Removing duplicates.')
sleep(3)
begin_set_chkpt = time()

# Removes duplicate extracted info (turns info list into a set)
info_set = []
[info_set.append(x) for x in videos_info if x not in info_set]

set_chkpt = time()
set_elapsed = set_chkpt - begin_set_chkpt
duplicates_removed = len(info_set) - len(videos_info)
if duplicates_removed == 1:
    print('Removed 1 duplicate.')
else:
    print(f'Removed {duplicates_removed} duplicates.')
print(f'Unique videos: {len(info_set)}')
print(f'Removal elapsed time: {set_elapsed : .3f} secs')

for info in info_set:
    print(info)
