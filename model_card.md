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

### Biggest Learning Moment

The turning point was testing the "Conflicting Preferences" profile (happy pop, but low energy). I fully expected the recommender to somehow balance these signals, but instead it returned high-energy pop songs with complete confidence. At first, I thought it was a bug. Then I realized: **it wasn't a bug—it was a fundamental architectural choice.**

By weighting genre 3.0x heavier than energy, I had built a system that treats genre as non-negotiable and everything else as a secondary refinement. This single weight ratio made the entire behavior emerge. Changing it required not just tweaking numbers, but reconsidering the entire model.

This taught me that in machine learning, the **highest-leverage decisions aren't in the code—they're in how you combine signals.** A simple +3.0 vs. +2.0 choice shapes thousands of recommendations.

### AI Tools in This Process

**What helped:**
- Used Copilot to quickly scaffold the OOP structure and CSV loading code, which eliminated boilerplate friction
- Asked Copilot for suggestions on weighting schemes, which accelerated the scoring logic design
- Generated comprehensive docstrings automatically, improving code clarity

**When I needed to double-check:**
1. **Weight suggestions:** Copilot suggested "genre: 2.0, mood: 2.0, energy: 1.0" but I had to manually test it to see it didn't differentiate enough between genre and mood
2. **Energy distance formula:** The AI suggested a simpler linear calculation, but I manually verified that `max(0, 1 - distance) * weight` was more intuitive
3. **Explanations:** Generated explanations looked good but sometimes included redundant detail; I hand-curated them to be concise and actionable

**Key insight:** Tools are best at speed, worst at taste. Copilot can generate 80% of working code in 20% of the time, but *you* have to decide what "good" is.

### What Surprised Me About Simple Algorithms

I was genuinely surprised at how **plausible** the recommendations felt, even though the algorithm is just three weighted sums. When I ran the pop/happy profile, "Sunrise City" came back as #1, and I thought "yeah, that makes sense!" without looking at the math first.

This revealed something important: **Users don't demand perfection; they demand explanation.** When the recommender returned high-energy pop to a low-energy user, it felt *wrong* not because the math was bad, but because I could see the reasoning ("genre matches") and recognize it was incomplete. Real streaming apps work partly because they hide their flaws under layers of:
- Collaborative filtering (other users' behavior)
- Personalization (your listen history)
- Serendipity (surprise recommendations)
- Context (time of day, playlist type)

A simple weighted sum can feel satisfying for 5 recommendations to a casual user. The cracks only show under stress testing.

### What Surprised Me About AI Systems

Building this recommender gave me empathy for why real recommenders are so complex. The moment I tried to optimize for "all user preferences at once," I hit the conflicting preferences problem, which forces hard architectural choices:
- Do you optimize for one dominant signal (genre) or try to balance competing signals?
- Do you use hard thresholds ("if energy preference is extreme, ignore genre") or soft weighting?
- Do you sacrifice predictability for serendipity?

Real systems answer these questions differently for different users, using collaborative filtering to fill the gaps that content-based alone cannot handle. This project made me understand why **ensemble and multi-model approaches are standard**, not optional.

### What I'd Try Next

If I extended this project, I'd tackle the conflicting preferences problem head-on:

1. **Build a multi-mode recommender:** 
   - Mode 1: "Strict matching" (all user signals matter equally, use Pareto optimality to find non-dominated songs)
   - Mode 2: "Genre first, then refine" (current approach)
   - Mode 3: "Exploration mode" (ignore genre, reward diversity)
   - Let users choose which mode they want

2. **Add a mood distribution chart:**
   - Show the user "here are the 5 recommendations, here's how they score on genre, mood, energy" as a simple table or visualization
   - This transparency would help users understand why conflicting preferences are hard to satisfy

3. **Implement user feedback loops:**
   - After recommending songs, ask "was this good?" and use answers to adjust weights dynamically
   - A user who thumbs-down "high-energy pop" repeatedly would trigger a mode switch away from genre dominance

4. **Expand to collaborative filtering:**
   - Add 5-10 more simulated users with their own profiles
   - Use "people like you enjoyed..." to surface songs that collaborative filtering finds but content-based filtering misses
   - This would solve the serendipity problem

5. **Test on real users (eventually):**
   - This simulation is useful, but real music taste is messier and includes factors this model doesn't capture (lyrics, artist prestige, cultural context, mood contagion)
   - A/B testing against Spotify or YouTube would ground the weights in reality

### Final Thought

This project taught me that **understanding limitations is more valuable than achieving perfection.** I could have spent hours tweaking weights to get slightly better test results, but instead, I spent time understanding *why* the system fails on conflicting preferences. That understanding is what makes a good engineer—knowing not just how to code, but why simple approaches break and what trade-offs exist in more complex ones.

Machine learning recommenders feel like magic because the outputs seem personalized and thoughtful. But behind every "smart recommendation" is someone who made explicit choices about what signals matter most, and those choices reveal what the system *values*. In this case, I chose genre over energy, and that single choice defined the entire user experience.
