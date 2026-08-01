import spotipy
import json

from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from dotenv import load_dotenv

SCOPE = "user-follow-read playlist-read-private playlist-modify-private"
USER_CACHE_PATH = Path("cache/user.json")
SPOTIFY_CACHE_PATH = Path("cache/spotify.json")

load_dotenv()


def load_cache():
    if not USER_CACHE_PATH.exists():
        return {
            "playlist_id": "",
        }

    with open(USER_CACHE_PATH, "r") as f:
        return json.load(f)

def save_cache(cache):
    USER_CACHE_PATH.parent.mkdir(exist_ok=True)

    with open(USER_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def create_playlist(sp, cache, name):

    # Already cached
    if cache.get("playlist_id"):
        return cache["playlist_id"]

    playlist = sp.current_user_playlist_create(
        name=name,
        public=False,
        description="",
    )

    cache["playlist_id"] = playlist["id"]
    save_cache(cache)

    return playlist["id"]


if __name__ == "__main__":

    auth_manager = SpotifyOAuth(
        scope=SCOPE,
        cache_path=SPOTIFY_CACHE_PATH,
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Trigger authentication
    sp.current_user()

    # Get the refresh token from the cache
    token_info = auth_manager.cache_handler.get_cached_token()
    refresh_token = token_info["refresh_token"]
    print(f"Refresh Token: {refresh_token}")

    cache = load_cache()
    playlist = create_playlist(sp, cache, "new releases")
    print(f"Playlist ID: {playlist}")