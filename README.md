# 🎵 Music Recommender Simulation

## Project Summary

This project implements a content-based music recommender system that suggests the top K songs from a catalog based on a user's taste profile. The system uses a weighted scoring algorithm that combines categorical matches (genre, mood) with numerical proximity calculations (energy distance).

The recommender includes:
- A `Song` data model with 10 attributes (genre, mood, energy, tempo, valence, danceability, acousticness, etc.)
- A `UserProfile` that captures listener preferences (favorite genre, mood, target energy, acoustic preference)
- A scoring function that awards points for matches and rates energy similarity
- A ranking function that sorts all songs and recommends the top K
- Both object-oriented and functional implementations

---

## How The System Works

This recommender simulates how a music service uses both categorical taste signals and numerical audio features. Each song is represented by attributes such as `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The user profile stores the listener's preferences for `favorite_genre`, `favorite_mood`, `target_energy`, and acoustic tendency.

The system scores every song against the user profile, then sorts songs by score to produce the top recommendations.

### Algorithm Recipe

- +3.0 points for a genre match
- +1.5 points for a mood match
- Similarity points for energy based on closeness to the user's target energy:
  - energy score = `max(0, 1 - abs(song.energy - target_energy)) * 2`
- +0.5 points if the user likes acoustic music and the song is acoustic enough

This recipe prioritizes genre as the strongest signal, while still using mood and energy distance to shape the recommendation.

### Data Flow

Input: User preferences (`favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`)

Process: Loop over every song in `data/songs.csv`, compute a score for each song, build an explanation for the match.

Output: Rank songs by score and return the top K recommendations.

```mermaid
flowchart LR
    U[User Prefs] --> P[Build UserProfile]
    P --> L[Load songs from CSV]
    L --> S[For each song: compute genre, mood, energy, acoustic score]
    S --> R[Score each song]
    R --> T[Sort by score]
    T --> O[Top K recommendations]
```

### Potential Biases

This system may over-prioritize genre matches and prefer songs that simply match the user’s stated energy level. As a result, it could ignore songs that are emotionally right for the listener but differ in genre, or overlook songs with subtle mood fit because they are not the exact genre or energy target.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Evaluation & Stress Testing

### Test Case 1: High-Energy Pop Lover
`{"genre": "pop", "mood": "happy", "energy": 0.8}`

✅ **Result:** Works perfectly. Top recommendation is "Sunrise City" (pop, happy, 0.82 energy) with score 6.46. System correctly weights genre + mood + energy proximity.

### Test Case 2: Chill Lofi Focus Music
`{"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": true}`

✅ **Result:** Excellent. Top two "Midnight Coding" (6.96) and "Library Rain" (6.90) are both lofi, chill, low-energy, and acoustic. Recommender found genre + mood + energy + acoustic alignment.

### Test Case 3: Deep Intense Rock
`{"genre": "rock", "mood": "intense", "energy": 0.9}`

✅ **Result:** Returns "Storm Runner" (rock, intense, 0.91 energy) as #1 with score 6.48. Perfect match.

### Test Case 4: Peaceful Acoustic Folk
`{"genre": "folk", "mood": "peaceful", "energy": 0.3, "likes_acoustic": true}`

✅ **Result:** "Forest Hymn" (folk, peaceful, 0.45 energy, acoustic) scores 6.70. System works well for consistent, low-energy preferences.

### Test Case 5: Upbeat Electronic Dance
`{"genre": "electronic", "mood": "upbeat", "energy": 0.85}`

✅ **Result:** "Neon Pulse" (electronic, upbeat, 0.85 energy) scores 6.50. Perfect match.

### Test Case 6: Conflicting Preferences (Edge Case)
`{"genre": "pop", "mood": "happy", "energy": 0.2, "likes_acoustic": true}`

❌ **FAILURE CASE:** User wants happy pop music BUT at low energy (0.2). Recommender returns:
1. **Sunrise City** (pop, happy, **0.82 energy**) - Score: 5.26  ← High energy!
2. City Sunrise (pop, nostalgic, 0.70 energy) - Score: 4.00
3. Gym Hero (pop, intense, **0.93 energy**) - Score: 3.54  ← Very high energy!

**Why this fails:** Genre match (+3.0) outweighs energy mismatch. "Sunrise City" gets 3.0 for genre + 1.5 for mood + 0.76 for poor energy = 5.26. A low-energy non-pop alternative (e.g., "Spacewalk Thoughts" at 0.28 energy) only scores 2.34 despite matching energy + acoustic preferences. **Conclusion: Genre weight is 3× more important than energy, making conflicting preferences unrecoverable.**

### Weight Sensitivity Experiment

Tested if reducing genre weight (3.0 → 2.0) and increasing energy weight (2.0 → 3.0) could fix conflicting preferences:

| Metric | Original | Experimental | Change |
|---|---|---|---|
| Genre weight | 3.0 | 2.0 | -33% |
| Energy weight (max) | 2.0 | 3.0 | +50% |
| Top song for low-energy user | Sunrise City (5.26) | Sunrise City (4.64) | Still genre-first |
| #3 song | Gym Hero (3.54) | Spacewalk Thoughts (3.26) | Energy ranked higher |

**Finding:** Even with increased energy weight, genre still dominates the top recommendations. The architecture (simple weighted sum) cannot handle truly conflicting preferences. A user wanting "happy but chill" would need a multiplicative or conditional model to balance competing signals.

### Key Insights Across All Cases

1. **Genre is the dominant signal.** 5/6 profiles with clear genre preferences received genre-matched recommendations as #1. No weight adjustment changed this.

2. **Conflicting preferences break the model.** The simple weighted sum cannot satisfy competing signals (e.g., "happy but low energy"). Real systems use ensemble methods or conditional logic to handle this.

3. **Energy distance works well for aligned preferences.** Users targeting low energy (0.3–0.4) correctly receive songs in the 0.28–0.45 range, providing nuance and variety.

4. **Explanations build trust.** By providing text reasons, users understand exactly why they got a recommendation and can spot errors.

5. **Mood matters, but is underweighted.** Mood (1.5 points) is 2× weaker than genre (3.0 points). For some music fans, mood might be MORE important than strict genre matching.

---

## 📋 Evaluation Checkpoint

✅ **Completed:**
- 6 user profiles tested (5 aligned cases pass; 1 edge case reveals critical limitation)
- Weight sensitivity experiment confirms architectural constraint
- Bias and limitation analysis documented in model_card.md
- All unit tests passing (2/2)

✅ **Key Finding:** The system works well when user preferences align but reveals the limitation of simple weighted-sum models when handling conflicting signals. This explains why real streaming services use hybrid and ensemble approaches.

---

## ✅ Implementation Checkpoint

All core components are implemented and tested:

- ✅ Data layer: `Song` and `UserProfile` dataclasses with proper types
- ✅ CSV loader: `load_songs()` reads and parses numeric features correctly
- ✅ Scoring logic: `score_song_for_user()` returns both numeric score and text explanation
- ✅ Recommender: Both OOP (`Recommender.recommend()`) and functional (`recommend_songs()`) implementations
- ✅ Tests: 2/2 passing (songs sorted by score, explanations non-empty)
- ✅ CLI: `python -m src.main` outputs comprehensive recommendations with scores and reasons
- ✅ Dataset: 18 songs with diverse genres and moods across 14 genres
- ✅ Evaluation: 6 test profiles with detailed findings documented in README and model_card.md

The recommender successfully demonstrates content-based filtering and reveals key architectural limitations of simple approaches.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

