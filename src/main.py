from dotenv import load_dotenv
from cache import load_cache
from utils import * 
from spotify_client import get_spotify_client


# Load environment variables and initialize Spotify client
load_dotenv()
sp = get_spotify_client()
cache = load_cache()

# Create or retrieve the playlist
playlist_name = "new releases"
playlist = get_or_create_playlist(sp, cache, playlist_name)

# Get all followed artists (up to 50 at a time)
artists = get_followed_artists(sp)

# Get new tracks from followed artists in the last 7 days
tracks = []
for i, artist in enumerate(artists):
    print(f"Artist {i + 1}: {artist[1]}")
    for release in get_artist_releases(sp, artist[0], days=7):
        print(f"Release: {release['name']}")
        for track in get_release_tracks(sp, release["id"]):
            print(f"Track: {track['name']}")
            tracks.append(track)


# Get unique track URIs to avoid duplicates
track_uris = get_unique_track_uris(tracks)

# Populate the playlist with new tracks
if track_uris:
    add_new_tracks_to_playlist(sp, playlist["id"], track_uris)
