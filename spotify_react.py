import spotipy
from spotipy.oauth2 import SpotifyOAuth

import sys
import os
import json

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller and IDE) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

with open(resource_path("config.json"), "r") as f:
    config = json.load(f)



SPOTIFY_CLIENT_ID = config.get("spotify_client_id")
SPOTIFY_CLIENT_SECRET = config.get("spotify_client_secret")
SPOTIFY_REDIRECT_URI = config.get("spotify_redirect_uri")

sp = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URI and SPOTIFY_CLIENT_ID != "YOUR_SPOTIFY_CLIENT_ID_HERE":
    try:
        sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope='user-read-playback-state user-read-currently-playing',
        )
        sp = spotipy.Spotify(auth_manager=sp_oauth)
    except Exception as e:
        print(f"Failed to initialize Spotify: {e}")
        sp = None

def get_current_song():
    if sp:
        try:
            current = sp.current_playback()
            if current and current['is_playing']:
                track = current['item']
                return f"{track['name']} by {track['artists'][0]['name']}"
        except Exception as e:
            # This will fail if the user is not authenticated, which is expected
            # if they haven't run the authentication flow.
            # We can silence this error.
            pass
    return None
