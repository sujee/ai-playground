"""Sri Lankan Tamil vs Tamil Nadu Tamil — Agaram 2.5B experiment.

For each example in sl-vs-tn-examples.json (id, english, sl_tamil,
tn_tamil, optional difference note), print the English meaning, then ask
the Agaram 2.5B chat model — served locally through Ollama — to explain
each Tamil variation in English. Every answer is auto-graded against the
expected meaning (✅ correct, 🟡 partial, ❌ wrong), and a summary table
is printed at the end.

Model card: https://huggingface.co/murai-labs/agaram-2.5b-instruct
(greedy decoding, no system prompt, up to 512 new tokens)

Usage:
    ollama pull hf.co/murai-labs/agaram-2.5b-gguf:Q8_0   # once
    uv run sl-vs-tn-tamil.py
"""

import json
import re
from pathlib import Path

from ollama import chat

MODEL = "hf.co/murai-labs/agaram-2.5b-gguf:Q8_0"
DATA_PATH = Path(__file__).resolve().parent / "sl-vs-tn-examples.json"
PROMPT = "Explain the meaning of this sentence in English: {sentence}"

# The two Tamil variations tested per example.
VARIATIONS = (
    ("Sri Lankan Tamil", "sl_tamil"),
    ("Tamil Nadu Tamil", "tn_tamil"),
)

# --- auto-grading: keyword overlap between expected and actual English ---
# A simple heuristic, not a judge.

# Canonical word -> the words that count as it.
SAME_AS = {
    "yes": "oh yeah",
    "mom": "mother",
    "eat": "eaten ate eating",
    "cannot": "can't cant",
    "need": "want",  # Tamil வேணும் means both want and need
    "who": "whom",
    "talk": "talking talked talks",
    "sing": "singing sings sang",
    "come": "coming comes came",
    "go": "going goes went",
    "look": "looking looks looked",
}
LEMMAS = {word: canon for canon, words in SAME_AS.items() for word in words.split()}
STOPWORDS = set(
    """
    i you me we my your our the a an is are am was were be been being to in
    on at of for with it its this that these those do does did have has had
    having will would shall should can may might must and or but not so very
    some please give let's
    """.split()
)
QUESTION_WORDS = {"what", "where", "when", "who", "why", "how"}


def content_words(text: str) -> set[str]:
    """Lowercased words, lemmas applied, framing stopwords removed."""
    words = re.findall(r"[a-z']+", text.lower().replace("’", "'"))
    return {LEMMAS.get(word, word) for word in words} - STOPWORDS


def grade(expected: str, answer: str) -> str:
    """Auto-grade an answer against the expected meaning: ✅ 🟡 ❌."""
    exp, ans = content_words(expected), content_words(answer)
    if not exp:
        return "❔"
    score = len(exp & ans) / len(exp | ans)  # keyword overlap (Jaccard)
    if exp & QUESTION_WORDS != ans & QUESTION_WORDS:
        score *= 0.5  # a different question word asks a different question
    if score >= 0.75:
        return "✅"
    if score >= 0.4:
        return "🟡"
    return "❌"


def explain(sentence: str) -> str:
    """Ask the chat model what a Tamil sentence means, in English."""
    response = chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT.format(sentence=sentence)}],
        options={"temperature": 0, "num_predict": 512},  # greedy decoding
    )
    return response.message.content.strip()


def one_line(text: str, limit: int = 60) -> str:
    """Collapse an answer to one line, truncated for the summary table."""
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def print_summary(results: list[tuple]) -> None:
    """Print a markdown summary table: English, Tamil, and graded answers."""
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print("| # | English meaning | Sri Lankan Tamil | Model said (SL) | Tamil Nadu Tamil | Model said (TN) |")
    print("|---|---|---|---|---|---|")
    for i, (example, answers) in enumerate(results, start=1):
        meaning = one_line(example["english"]).replace("|", "\\|")
        cells = [meaning]
        for label, key in VARIATIONS:
            answer, verdict = answers[label]
            sentence = one_line(example[key]).replace("|", "\\|")
            reply = one_line(answer).replace("|", "\\|")
            cells.append(sentence)
            cells.append(f"{verdict} {reply}")
        print(f"| {i} | {' | '.join(cells)} |")
    print()
    for label, _ in VARIATIONS:
        correct = sum(1 for _, answers in results if answers[label][1] == "✅")
        print(f"{label}: {correct}/{len(results)} ✅")
    print()
    print("✅ correct · 🟡 partial · ❌ wrong (auto-graded by keyword overlap)")


def main() -> None:
    examples = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    print(f"Using Ollama model: {MODEL}")
    print(f"Loaded {len(examples)} examples from {DATA_PATH.name}\n")

    results: list[tuple] = []  # (example, {label: (answer, verdict)})
    for i, example in enumerate(examples, start=1):
        print("=" * 72)
        print(f"Example {example.get('id', i)}/{len(examples)} — English meaning: {example['english']}")
        if example.get("difference"):
            print(f"Difference: {example['difference']}")
        print("=" * 72)
        answers: dict[str, tuple[str, str]] = {}
        for label, key in VARIATIONS:
            answer = explain(example[key])
            verdict = grade(example["english"], answer)
            answers[label] = (answer, verdict)
            print(f"\n{label}: {example[key]}")
            print(f"Model says: {verdict} {answer}")
        results.append((example, answers))
        print()

    print_summary(results)


if __name__ == "__main__":
    main()
