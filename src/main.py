"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define diverse test profiles
    test_profiles = [
        {
            "name": "High-Energy Pop Lover",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
        },
        {
            "name": "Chill Lofi Focus Music",
            "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
        },
        {
            "name": "Deep Intense Rock",
            "prefs": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
        },
        {
            "name": "Peaceful Acoustic Folk",
            "prefs": {"genre": "folk", "mood": "peaceful", "energy": 0.3, "likes_acoustic": True},
        },
        {
            "name": "Upbeat Electronic Dance",
            "prefs": {"genre": "electronic", "mood": "upbeat", "energy": 0.85, "likes_acoustic": False},
        },
        {
            "name": "Conflicting Preferences (Happy but Low Energy)",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.2, "likes_acoustic": True},
        },
    ]

    # Test all profiles
    for profile in test_profiles:
        print(f"\n{'='*60}")
        print(f"Profile: {profile['name']}")
        print(f"Preferences: {profile['prefs']}")
        print(f"{'='*60}\n")

        recommendations = recommend_songs(profile["prefs"], songs, k=5)

        print("Top 5 recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"{i}. {song['title']} by {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
            print(f"   Score: {score:.2f}")
            print(f"   Reason: {explanation}")
            print()


if __name__ == "__main__":
    main()
