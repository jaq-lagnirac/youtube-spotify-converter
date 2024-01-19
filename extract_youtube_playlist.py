# Justin Caringal
# A script to extract a Youtube playlist into
# a text format

# Elapsed time
from time import time

# Youtube Library
import pytube

# Multithreading Libraries
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def extract_info(video):
    ''' Streamlines extraction
    
    A function which breaks down a pytube video object
    into its component parts and returns a populated
    dictionary containing the relevant information

    Args:
        video (Video): pytube video object
    
    Returns:
        dict: A dictionary with the relevant video info
    '''

    info_dict = {
        'title' : video.title,
        'author' : video.author
    }
    return info_dict