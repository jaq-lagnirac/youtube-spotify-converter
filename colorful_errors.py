# Justin Caringal
# A custom method to standardize error messages and handling

import sys
from colorama import Fore, Style

def red(text):
    """ Streamlines red text
    
    Args: 
        text (str): the text to be colored

    Returns:
        str: A string colored to the desired shade
    
    """

    return Fore.RED + text + Style.RESET_ALL

def green(text):
    """ Streamlines green text
    
    Args: 
        text (str): the text to be colored

    Returns:
        str: A string colored to the desired shade
    
    """

    return Fore.GREEN + text + Style.RESET_ALL

def error_exit(message):
    """ Standardizes error

    A function to output an error message and safely exit the program.

    Args:
        message (str): the custom error message

    """

    print(red(f'ERROR! {message}\nExiting program.'))
    sys.exit(1)