import json
from pathlib import Path


CACHE_PATH = Path("data/user_cache.json")

def load_cache():
    if not CACHE_PATH.exists():
        return {
            "user_id": "",
            "playlist_id": "",
        }

    with open(CACHE_PATH, "r") as f:
        return json.load(f)


def save_cache(cache):
    CACHE_PATH.parent.mkdir(exist_ok=True)

    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)