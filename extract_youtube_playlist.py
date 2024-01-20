# Justin Caringal
# A script to extract a Youtube playlist into
# a text format

import pytube # accesses youtube
import re # clean up names
import json # output extracted information

# custom error messaging and text coloring
from colorful_errors import error_exit, red, green

# Multithreading Libraries
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def get_playlist(url):
    """ Organizes user input
    
    A function which prompts the user for a YouTube
    playlist URL and returns a pytube playlist object

    Args:
        url (str): a URL for a Youtube playlist
    
    Returns:
        Playlist: returns a pytube playlist object
    
    """

    try:
        playlist = pytube.Playlist(url)
    except:
        error_exit(f'Unable to generate pytube Playlist object from {url}')
    
    return playlist


def extract_video_info(video):
    """ Streamlines extraction
    
    A function which breaks down a pytube video object
    into its component parts and returns a populated
    dictionary containing the relevant information

    Args:
        video (Video): pytube video object
    
    Returns:
        dict: A dictionary with the relevant video info
    """

    info_dict = {
        'title' : video.title,
        'author' : video.author
    }
    return info_dict


def process_playlist(playlist):
    """Organizes playlist extraction
    
    A function to extract video information from a playlist
    using a ThreadPool
    
    Args:
        playlist (Playlist): A pytube Playlist object

    Returns:
        dict: A dictionary containing the relevant playlist information
            
    """

    print(f'Playlist: {playlist.title}')

    # processes tasks using ThreadPoolExecutor
    processes = []
    errors = []
    with ThreadPoolExecutor(max_workers = multiprocessing.cpu_count()) as executor:
        for video in playlist.videos:
            try:
                processes.append(executor.submit(extract_video_info, video))
                print(f'Title: {video.title} - Author: {video.author}')
            except:
                print(f'-----Error with {video.url}-----')
                errors.append(video)

    # adds completed tasks to a list
    videos_info = []
    for task in as_completed(processes):
        videos_info.append(task.result())
    
    playlist_dict = {
        'playlist_title' : playlist.title,
        'videos_info' : videos_info,
        'errors' : errors
    }

    return playlist_dict


def main():
    """Main function"""
    
    # https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ

    VALID_PLAYLIST_URL = 'youtube.com/playlist?'
    url = input(green('Copy-paste a Youtube Playlist URL here: '))

    while VALID_PLAYLIST_URL not in url:
        print(red(f'Invalid YouTube Playlist URL (Must contain {VALID_PLAYLIST_URL})'))
        url = input('Try again: ')
    
    print('Valid URL inputted.')

    # gets playlist from URL
    playlist = get_playlist(url)

    # generates dictionary from playlist object
    playlist_dict = process_playlist(playlist)

    # trims name to create JSON file
    json_name = playlist_dict['playlist_title']
    json_name = re.sub('[^0-9a-zA-Z ]+', '', json_name)
    json_name = json_name.replace(' ', '_')

    # dumps info into JSON file output
    with open(f'{json_name}.json', 'w') as outfile:
        outfile.write(json.dumps(playlist_dict,
                                 ensure_ascii=False,
                                 indent=4))


if __name__ == '__main__':
    main()