"""
Experimental weight sensitivity test.
Compares original weights vs adjusted weights.
"""

from typing import Tuple, List
from .recommender import Song, UserProfile, load_songs


def score_song_original(song: Song, user: UserProfile) -> Tuple[float, str]:
    """Original scoring with genre: 3.0, mood: 1.5, energy: 2.0"""
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
    reasons.append(f"energy weight: {energy_score:.2f}")

    if user.likes_acoustic and song.acousticness >= 0.5:
        score += 0.5
        reasons.append("acoustic match")

    explanation = "; ".join(reasons) if reasons else "no match"
    return score, explanation


def score_song_experimental(song: Song, user: UserProfile) -> Tuple[float, str]:
    """Experimental: genre: 2.0, mood: 1.5, energy: 3.0 (energy weighted heavier)"""
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.favorite_genre:
        score += 2.0  # Reduced from 3.0
        reasons.append("genre matches")

    if song.mood == user.favorite_mood:
        score += 1.5
        reasons.append("mood matches")

    energy_distance = abs(song.energy - user.target_energy)
    energy_score = max(0.0, 1.0 - energy_distance) * 3.0  # Increased from 2.0
    score += energy_score
    reasons.append(f"energy weight: {energy_score:.2f}")

    if user.likes_acoustic and song.acousticness >= 0.5:
        score += 0.5
        reasons.append("acoustic match")

    explanation = "; ".join(reasons) if reasons else "no match"
    return score, explanation


def run_weight_comparison():
    """Compare original vs experimental weights."""
    songs_dicts = load_songs("data/songs.csv")

    # Convert to Song objects
    songs = [
        Song(
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
        for song in songs_dicts
    ]

    # Test case: Conflicting preferences (Happy but Low Energy)
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.2,
        likes_acoustic=True,
    )

    print("\n" + "=" * 70)
    print("WEIGHT EXPERIMENT: Conflicting Preferences (Happy but Low Energy)")
    print("=" * 70)

    # Original scores
    original_scored = [
        (song, *score_song_original(song, user)) for song in songs
    ]
    original_scored.sort(key=lambda x: x[1], reverse=True)

    # Experimental scores
    experimental_scored = [
        (song, *score_song_experimental(song, user)) for song in songs
    ]
    experimental_scored.sort(key=lambda x: x[1], reverse=True)

    print("\n--- ORIGINAL WEIGHTS (Genre: 3.0, Energy: 2.0 max) ---\n")
    print("Top 5:")
    for i, (song, score, reason) in enumerate(original_scored[:5], 1):
        print(
            f"{i}. {song.title} | Score: {score:.2f} | {reason}"
        )

    print("\n--- EXPERIMENTAL WEIGHTS (Genre: 2.0, Energy: 3.0 max) ---\n")
    print("Top 5:")
    for i, (song, score, reason) in enumerate(experimental_scored[:5], 1):
        print(
            f"{i}. {song.title} | Score: {score:.2f} | {reason}"
        )

    print("\n--- INSIGHT ---")
    print(
        "With original weights, high-energy pop songs rank high because genre match"
    )
    print("(+3.0) outweighs the energy mismatch penalty.")
    print("")
    print("With experimental weights, energy becomes more important, but genre still")
    print("dominates. The 'Gym Hero' (pop, intense, 0.93 energy) vs low-energy acoustic")
    print("shows that genre is THE critical signal in this system.")
    print("")
    print("Recommendation: For conflicting preferences, the system fails to balance")
    print("competing signals. A user wanting 'happy pop' but 'low energy' is inherently")
    print("a niche that our simple weighted sum cannot satisfy without more nuance.")


if __name__ == "__main__":
    run_weight_comparison()
