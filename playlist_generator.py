import requests
import base64
from secrets import USER_CLIENT_ID, USER_CLIENT_SECRET, USER_REDIRECT_URI, spotify_user_id
from urllib.parse import urlencode

# using OAuth we create a link to redirect user to their spotify account
def create_oauth_link():
    params = {
        "client_id": USER_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": USER_REDIRECT_URI,
        "scope": "user-read-private user-read-email"
    }
    endpoint = "https://accounts.spotify.com/authorize"
    response = requests.get(endpoint, params=params)
    url = response.url
    return url

# authorization process to exchange code for token
# you can either pass client credentials either in the body or header base64 encoding
def exchange_code_token(code=None):
    code_params = {
        "grant_type": "client_credentials",
        "code": str(code),
        "redirect_uri": USER_REDIRECT_URI,
        "client_id": USER_CLIENT_ID,
        "client_secret": USER_CLIENT_SECRET,
    }
    #client_cred = f"{USER_CLIENT_ID}:{USER_CLIENT_SECRET}"
    #client_cred_b64 = base64.b64encode(client_cred.encode()).decode()
    #headers = {"Authorization": f"Basic {client_cred_b64}"}
    
    s_endpoint = "https://accounts.spotify.com/api/token"
    s_response = requests.post(s_endpoint, data=code_params).json()
    return s_response["access_token"]
    
# get user data
user_id = spotify_user_id
def print_user_info(user_id, access_token=None):
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = f"https://api.spotify.com/v1/users/{user_id}"
    response = requests.get(endpoint, headers=headers).json()
    name = response['display_name']
    return f"name: {name}"
    
# get user playlists
def get_user_playlists(user_id, access_token=None):
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(endpoint, headers=headers).json()

    for item in response["items"]:
        playlist_name = item["name"]
        playlist_id = item["id"]
        print(
            f"Playlist name: {playlist_name} | Playlist ID: {playlist_id}"
        )

link = create_oauth_link()
print(f"Follow the link to start the authentication with Spotify: {link}")
code = input("Spotify Code: ")
access_token = exchange_code_token(code)
print(print_user_info(user_id, access_token=access_token))
get_user_playlists(user_id, access_token=access_token)




