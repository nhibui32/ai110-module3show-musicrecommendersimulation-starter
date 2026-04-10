import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Score and rank songs against a user profile to produce recommendations."""
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by match score for the user."""
        scored = [(song, *score_song_for_user(song, user)) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a text explanation for why a song was recommended to a user."""
        _, explanation = score_song_for_user(song, user)
        return explanation


def score_song_for_user(song: Song, user: UserProfile) -> Tuple[float, str]:
    """Score one song against a user profile and return a text explanation."""
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.favorite_genre:
        score += 3.0
        reasons.append("genre matches")

    if song.mood == user.favorite_mood:
        score += 1.5
        reasons.append("mood matches")

    energy_distance = abs(song.energy - user.target_energy)
    energy_score = max(0.0, 1.0 - energy_distance) * 2.0
    score += energy_score
    reasons.append(f"energy is close to the user's preference ({song.energy:.2f} vs {user.target_energy:.2f})")

    if user.likes_acoustic and song.acousticness >= 0.5:
        score += 0.5
        reasons.append("acousticness aligns with preference")

    explanation = "; ".join(reasons) if reasons else "no strong match found"
    return score, explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user preferences and return the top k ranked recommendations with explanations."""
    favorite_genre = user_prefs.get("genre", "")
    favorite_mood = user_prefs.get("mood", "")
    target_energy = float(user_prefs.get("energy", 0.5))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        user = UserProfile(
            favorite_genre=favorite_genre,
            favorite_mood=favorite_mood,
            target_energy=target_energy,
            likes_acoustic=likes_acoustic,
        )
        song_obj = Song(
            id=song["id"],
            title=song["title"],
            artist=song["artist"],
            genre=song["genre"],
            mood=song["mood"],
            energy=song["energy"],
            tempo_bpm=song["tempo_bpm"],
            valence=song["valence"],
            danceability=song["danceability"],
            acousticness=song["acousticness"],
        )
        score, explanation = score_song_for_user(song_obj, user)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
