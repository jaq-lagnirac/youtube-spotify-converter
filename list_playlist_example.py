# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Elapsed time
from time import time

# Youtube Library
import pytube

# Multithreading Libraries
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

url = 'https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ'

playlist = pytube.Playlist(url)
    
def extract_info(video):
    info_dict = {
        'title' : video.title,
        'author' : video.author
    }
    return info_dict

start = time()
    
print(f'Playlist: {playlist.title}')

processes = []
errors = []
with ThreadPoolExecutor(max_workers = multiprocessing.cpu_count()) as executor:
    for video in playlist.videos:
        try:
            processes.append(executor.submit(extract_info, video))
            print(f'Title: {video.title} - Author: {video.author}')
        except:
            print(f'-----Error with {video.url}-----')
            errors.append(video)

videos_info = []
for task in as_completed(processes):
    videos_info.append(task.result())
    print(task.result())

elapsed = time() - start
print(f'Elapsed time {elapsed : .2f} secs')
print(f'No. of Vidoes: {len(videos_info)}')
    
for error in errors:
    print(error)