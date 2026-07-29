from datetime import datetime, timedelta


def get_release_tracks(sp, album_id):
    tracks = sp.album_tracks(album_id)
    return tracks["items"]


def get_artist_releases(sp, artist_id, days=7):
    cutoff = datetime.today() - timedelta(days=days)

    releases = sp.artist_albums(
        artist_id,
        include_groups="album,single,appears_on",
        limit=10
    )

    return [
        release for release in releases["items"]
        if datetime.strptime(release["release_date"], "%Y-%m-%d") >= cutoff
    ]
