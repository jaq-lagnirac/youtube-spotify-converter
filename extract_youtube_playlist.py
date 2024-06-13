# Justin Caringal
# A script to extract a Youtube playlist into
# a text format

import pytube # accesses youtube
import re # clean up names
import json # output extracted information
import argparse

# custom error messaging and text coloring
from colorful_errors import error_exit, red, green, cyan

# Multithreading Libraries
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

DESCRIPTION = '''
'''
EPILOG = '''
'''


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


def extract_video_info(index, video):
    """ Streamlines extraction
    
    A function which breaks down a pytube video object
    into its component parts and returns a populated
    dictionary containing the relevant information

    Args:
        index (int): the index of the object
        video (Video/YouTube): pytube video object
    
    Returns:
        tuple (int, dict): A tuple with the relevant video info
    """

    info_dict = {
        'title' : video.title,
        'author' : video.author
    }
    return (index, info_dict)


def process_playlist(playlist):
    """Organizes playlist extraction
    
    A function to extract video information from a playlist
    
    Args:
        playlist (Playlist): A pytube Playlist object

    Returns:
        dict: A dictionary containing the relevant playlist information
    
    PLEASE NOTE: This function is now deprecated. process_playlist_multithreaded()
    now maintains order of playlist, rendering this function obsolete as it linearly
    searches the playlist in a way that takes exponentially longer. This function
    may be removed in a future commit, but for now remains in the code for posterity.
    """

    print(f'Playlist: {playlist.title}')
    
    videos_info = []
    errors = []
    for video in playlist.videos:
        try:
            print(f'Title: {video.title} - Author: {video.author}')
            _, video_dict = extract_video_info(0, video) # 0 is a dummy value
            videos_info.append(video_dict)
        except:
            print(f'-----Error with {video.url}-----')
            errors.append(video)
    
    playlist_dict = {
        'playlist_title' : playlist.title,
        'videos_info' : videos_info,
        'errors' : errors
    }

    return playlist_dict


def process_playlist_multithreaded(playlist):
    """Organizes playlist extraction with multithreading
    
    A function to extract video information from a playlist
    using a ThreadPool. NOW MAINTAINS THE ORDER OF THE PLAYLIST
    
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
        for index, video in enumerate(playlist.videos):
        # stores index along with video object to allow for sorting down the line
            try:
                processes.append(executor.submit(extract_video_info, index, video))
                #print(f'Title: {video.title} - Author: {video.author}')
            except:
                print(f'-----Error with {video.url}-----')
                errors.append(video)

    # adds completed tasks to a list
    videos_info = []
    for task in as_completed(processes):
        videos_info.append(task.result())
    
    playlist_dict = {
        'playlist_title' : playlist.title,
        'videos_info' : list(dict(sorted(videos_info)).values()),
        'errors' : errors
    }

    ### Explaining the nifty little one-liner "list(dict(sorted(videos_info)).values())":
    #
    # videos_info is a list of tuples that cotains (int/index, dict/info-for-video).
    # the list is sorted by index using sorted() with a supposed O(n*log(n)) (on par with
    # quicksort) then converted to a dict (one can convert [(key, value), (key, value),...]
    # to a dictionary). The values/individual-video-info is then extracted from the dict,
    # then converted to a list in order to send off into the JSON file or accompanying program

    return playlist_dict


def main():
    """Main function"""
    
    # https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ

    VALID_PLAYLIST_URL = 'youtube.com/playlist?'
    
    url = args.url

    if not url: # if no URL is included with argparse
        url = input(green('Copy-paste a Youtube playlist URL here: '))

    while VALID_PLAYLIST_URL not in url:
        print(red(f'Invalid YouTube Playlist URL (Must contain {VALID_PLAYLIST_URL})'))
        url = input('Try again: ')
    
    print(cyan('Valid URL inputted.'))

    # gets playlist from URL
    playlist = get_playlist(url)

    # generates dictionary from playlist object
    print(cyan('Generating playlist dictionary.'))
    playlist_dict = process_playlist_multithreaded(playlist)

    # trims name to create JSON file
    json_name = playlist_dict['playlist_title']
    json_name = re.sub('[^0-9a-zA-Z ]+', '', json_name)
    json_name = json_name.replace(' ', '_')

    # dumps info into JSON file output
    with open(f'{json_name}.json', 'w') as outfile:
        outfile.write(json.dumps(playlist_dict,
                                 ensure_ascii=False,
                                 indent=4))
    
    print(green(f'Extraction complete, data saved in {json_name}.json'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument('url',
                        nargs='?',
                        help='Youtube playlist URL')
    args = parser.parse_args()
    main()


    # playlist = pytube.Playlist("https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ")
    # print(process_playlist_multithreaded(playlist))

    # from time import time
    # start = time()
    # playlist = pytube.Playlist("https://www.youtube.com/playlist?list=PLvaO_paR56p-SNDvQNboq2BXniEfxj8gQ")
    # end = time()
    # elapsed = end - start
    # print(f'extraction: {elapsed:2f}')
    
    # start = time()
    # dict = {}
    # for index, video in enumerate(playlist.videos):
    #     dict[index] = video
    # end = time()
    # elapsed = end - start
    # print(f'conversion: {elapsed:2f}')
    
    # start = time()
    # print(playlist)
    # end = time()
    # elapsed = end - start
    # print(f'printing list: {elapsed:2f}')

    # start = time()
    # print(dict)
    # end = time()
    # elapsed = end - start
    # print(f'printing dict: {elapsed:2f}')