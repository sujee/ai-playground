# Seeding the FAQ data to pinecone


## Prerequisites

- Pinecone API Key.  Get it at [https://app.pinecone.io/](https://app.pinecone.io/)
- Nebius API Key.  Get it at [tokenfactory.nebius.com](https://tokenfactory.nebius.com/models)

## Setup .env file

Create an `.env` with this content:

```text
PINECONE_API_KEY = your pine cone key here
NEBIUS_API_Key = your api key goes here
```

## Setup Python env

### Option 1 - (Recommended) Using `uv`

```bash
uv venv --seed --python 3.12
source .venv/bin/activate
uv pip  install pinecone openai python-dotenv
```

### Option 2 - Using plain python

TODO

## Import the data into Pinecone

```bash
 uv run python seed-pinecone.py
 # or 
# python seed-pinecone.py
```

After the run is sucessfully completed, you will see a message like this

```text
Done! Index stats:
   Index: support-faq
   Host:  HOST-NAME.pinecone.io
   Dimension: 256
   Total vectors: 44
   Namespaces:
     'kb': 29 vectors
     'faq': 15 vectors

⚠️  Update the Pinecone host URL in your n8n workflow:
   https://HOST-NAME.pinecone.io/query
```

Make a note of the `https://HOST-NAME.pinecone.io/query`