# Playing with Agaram Tamil Model

## Pointers

Announcements:
- https://x.com/Mechramc/status/2115426441764499947
- https://x.com/Mechramc/status/2115810213836013699

Project pointers:
- Weights: [http://huggingface.co/murai-labs](https://t.co/TzNRnEO1gE) 
- GGUF (llama.cpp): [http://huggingface.co/murai-labs/agaram-2.5b-gguf](https://t.co/PtOj7AH91b) 
- Code: [http://github.com/Murai-Labs/Agaram2.5b](https://t.co/aqwCKkLpsa) 
- Paper: [http://arxiv.org/abs/2610.18420](https://t.co/GBgleDor7U)

## Setup

```bash
ollama run hf.co/murai-labs/agaram-2.5b-gguf:Q8_0
```

## Chat Transcript

```text
>>> how are you?
I am doing well, thank you for asking! How can I help you today?

>>> eppadi suham?
I'm doing great! I'm here to help you with anything you need.

>>> eppadi suham? answer in tamil
நான் நல்லா இருக்கேன். உங்களுக்கு என்ன உதவி வேணும்னு சொல்லுங்க, நான் பண்றேன்.

>>> எப்படி சுஹம் ?
எப்படி இருக்கீங்க? நான் நல்லா இருக்கேன். உங்களுக்கு என்ன வேணும்னு சொல்லுங்க, நான் பண்றேன்.


>>> write me a poem about cats
நிச்சயமாக! இதோ ஒரு குட்டி கவிதை:

வீட்டின் காவலன்,
வெயிலில் உழைக்கும் நண்பன்,
அன்பான நண்பன்,
என் செல்லக்குட்டி!

>>> """ Explain the meaning of this sentence in English:
... “அந்தப் பெடியன் வடிவா கதைக்கிறான்.”
"""
The boy is speaking in a very formal way.

>>> """ Explain the meaning of this sentence in English:
அந்தப் பையன் அழகா பேசுறான்.
"""
The boy is speaking in a very formal way.
```

## Sri Lankan Tamil vs Tamil Nadu Tamil Experiment :-)

The same meaning, said two ways — a few samples:

| # | English | Sri Lankan Tamil | Tamil Nadu Tamil | Difference |
|---|---|---|---|---|
| 1 | Yes, I know. | ஓம், எனக்குத் தெரியும். | ஆமா, எனக்குத் தெரியும். | ஓம் / ஆமா: yes |
| 2 | I need to talk to you. | நான் உங்களோட கதைக்க வேணும். | நான் உங்ககிட்ட பேசணும். | கதைக்க / பேச: to talk |
| 7 | It looks beautiful. | அது வடிவா இருக்கு. | அது அழகா இருக்கு. | வடிவா / அழகா: beautiful in this context |

Full dataset (all 20 sentences): [sl-vs-tn-examples.json](sl-vs-tn-examples.json)

Experiment write-up and results: [srilankan-vs-tamil-nadu-tamil.md](srilankan-vs-tamil-nadu-tamil.md)
