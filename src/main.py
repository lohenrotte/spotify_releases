from dotenv import load_dotenv
from cache import load_cache
from utils import get_artist_releases, get_or_create_playlist, get_release_tracks
from spotify_client import get_spotify_client


# Load environment variables and initialize Spotify client
load_dotenv()
sp = get_spotify_client()
cache = load_cache()

# Create or retrieve the playlist
playlist_name = "new releases"
playlist = get_or_create_playlist(sp, cache, playlist_name)

# Get followed artists 
artists = sp.current_user_followed_artists(limit=10)["artists"]["items"]

# Get new tracks from followed artists in the last 7 days
tracks = []
for artist in artists:
    print(f"Artist: {artist['name']}")
    for release in get_artist_releases(sp, artist["id"], days=7):
        print(f"Release: {release['name']}")
        release["artist_name"] = artist["name"]
        for track in get_release_tracks(sp, release["id"]):
            print(f"Track: {track['name']}")
            tracks.append(track)

# Get unique track URIs to avoid duplicates
seen = set()
track_uris = []
for track in tracks:
    tid = track["uri"]
    if tid not in seen:
        seen.add(tid)
        track_uris.append(tid)

# Populate the playlist with new tracks
if track_uris:
    sp.playlist_add_items(playlist["id"], track_uris)
