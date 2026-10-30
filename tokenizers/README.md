# Tokenizers

## Setup

```bash
uv  sync
```

## Intro

Imagine you want to teach a computer to understand English. You can't just feed it raw text; it needs to be broken down into smaller, manageable chunks. This is where **tokenizers** come in. They are the essential preprocessing tools that transform raw text into numerical representations that LLMs (Large Language Models) can understand and process.

Think of a tokenizer as a translator between human language and machine code. It takes a sentence like "The quick brown fox jumps over the lazy dog" and breaks it down into individual units called **tokens**. These tokens can be:

* **Words:** This is the simplest approach, where each word becomes a token ("the", "quick", "brown", etc.).
* **Subwords:** Words are broken down into smaller subword units (e.g., "unhappi" and "ness" instead of "unhappiness"). This helps with handling rare words or out-of-vocabulary terms.
* **Characters:** Each individual character becomes a token.



Here's a long sentence and examples of how different tokenization methods would break it down:

**Sentence:** "The quick brown fox jumps over the lazy dog, but the cunning cat stealthily observes from atop a bookshelf."


**1. Word-based Tokenization:**

["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "but", "the", "cunning", "cat", "stealthily", "observes", "from", "atop", "a", "bookshelf"]

**2. Subword Tokenization (e.g., BPE):**

["The", "quick", "brown", "fox", "jump", "##s", "over", "the", "lazy", "dog", ",", "but", "the", "cunning", "cat", "stealth", "##ily", "observe", "##s", "from", "ato", "##p", "a", "bookshelf"]

Notice how words like "jumps" and "stealthily" are broken down into smaller, more frequent subword units. 

**3. Character-based Tokenization:**

["T", "h", "e", " ", "q", "u", "i", "c", "k", " ", "b", "r", "o", "w", "n", " ", "f", "o", "x", " ", "j", "u", "m", "p", "s", " ", "o", "v", "e", "r", " ", "t", "h", "e", " ", "l", "a", "z", "y", " ", "d", "o", "g", ",", " ", "b", "u", "t", " ", "t", "h", "e", " ", "c", "u", "n", "n", "i", "n", "g", " ", "c", "a", "t", " ", "s", "t", "e", "a", "l", "t", "h", "i", "l", "y", " ", "o", "b", "s", "e", "r", "v", "e", "s", " ", "f", "r", "o", "m", " ", "a", "t", "o", "p", " ", "a", " ", "b", "o", "o", "k", "s", "h", "e", "l", "f", "."]

This approach treats each individual character as a token.

The choice of tokenization method depends on the specific LLM architecture and the task at hand.


**Why are tokenizers so important?**

1. **Input Formatting:** LLMs expect input in a standardized numerical format. Tokenizers convert text into sequences of numbers representing each token, allowing the model to understand the structure and meaning of the input.
2. **Vocabulary Management:** By breaking down words into subword units, tokenizers can handle a vast vocabulary without needing massive lookup tables for every single word. This makes LLMs more efficient and scalable.
3. **Contextual Understanding:** Some advanced tokenizers consider the context of words when assigning tokens, allowing for better understanding of nuanced language and relationships between words.

**Examples of Tokenizers:**

* **WordPiece:** Used by BERT and other popular models, it breaks down words into subword units based on frequency statistics.
* **Byte Pair Encoding (BPE):** Similar to WordPiece, but learns subword units iteratively by merging frequent character pairs.
* **SentencePiece:** A versatile tokenizer that can handle various languages and tokenization strategies.

## Code

Run [tokenizer.ipynb](tokenizer.ipynb)
