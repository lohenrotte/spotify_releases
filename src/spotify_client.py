import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-follow-read playlist-read-private playlist-modify-private"

def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=SCOPE,
            cache_handler=spotipy.cache_handler.MemoryCacheHandler(
                token_info={
                    "refresh_token": os.getenv("SPOTIPY_REFRESH_TOKEN"),
                    "access_token": "",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "scope": SCOPE,
                    "expires_at": 0,
                }
            )
        )
    )