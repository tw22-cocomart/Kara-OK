# service.py
# Handles the main logic for songs, searching, queue management, and scoring.

from models import Song
import storage
import random

# In-memory storage for songs and queue
_songs = {}   # song ID -> song info (dict)
_queue = []   # list of song IDs

def init_backend():
    # Load songs and queue from JSON files
    global _songs, _queue
    _songs = storage.load_songs()
    _queue = storage.load_queue()

# --- SongBook functions ---
def get_all_songs():
    # Return all songs in the catalog
    return list(_songs.values())

def search_songs(query: str):
    # Search songs by ID, title, or artist
    q = query.lower().strip()
    results = []
    for sid, info in _songs.items():
        if q in sid.lower() or q in info.get("title","").lower() or q in info.get("artist","").lower():
            results.append(info)
    return results

def add_song_to_catalog(sid: str, title: str, artist: str, lyrics: str = ""):
    # Add a new song to the catalog and save it
    _songs[sid] = {"id": sid, "title": title, "artist": artist, "lyrics": lyrics}
    storage.save_songs(_songs)

# --- Queue functions ---
def reserve_song(song_id: str):
    # Add a song to the queue if it exists
    if song_id not in _songs:
        raise ValueError("Song ID not found")
    _queue.append(song_id)
    storage.save_queue(_queue)

def get_queue():
    # Return the current queue list
    return list(_queue)

def current_song():
    # Return the song at the front of the queue
    return _songs.get(_queue[0]) if _queue else None

def skip_current():
    # Remove the current song from the queue
    if _queue:
        skipped = _queue.pop(0)
        storage.save_queue(_queue)
        return skipped
    return None

# --- Scoring ---
def score_performance(song_id: str, performance_text: str = "") -> int:
    # Simple scoring placeholder based on lyrics length + random factor
    lyrics = _songs.get(song_id, {}).get("lyrics", "")
    base = len(lyrics) % 70
    rand = random.randint(0, 30)
    return min(100, base + rand)
