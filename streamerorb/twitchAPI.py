import requests
from dotenv import load_dotenv, set_key
import os

# Load environment variables from .env file
load_dotenv()
if load_dotenv() == False:
    print("No .env file found. Please create one with the required values.")
    exit()

# Get values from the .env file
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')

def get_new_token(client_id, client_secret):
    token_url = 'https://id.twitch.tv/oauth2/token'
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    token_response = requests.post(token_url, params=token_params)
    token_response.raise_for_status()  # Raises an error for bad responses
    token_data = token_response.json()
    return token_data['access_token']

def update_env_file(token):
    set_key('.env', 'TWITCH_OAUTH_TOKEN', token)

def validate_token(token):
    validation_url = 'https://id.twitch.tv/oauth2/validate'
    headers = {
        'Authorization': f'OAuth {token}'
    }
    
    response = requests.get(validation_url, headers=headers)
    return response.status_code == 200

def get_valid_token():
    global ACCESS_TOKEN
    
    # Validate the current token
    if not validate_token(ACCESS_TOKEN):
        print("Current token is invalid or expired. Refreshing token...")
        ACCESS_TOKEN = get_new_token(CLIENT_ID, CLIENT_SECRET)
        update_env_file(ACCESS_TOKEN)
        print("New token obtained and stored.")
    #else:
        #print("Current token is still valid.")
    
    return ACCESS_TOKEN

def search_user(username):
    token = get_valid_token()
    search_url = 'https://api.twitch.tv/helix/search/channels'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    params = {
        'query': username,
        'first': 5,
        'live_only': 'false'
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    user_data = response.json()
    
    if user_data['data']:
        return user_data['data']
    else:
        return None

if __name__ == '__main__':
    users = search_user('arbavaçqhqwasvlrmaroib3214')
    print(users)
