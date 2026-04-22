"""
Pinecone Seeder for CandleKeep Customer Support (v2)
=====================================================
Seeds CandleKeep-specific FAQ data into Pinecone.

Usage:
    pip install pinecone openai python-dotenv
    python v2/seed/seed-pinecone.py

Keys are loaded automatically from v2/.env

This script:
1. Loads FAQ data from faq-data.json (20 CandleKeep FAQs)
2. Generates embeddings via Nebius Token Factory (OpenAI-compatible)
3. Upserts vectors into Pinecone index 'support-faq' namespace 'faq'
"""

import json
import os
import sys
import time

# ─── Load .env file automatically ────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # env_path = os.path.join(script_dir, "..", ".env")
    load_dotenv()
    print(f"📂 Loaded .env from {os.path.abspath('.env')}")
except ImportError:
    print("⚠️  python-dotenv not installed — falling back to environment variables")
    print("   Install it with: pip install python-dotenv")

try:
    from pinecone import Pinecone, ServerlessSpec
except ImportError:
    print("❌ Missing dependency. Run: pip install pinecone")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("❌ Missing dependency. Run: pip install openai")
    sys.exit(1)

# ─── Configuration ────────────────────────────────────────────────────────────

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")
NEBIUS_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
EMBEDDING_MODEL = "BAAI/bge-en-icl"
PINECONE_INDEX = "support-faq"
EMBEDDING_DIMENSION = 768  # Truncated from 4096 (Matryoshka) — better semantic precision

if not PINECONE_API_KEY:
    print("❌ Set PINECONE_API_KEY in v2/.env")
    sys.exit(1)

if not NEBIUS_API_KEY:
    print("❌ Set NEBIUS_API_KEY in v2/.env")
    sys.exit(1)

# ─── Initialize Clients ──────────────────────────────────────────────────────

print("🔧 Initializing clients...")

pc = Pinecone(api_key=PINECONE_API_KEY)

nebius = OpenAI(
    api_key=NEBIUS_API_KEY,
    base_url=NEBIUS_BASE_URL,
)

# ─── Create Index (if it doesn't exist) ──────────────────────────────────────

existing_indexes = [idx.name for idx in pc.list_indexes()]

if PINECONE_INDEX not in existing_indexes:
    print(f"📦 Creating Pinecone index '{PINECONE_INDEX}'...")
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print("⏳ Waiting for index to be ready...")
    time.sleep(10)
else:
    print(f"✅ Index '{PINECONE_INDEX}' already exists")

index = pc.Index(PINECONE_INDEX)

# ─── Helper: embed and upsert a dataset ──────────────────────────────────────

def embed_and_upsert(data, namespace, text_fn, metadata_fn, label):
    """Embed a list of records and upsert into a Pinecone namespace."""
    print(f"\n{'='*60}")
    print(f"📄 Seeding {len(data)} {label} entries → namespace '{namespace}'")
    print(f"{'='*60}")

    vectors = []

    for i, record in enumerate(data):
        text = text_fn(record)
        print(f"  🔢 Embedding [{i+1}/{len(data)}]: {text[:60]}...")

        response = nebius.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL,
        )

        embedding = response.data[0].embedding[:EMBEDDING_DIMENSION]

        vectors.append({
            "id": record["id"],
            "values": embedding,
            "metadata": metadata_fn(record),
        })

        time.sleep(0.2)  # rate limit

    # Upsert in batches of 100
    BATCH_SIZE = 100
    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i : i + BATCH_SIZE]
        index.upsert(vectors=batch, namespace=namespace)
        print(f"  ✅ Upserted batch {i // BATCH_SIZE + 1} ({len(batch)} vectors)")

    return len(vectors)

# ─── Load & Seed FAQ Data ────────────────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))

faq_path = os.path.join(script_dir, "faq-data.json")
with open(faq_path, "r") as f:
    faq_data = json.load(f)

faq_count = embed_and_upsert(
    data=faq_data,
    namespace="faq",
    text_fn=lambda r: f"Question: {r['question']}\nAnswer: {r['answer']}",
    metadata_fn=lambda r: {
        "question": r["question"],
        "answer": r["answer"],
        "category": r.get("category", "general"),
        "text": f"Question: {r['question']}\nAnswer: {r['answer']}",
    },
    label="CandleKeep FAQ",
)

# ─── Verify ──────────────────────────────────────────────────────────────────

time.sleep(2)  # wait for index to update
stats = index.describe_index_stats()
host = pc.describe_index(PINECONE_INDEX).host

print(f"\n{'='*60}")
print(f"🎉 Done! Index stats:")
print(f"   Index: {PINECONE_INDEX}")
print(f"   Host:  {host}")
print(f"   Dimension: {stats.dimension}")
print(f"   Total vectors: {stats.total_vector_count}")
print(f"   Namespaces:")
for ns_name, ns_info in stats.namespaces.items():
    print(f"     '{ns_name}': {ns_info.vector_count} vectors")
print(f"\n⚠️  Update the Pinecone host URL in your n8n workflow:")
print(f"   https://{host}/query")
print(f"\n✅ Pinecone is ready. You can now activate your n8n workflow!")
