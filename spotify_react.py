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



SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:8000/callback'


SCOPE = 'user-read-playback-state user-read-currently-playing'


sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,

)


sp = spotipy.Spotify(auth_manager=sp_oauth)

def get_current_song():
    try:
        current = sp.current_playback()
        if current and current['is_playing']:

            track = current['item']
            return f"{track['name']} by {track['artists'][0]['name']}"
    except Exception as e:
        print("Spotify check failed:", e)
    return None
