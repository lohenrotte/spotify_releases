from datetime import datetime, timedelta
import json
from cache import save_cache


def get_followed_artists(sp) -> list:

    after = None
    followed_artists = []
    while True:
        results = sp.current_user_followed_artists(limit=50, after=after)

        for artist in results["artists"]["items"]:
            followed_artists.append((artist["id"], artist["name"]))

        after = results["artists"]["cursors"]["after"]
        if not after:
            break
    return followed_artists

def get_release_tracks(sp, album_id):
    tracks = sp.album_tracks(album_id)
    return tracks["items"]

def parse_release_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def get_artist_releases(sp, artist_id, days=7):
    cutoff = datetime.today() - timedelta(days=days)

    releases = sp.artist_albums(
        artist_id,
        include_groups="album,single,appears_on",
        limit=10
    )

    return [
        release
        for release in releases["items"]
        if (date := parse_release_date(release["release_date"]))
        and date >= cutoff
    ]

def get_unique_track_uris(tracks):
    seen = set()
    uris = []
    for track in tracks:
        tid = track["uri"]
        if tid not in seen:
            seen.add(tid)
            uris.append(tid)
    return uris

def get_or_create_playlist(sp, cache, name):

    # Already cached
    if cache.get("playlist_id"):
        return sp.playlist(cache["playlist_id"])

    playlist = sp.current_user_playlist_create(
        name=name,
        public=False,
        description="",
    )

    cache["playlist_id"] = playlist["id"]
    save_cache(cache)

    return playlist

def add_new_tracks_to_playlist(sp, playlist_id, track_uris):
    
    # Get existing track URIs
    existing_uris = set()
    offset = 0

    while True:
        results = sp.playlist_items(
            playlist_id,
            fields="items(item.uri), next",
            limit=100,
            offset=offset,
        )

        for item in results["items"]:
            track = item.get("item")
            if track and track.get("uri"):
                existing_uris.add(track["uri"])

        if results["next"] is None:
            break

        offset += 100

    # Keep only tracks not already present
    new_track_uris = [
        track_uri
        for track_uri in track_uris
        if track_uri not in existing_uris
    ]

    # Add in batches of 100
    for i in range(0, len(new_track_uris), 100):
        sp.playlist_add_items(
            playlist_id,
            new_track_uris[i:i + 100],
        )

    return len(new_track_uris)
