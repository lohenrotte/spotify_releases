import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-follow-read playlist-modify-private",
        cache_path=".spotify_cache"
    )
)

# Trigger authentication
sp.current_user()
