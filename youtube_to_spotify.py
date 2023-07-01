# Justin Caringal
# A script to convert a Youtube playlist into
# a Spotify playlist

# Standard Python Libraries
import os
import sys
import argparse
import logging

# Library to load in .env
from dotenv import load_dotenv

# Youtube API client library
import googleapiclient.discovery

# Youtube API info
api_service_name = 'youtube'
api_version = 'v3'

# Youtube API key
load_dotenv()
YOUTUBE_TOKEN = os.getenv('YOUTUBE_TOKEN')

# API client
youtube = googleapiclient.discovery.build(api_service_name,
                                          api_version,
                                          developerKey = YOUTUBE_TOKEN)

request = youtube.playlistItems().list()

# Query execution
response = request.execute()

print(response)