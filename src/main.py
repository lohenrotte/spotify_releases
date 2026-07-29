from dotenv import load_dotenv
from utils import get_artist_releases, get_release_tracks
from spotify_client import get_spotify_client

import spotipy


load_dotenv()

sp = get_spotify_client()

artists = sp.current_user_followed_artists(limit=5)["artists"]["items"][:1]

print(artists)

tracks = []
for artist in artists:
    for release in get_artist_releases(sp, artist["id"], days=7):
        release["artist_name"] = artist["name"]
        for track in get_release_tracks(sp, release["id"]):
            tracks.append(track)

tracks = list({track["id"]: track for track in tracks}.values())

for track in tracks:
    print(f"{track['name']} - {track['artists'][0]['name']}")
