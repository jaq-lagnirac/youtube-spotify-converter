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

# URL to be extracted
url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'
# pytube playlist object called from URL
playlist = pytube.Playlist(url)
# name of checkpoint file
filename = 'extracted_videos_checkpoint.txt'


# functions


def extract_info(video):
    # cleans input
    title = (video.title).lower()
    author = (video.author).lower()
    title.replace('official', '')
    title.replace('lyric', '')
    title.replace('audio', '')
    title.replace('video', '')
    title.replace('animated', '')

    # removes parentheses and anything inside of it
    re.sub('\(\s*\)', '', title)

    # assembles info into a dict
    info_dict = {
        'title' : title,
        'author' : author
    }
    return info_dict


# Start of main body

start_time = time()

# creates checkpoint file (dummy, incomplete)
with open(filename, 'w') as file:
    file.write(f'Playlist: {playlist.title}\n')

# Extracts video title and author from Youtube playlist
videos_info = [] # list of dicts
print(f'Extracting video info from playlist - {playlist.title}')
sleep(3)
for video in playlist.videos:
    try:
        video.check_availability() # throws exception(s) if video unavailable
        print(f'Extracting:\tTitle: {video.title}\n\t\tAuthor: {video.author}')
        videos_info.append(extract_info(video)) # adds dict to end of list
        
        # appends extracted video info to checkpoint file (in case of failure)
        with open(filename, 'a') as file:
            file.write(f'{video.title} {video.author}\n')
    except Exception as e:
        print(f'Exception occured:\t{e}\n\t\tMessage: {e.message}')
        continue # continues executing and extracting

# print extraction diagnostics
extraction_chkpt = time()
extraction_elapsed = extraction_chkpt - start_time
print(f'Extraction complete.')
print(f'Videos extracted: {len(videos_info)}')
print(f'Extraction elapsed time: {extraction_elapsed : .3f} secs')
sleep(3)

# begin set-ification
print('Removing duplicates.')
sleep(3)
begin_set_chkpt = time()

# Removes duplicate extracted info (turns info list into a set)
info_set = []
[info_set.append(x) for x in videos_info if x not in info_set]

# print set diagnostics
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
