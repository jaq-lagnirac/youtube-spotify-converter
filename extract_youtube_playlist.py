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
    
    Args:
        playlist (Playlist): A pytube Playlist object

    Returns:
        dict: A dictionary containing the relevant playlist information
            
    """

    print(f'Playlist: {playlist.title}')
    
    videos_info = []
    errors = []
    for video in playlist.videos:
        try:
            print(f'Title: {video.title} - Author: {video.author}')
            video_dict = extract_video_info(video)
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
    using a ThreadPool. DOES NOT MAINTAIN ORDER OF THE INPUTTED
    PLAYLIST
    
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
        'videos_info' : videos_info,
        'errors' : errors
    }

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
    if args.performance:
        print(cyan('Performance mode enabled. Playlist order will not be maintained.'))
        playlist_dict = process_playlist_multithreaded(playlist)
    else:
        print(cyan('Deep-copy extraction enabled. Playlist order will be maintained.'))
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
    
    print(green(f'Extraction complete, data saved in {json_name}.json'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument('url',
                        nargs='?',
                        help='Youtube playlist URL')
    parser.add_argument('-p',
                        '--performance',
                        action='store_true',
                        help='Enables performance mode. Does not maintain playlist order.')
    args = parser.parse_args()
    main()