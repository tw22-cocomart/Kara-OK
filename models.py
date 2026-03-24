# models.py
# Defines the Song class used in the karaoke app.

class Song:
    def __init__(self, sid: str, title: str, artist: str, lyrics: str = ""):
        # Create a new Song with ID, title, artist, and optional lyrics
        self.id = sid
        self.title = title
        self.artist = artist
        self.lyrics = lyrics

    def to_dict(self):
        # Convert Song object into a dictionary (for saving to JSON)
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "lyrics": self.lyrics
        }

    @staticmethod
    def from_dict(d):
        # Create a Song object from a dictionary (for loading from JSON)
        return Song(d["id"], d["title"], d["artist"], d.get("lyrics", ""))
