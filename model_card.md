# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatcher 1.0** — A simple content-based music recommender that scores songs based on genre, mood, energy, and acoustic properties.

---

## 2. Intended Use  

This recommender suggests the top 5 songs from a 18-song catalog based on a user's music taste profile. It uses weighted scoring over categorical (genre, mood) and numerical (energy distance, acousticness) features.

**For:** Educational exploration of how recommendation systems work. NOT for real-world deployment.

**Assumptions:** Users have a single, stable favorite genre and mood; energy preference is independent of other features; acoustic preference is binary.

---

## 3. How the Model Works  

The recommender scores each song by summing points for matching user preferences:

- **Genre match:** +3.0 points (most important signal)
- **Mood match:** +1.5 points  
- **Energy similarity:** 0–2.0 points based on how close the song's energy is to the user's target (calculated as `max(0, 1 - |song_energy - target_energy|) * 2`)
- **Acoustic bonus:** +0.5 points if the user likes acoustic songs AND the song has acousticness ≥ 0.5

All songs are scored, then ranked from highest to lowest score. The top K are recommended with explanations.

**Design logic:** Genre is weighted heaviest because it's the broadest taste signal. Energy distance rewards nuance—songs close to your energy preference score better than those far away. This avoids the trap of "just pick the highest energy" or "just pick the lowest energy."

---

## 4. Data  

**Catalog Size:** 18 songs (expanded from 10 starter songs)

**Coverage:**
- Genres: pop, rock, metal, latin, folk, electronic, reggae, classical, hip hop, jazz, ambient, lofi, indie pop, synthwave (14 genres)
- Moods: happy, intense, chill, peaceful, upbeat, warm, dreamy, soulful, nostalgic, energized, playful, relaxed, focused, moody (14 moods)
- Energy range: 0.28 (ambient) to 0.94 (metal)
- Acousticness range: 0.05 (pop/rock) to 0.95 (classical)

**Limitations:** 
- No hip hop or rap songs actually made it in despite labels; need more diverse artist representation
- Catalog is small (major streaming services have millions)
- No music from non-Western traditions (Indian classical, K-pop, etc.)
- All songs have upbeat or neutral emotional valence; missing "sad" or "angry" moods

---

## 5. Strengths  

1. **Clear differentiation by genre:** For users with strong genre preferences (e.g., "I want lofi"), the recommender works very well. All five test profiles with consistent preferences got genre-aligned recommendations as #1.

2. **Energy nuance:** The distance-based energy scoring prevents the system from simply picking "all high energy" or "all low energy." A user targeting 0.4 energy gets songs ranging from 0.28 to 0.42, creating variety within the energy band.

3. **Transparent reasoning:** Every recommendation comes with a clear explanation (e.g., "genre matches; mood matches; energy is close"), making it easy to understand why a song was suggested.

4. **Mood + Genre interaction:** When genre match fails, mood can still elevate a song (e.g., "Rooftop Lights" ranks 4th for the pop/happy user because it has "indie pop" + "happy" mood, earning points for mood even without exact genre).

5. **Acoustic bonus adds nuance:** Users with acoustic preferences get a measurable boost for fitting songs, helping them discover artists like "Willow Root" or "Orchestra Noir."

---

## 6. Limitations and Bias  

**Major Finding:** The system **over-prioritizes genre** and cannot handle conflicting user preferences.

**The Conflicting Preference Problem:**
When testing a profile asking for "happy pop at low energy (0.2)," the recommender returned high-energy pop songs (0.82–0.93 energy). Why?

Because:
- Genre match = 3.0 points (pop → "Sunrise City," "Gym Hero," etc. score 3.0+ immediately)
- Energy mismatch = only 0.76–1.0 point penalty (for songs 0.62 energy away)
- Mood match = 1.5 points (only "Sunrise City" has happy)

Result: A pop song with "wrong" energy still scores 3.54–5.26 points. A low-energy non-pop song scores ~2.3 points, even if it matches the acoustic and energy preferences.

**This is a real problem in music streaming:** A user wanting "happy but chill" legitimately wants both signals honored. Our weighting says "No; pop is more important than your energy preference."

**Other Limitations:**
- **Mood underweighting:** Mood is worth only 1.5 vs. 3.0 for genre. In reality, mood/vibe might be equally important.
- **No negative signals:** A user who dislikes "metal" gets penalized for metal songs only by energy mismatch, not by genre. No explicit "avoid this genre" option.
- **Energy distance is forgiving:** A song 0.6 energy away still scores 0.8 points. For a user wanting very specific energy (like meditation music at 0.1), this is too lenient.
- **Small catalog bias:** With only 18 songs across 14+ genres, some genres have only 1–2 representatives. "Classical" has just 1 song ("Moonlit Sonata"), so a classical fan gets very limited options.
- **Dataset representation bias:** Pop is 4/18 songs (~22%). A pop-loving recommender will naturally surface pop more often, which reinforces the pop-heavy bias in the data.

---

## 7. Evaluation  

**Test Profiles Evaluated:**
1. High-Energy Pop Lover (genre: pop, mood: happy, energy: 0.8)
2. Chill Lofi Focus Music (genre: lofi, mood: chill, energy: 0.4, acoustic: true)
3. Deep Intense Rock (genre: rock, mood: intense, energy: 0.9)
4. Peaceful Acoustic Folk (genre: folk, mood: peaceful, energy: 0.3, acoustic: true)
5. Upbeat Electronic Dance (genre: electronic, mood: upbeat, energy: 0.85)
6. Conflicting Preferences (genre: pop, mood: happy, energy: 0.2, acoustic: true) [EDGE CASE]

**Key Findings:**

For profiles 1–5 with aligned preferences, the recommender excels. Profile 6 (conflicting) revealed a critical weakness: genre dominates energy by a 3:1 margin, so a low-energy user asking for pop still gets high-energy pop songs.

**Weight Sensitivity Experiment:**
Changed genre from 3.0 → 2.0 and energy from 2.0 → 3.0 for conflicting preferences:
- Original: "Sunrise City" (pop, 0.82 energy) scored 5.26 (3.0 + 0.76 + 1.5)
- Experimental: "Spacewalk Thoughts" (0.28 energy) scored 3.26 (0 + 2.76 + 0.5)

Result: Energy weight increased importance, but genre still has too much inertia. The solution requires rethinking how to combine competing signals, not just reweighting.

**Surprise:** The recommender is too predictable. For any genre match, that genre dominates results. Real systems use collaborative filtering to add serendipity—"people like you also enjoyed..."—which this model cannot do.

---

## 8. Future Work  

1. **Conditional weighting:** If a user's energy preference conflicts with their genre, reduce genre weight and boost energy weight dynamically.

2. **Negative preferences:** Allow users to blacklist genres ("No metal") or specify mood ranges ("Energy 0.2–0.4 only").

3. **Collaborative filtering layer:** Find users with similar taste profiles and recommend songs they liked that this user hasn't heard yet (would require more user data).

4. **Valence + Arousal model:** Use psychological mood dimensions (valence = positive/negative, arousal = calm/excited) instead of categorical mood. This would allow for "happily exhausted" or "sadly relaxed."

5. **Discover mode:** Add an "exploration" flag that temporarily reduces genre weight and rewards novelty (songs not in the user's recent history).

6. **Larger catalog:** Expand to 100+ songs with more balanced genre/mood distribution to reduce recommendation repetitiveness.

7. **Contextual recommendations:** Consider time of day, user activity (gym vs. sleep), or playlist context (study mix vs. party mix) to adjust preferences dynamically.

---

## 9. Personal Reflection  

**What I learned:**
Building a simple weighted-sum recommender exposed the fragility of naive preference weighting. It seems obvious that "genre is most important," but testing revealed that this assumption breaks down when user preferences conflict. Real streaming services handle this with multiple algorithms (collaborative + content-based + contextual), and now I understand why.

I also learned that **transparency and explainability matter.** By generating explanations ("genre matches; mood matches; energy is close"), I could immediately spot when the system was wrong (recommending 0.93-energy songs to a 0.2-energy user). This kind of reasoning output is essential for debugging recommendation systems.

**Something unexpected:**
The conflicting preferences case showed me that the initial "simple sum" approach is insufficient. A user wanting "happy but chill" doesn't want a *compromise*; they want songs that satisfy ALL preferences. Our model instead **forced a ranking trade-off**, with genre always winning. This mirrors a real criticism of streaming services: recommendations can feel generic if they over-optimize for simplicity.

**How this changed my thinking:**
I no longer view music taste as a single point ("pop fan") but as a multidimensional shape—someone might love high-energy pop for workouts, sad acoustic pop for reflection, and upbeat electronic pop for parties. A better recommender would recognize these sub-preferences within a single user profile, not just average them into one.
