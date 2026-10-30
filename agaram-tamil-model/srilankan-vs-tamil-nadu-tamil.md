# Sri Lankan Tamil vs Tamil Nadu Tamil

A fun experiment comparing Sri Lankan Tamil dialect and Tamil Nadu Tamil dialect 😁

Tested against [murai-labs/agaram-2.5b-instruct](https://huggingface.co/murai-labs/agaram-2.5b-instruct) — a 2.5B Tamil–English model trained from scratch by Murai Labs and Ramchand Kumaresan.

## Contents

- [Examples](#examples)
- [Testing Manually](#testing-manually)
- [App](#app)
- [Run](#run)
- [Results](#results)
- [Observations](#observations)
- [Conclusion](#conclusion)
- [Credits](#credits)

## Examples

| Meaning                    | Sri Lankan Tamil             | Tamil Nadu Tamil              |
| ---------------------------| -----------------------------| ------------------------------|
| Yes, I know.               | ஓம், எனக்குத் தெரியும்.      | ஆமா, எனக்குத் தெரியும்.       |
| I need to talk to you.     | நான் உங்களோட கதைக்க வேணும்.  | நான் உங்ககிட்ட பேசணும்.       |
| Where is that boy going?   | அந்தப் பெடியன் எங்க போறான்?  | அந்தப் பையன் எங்க போறான்?     |
| It looks beautiful.        | அது வடிவா இருக்கு.           | அது அழகா இருக்கு.             |
| Mother is in the kitchen.  | அம்மா குசினியில இருக்கிறா.   | அம்மா சமையலறையில இருக்காங்க.  |

All 20 examples: [sl-vs-tn-examples.json](sl-vs-tn-examples.json) — the single source of truth for this table and the app.


## Testing Manually 

```text
>>> """ Explain the meaning of this sentence in English:
... “அந்தப் பெடியன் வடிவா கதைக்கிறான்.”
"""
The boy is speaking in a very formal way.

>>> """ Explain the meaning of this sentence in English:
அந்தப் பையன் அழகா பேசுறான்.
"""
The boy is speaking in a very formal way.
```

Both sentences actually mean "the boy speaks **beautifully**" (வடிவா /
அழகா used as adverbs) — "speaking in a very formal way" is wrong both
times. This manual test was an early glimpse of the வடிவா/அழகா weakness,
with a nuance: அழகா as an adverb (அழகா பேசுறான், above) fails, while
அழகா as a predicate adjective (அழகா இருக்கு, row 7) passes in the app
run — same word, different grammar, different outcome.

## App

The app [sl-vs-tn-tamil.py](sl-vs-tn-tamil.py) runs all 20 examples from
[sl-vs-tn-examples.json](sl-vs-tn-examples.json).

Created with OpenCode + GLM 5.3

Prompt:

```text
Write a python app 'sl-vs-tn-tamil.py'.

It will read the table from sl-vs-tn-examples.json.

for each row, 
- print English meaning first
- ask the chat `Explain the meaning of this sentence in English: TAMIL variation` 
- and print out the output
- print the final summary

Use Ollama backend and use API to communicate.

And setup a uv project
```

## Run

First download the model (the Ollama server — menu-bar app or `ollama
serve` — must be running for the app to reach it):

```bash
ollama pull hf.co/murai-labs/agaram-2.5b-gguf:Q8_0
```

Then run the app

```bash
uv run sl-vs-tn-tamil.py
```

## Results

The app prints the results.. then they are manually checked for accuracy.

Run of `sl-vs-tn-tamil.py` (20 examples) —
murai-labs/agaram-2.5b-instruct served through Ollama (GGUF Q8_0), greedy
decoding (temperature 0).

- ✅ correct · 🟡 partial · ❌ wrong
- Sri Lankan Tamil: 12/20 ✅ (auto-graded 11/20 — manual review accepts row 15's "female")
- Tamil Nadu Tamil: 17/20 ✅


| # | English meaning | Sri Lankan Tamil | Model said (SL) | Tamil Nadu Tamil | Model said (TN) |
|---|---|---|---|---|---|
| 1 | Yes, I know. | ஓம், எனக்குத் தெரியும். | ✅ Oh, I know. | ஆமா, எனக்குத் தெரியும். | ✅ Yes, I know. |
| 2 | I need to talk to you. | நான் உங்களோட கதைக்க வேணும். | ❌ I want to tell you a story. | நான் உங்ககிட்ட பேசணும். | ✅ I want to talk to you. |
| 3 | I can’t come today. | எனக்கு இண்டைக்கு வர ஏலாது. | ✅ I can't come today. | என்னால இன்னைக்கு வர முடியாது. | ✅ I cannot come today. |
| 4 | What are you doing? | என்ன செய்யிறீங்கள்? | ✅ What are you doing? | என்ன பண்றீங்க? | ✅ What are you doing? |
| 5 | Have you eaten? | சாப்பிட்டீங்களோ? | ✅ Did you eat? | சாப்பிட்டீங்களா? | ✅ Did you eat? |
| 6 | Where is that boy going? | அந்தப் பெடியன் எங்க போறான்? | ❌ What is the boy going to? | அந்தப் பையன் எங்க போறான்? | ❌ What is the boy going to? |
| 7 | It looks beautiful. | அது வடிவா இருக்கு. | ❌ It looks like it. | அது அழகா இருக்கு. | ✅ It looks beautiful. |
| 8 | A little water, please. | கொஞ்சம் தண்ணி தாங்கோ. | 🟡 Please give me some water. | கொஞ்சம் தண்ணி குடுங்க. | 🟡 Give me some water. |
| 9 | Mother is in the kitchen. | அம்மா குசினியில இருக்கிறா. | ✅ Mom is in the kitchen. | அம்மா சமையலறையில இருக்காங்க. | ✅ Mom is in the kitchen. |
| 10 | Shall we go to the shop? | கடைக்குப் போவோமா? | ✅ Shall we go to the shop? | கடைக்குப் போலாமா? | ✅ Shall we go to the shop? |
| 11 | Can you come today? | உங்களுக்கு இண்டைக்கு வர ஏலுமா? | ✅ Can you come today? | உங்களால இன்னைக்கு வர முடியுமா? | ✅ Can you come today? |
| 12 | I can’t do this. | எனக்கு இதைச் செய்ய ஏலாது. | ✅ I cannot do this. | என்னால இதைப் பண்ண முடியாது. | ✅ I cannot do this. |
| 13 | Let’s talk about this tomorrow. | இதைப் பற்றி நாளைக்குக் கதைப்போம். | ✅ Let's talk about it tomorrow. | இதைப் பத்தி நாளைக்குப் பேசலாம். | ✅ We can talk about it tomorrow. |
| 14 | Who were you talking to? | நீங்கள் ஆரோட கதைச்சீங்கள்? | ❌ What is your story? | நீங்க யார்கிட்ட பேசுனீங்க? | ❌ What did you talk to? |
| 15 | That girl sings well. | அந்தப் பெட்டை நல்லாப் பாடுறாள். | ✅ The female is singing well. | அந்தப் பொண்ணு நல்லாப் பாடுறா. | ✅ The girl is singing well. |
| 16 | This flower is beautiful. | இந்தப் பூ வடிவா இருக்கு. | ❌ It looks like a flower. | இந்தப் பூ அழகா இருக்கு. | ✅ This flower is beautiful. |
| 17 | Please come here. | இங்க வாங்கோ. | ✅ Come here. | இங்க வாங்க. | ✅ Come here. |
| 18 | Please sit down. | இருங்கோ. | ❌ Iruno. | உக்காருங்க. | ✅ Sit down. |
| 19 | Please give me that book. | அந்தப் புத்தகத்தை எனக்குத் தாங்கோ. | ✅ Please give me the book. | அந்தப் புத்தகத்தை எனக்குக் குடுங்க. | ✅ Please give me the book. |
| 20 | Yes, that boy is my younger brother. | ஓம், அந்தப் பெடியன் என்ர தம்பி. | 🟡 Om, that boy is my younger brother. | ஆமா, அந்தப் பையன் என்னோட தம்பி. | ✅ Yes, that boy is my younger brother. |



## Observations

- The dialect gap widened on the harder set: SL 6/10 → 12/20 and TN 8/10 →
  17/20 when the examples grew from 10 to 20
- **வடிவா** is a confirmed vocabulary hole — the model knows அழகா but not
  the SL word for beautiful; it fails in both contexts (rows 7 and 16)
- **The கதை root is context-dependent**: கதைப்போம் (future, row 13) →
  "talk" ✅, but கதைக்க (infinitive, row 2) and கதைச்சீங்கள் (past,
  row 14) → "story" ❌
- **When it doesn't know a word, it transliterates instead of translating**:
  இருங்கோ → "Iruno" (row 18), ஓம் → "Om" (row 20)
- பெட்டை (SL "girl") → "female" (row 15) — a literal but defensible gloss
- SL vocabulary the model handles fine: இண்டைக்கு, ஏலாது/ஏலுமா, தாங்கோ,
  வாங்கோ, குசினி, என்ர
- Both-dialect failures — model limitations, not dialect gaps: row 6
  (reads எங்க "where" as "what") and row 14 (the "who" is lost in both,
  though the SL miss is much worse)
- Greedy decoding makes every run identical, so this is a stable baseline

## Conclusion

The model handles Tamil Nadu Tamil well but is noticeably weaker on Sri
Lankan Tamil — the misses cluster on SL-specific vocabulary (வடிவா,
கதைக்க, இருங்கோ) while shared grammar and common SL words pass. It is a
vocabulary gap, not a grammar gap.

The likely cause is training data: Agaram's pretraining is ~58% Tamil, but
the model card doesn't break that down by dialect — and web text, where
TN usage dominates, leaves SL-specific words rare enough to go unlearned.
The fallbacks we observed (transliterating unknown words as "Iruno" and
"Om", reading கதைக்க through its TN meaning "tell a story") are classic
low-frequency behavior.

Practically: the model is fine for TN Tamil chat and translation —
double-check anything in SL Tamil. Closing the gap needs more SL Tamil
text in training; dialects that live mostly in speech and diaspora print
are hard to learn from the web alone.

## Credits

- **Model** — [Agaram 2.5B](https://huggingface.co/murai-labs/agaram-2.5b-instruct) by Murai Labs and [Ramchand Kumaresan](https://www.ramchandk.com/) ([@Mechramc](https://x.com/Mechramc)) · [Ollama GGUF build](https://huggingface.co/murai-labs/agaram-2.5b-gguf) · [code](https://github.com/Murai-Labs/Agaram2.5b) · [paper](https://arxiv.org/abs/2610.18420)
- **App** — built with OpenCode + GLM 5.3
