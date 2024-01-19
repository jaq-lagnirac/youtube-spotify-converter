# Justin Caringal
# Based off tutorial--> https://www.youtube.com/watch?v=WAmEZBEeNmg

from dotenv import load_dotenv
import os
import base64
import json
import requests


# loads in private .env variables
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_token():
    # returns base64 object to send API request to
    auth_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    # set up requests variables
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization' : f'Basic {auth_base64}',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {'grant_type' : 'client_credentials'}

    # formulate response
    result = requests.post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

token = get_token()
print(token)