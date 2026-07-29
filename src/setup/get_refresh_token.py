import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

SCOPE = "user-follow-read playlist-read-private playlist-modify-private"

load_dotenv()


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        cache_path="data/spotify_cache.json"
    )
)

# Trigger authentication
sp.current_user()
