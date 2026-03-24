# storage.py
# Handles saving and loading data (songs, queue, users) to JSON files.

import json
from typing import Dict, List

# File paths for storing data
USERS_FILE = "data/users.json"
SONGS_FILE = "data/songs.json"
QUEUE_FILE = "data/queue.json"

def load_json(path: str, default):
    # Load JSON data from a file, return default if file is missing
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) 
    except FileNotFoundError:
        return default
    except Exception:
        raise

def save_json(path: str, data):
    # Save data into a JSON file
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        raise

def load_songs() -> Dict[str, Dict]:
    # Load all songs from songs.json
    return load_json(SONGS_FILE, {})

def save_songs(songs: Dict[str, Dict]):
    # Save songs back into songs.json
    save_json(SONGS_FILE, songs)

def load_queue() -> List[str]:
    # Load the song queue from queue.json
    return load_json(QUEUE_FILE, [])

def save_queue(queue_list: List[str]):
    # Save the song queue into queue.json
    save_json(QUEUE_FILE, queue_list)
