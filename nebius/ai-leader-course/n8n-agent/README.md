# 🎫 CandleKeep Customer Support Multi-Agent v2

A multi-agent AI customer support system built with **n8n** and **Nebius Token Factory**. This version implements a two-agent architecture with **FAQ matching** and **order history lookup**.

This is **v2** — with two workflow variants:

- **Excel version**: Reads order data from local `CandleKeep Data.xlsx`
- **Google Sheets + FAQ version**: Reads from Google Sheets + FAQ search via Pinecone

---

## Architecture (Google Sheets + FAQ)

```
  Webhook (User Message)
         │
         ▼
  ┌─────────────┐
  │ Preprocess  │  ◄── Extract order ID, ticket ID, channel
  └─────────────┘
         │
         ▼
  ┌─────────────────┐
  │ Has Order ID?   │
  └─────────────────┘
         │
    ┌────┴────┐
    │         │
   YES        NO
    │         │
    │         ▼
    │   ┌───────────────┐
    │   │ Embed Query   │  ◄── Nebius embeddings
    │   └───────────────┘
    │         │
    │         ▼
    │   ┌───────────────┐
    │   │ FAQ Search    │  ◄── Pinecone vector search
    │   └───────────────┘
    │         │
    │    ┌────┴────┐
    │    │         │
    │  Match    No Match
    │  ≥0.65       │
    │    │         │
    │    ▼         │
    │  ┌───────┐   │
    │  │Return │   │
    │  │ FAQ   │   │
    │  └───────┘   │
    │              │
    └──────┬───────┘
           │
           ▼
  ┌──────────────────┐
  │ Read Google Sheet│  ◄── Order history data
  └──────────────────┘
           │
           ▼
  ┌─────────────────┐
  │ Lookup Order    │  ◄── Find matching order by ID
  └─────────────────┘
           │
           ▼
  ┌─────────────────────┐
  │ 🤖 Coordinator Agent│
  │  • Sentiment        │
  │  • Category         │
  │  • Department       │
  │  • Recognized?      │
  └─────────────────────┘
           │
    ┌──────┴──────┐
    │             │
Recognized   Unrecognized
    │             │
    ▼             ▼
┌───────────┐  ┌────────────┐
│Resolution │  │ Manual     │
│  Agent    │  │ Queue      │
└───────────┘  └────────────┘
    │
┌───┴───┐
│       │
High   Low
│       │
▼       ▼
Auto   Manual
```

---

## Features

| Feature                      | Description                                                      |
| ---------------------------- | ---------------------------------------------------------------- |
| **FAQ Matching**             | General queries matched against Pinecone FAQ database            |
| **Two-Agent System**         | Coordinator for triage, Resolution for responses                 |
| **Sentiment Analysis**       | Detects positive, neutral, or negative tone                      |
| **Department Routing**       | Routes to Logistics, Returns, Customer Support, Product, Billing |
| **Order History Enrichment** | Reads order data when order ID is detected                       |
| **Confidence-Based Routing** | Auto-send high/medium confidence, manual queue for low           |
| **Google Sheets**            | Cloud-hosted order data (easy to update)                         |

---

## Tech Stack

| Component                | Detail                                     | Free tier? |
| ------------------------ | ------------------------------------------ | ---------- |
| **n8n**                  | Workflow engine — n8n Cloud or self-hosted | ✅         |
| **Nebius Token Factory** | LLM `Llama-3.3-70B-Instruct` + embeddings  | ✅         |
| **Pinecone**             | Vector database for FAQ search             | ✅         |
| **Google Sheets**        | Cloud-hosted order data                    | ✅         |

---

## Data Source

The workflow reads directly from **CandleKeep Data.xlsx** with two sheets:

### Sheet 1: Ground Truth (input + human output)

| Column                   | Description                               |
| ------------------------ | ----------------------------------------- |
| Request Text             | Customer's message                        |
| Submission Channel       | Website, Mobile App, External Marketplace |
| Related to order         | yes / no / -                              |
| Order ID                 | 6-digit order number                      |
| Category                 | Order Issue, Delivery, Payment, etc.      |
| Routing to Department    | Logistics, Customer Support, Returns      |
| Timestamp                | When request was received                 |
| Order History            | Pipe-separated timeline of order events   |
| [Human] Initial Response | Human agent's response (ground truth)     |

### Sheet 2: Agent output + artifacts

Used for comparing agent responses against human ground truth.

---

## Setup

### 1 — Seed Pinecone FAQ Data

Run this locally (one-time setup) to populate the FAQ vectors:

```bash
pip install pinecone openai python-dotenv

export NEBIUS_API_KEY=your-nebius-api-key
export PINECONE_API_KEY=your-pinecone-api-key

python seed/seed-pinecone.py
```

This creates the `support-faq` index with 20 CandleKeep FAQs. **Copy the Host URL** from the output — you'll need it in step 4.

### 2 — Import Workflow in n8n

1. Open **n8n** (Cloud or self-hosted)
2. Go to **Workflows → Import from File**
3. Select `workflow/customer-support-multi-agent-v3.json`

### 3 — Configure Credentials

Create these credentials in n8n:

**Nebius Token Factory** (OpenAI API type):

- Name: `Nebius Token Factory`
- Base URL: `https://api.tokenfactory.nebius.com/v1`
- API Key: Your Nebius API key

**Pinecone API**:

- Name: `Pinecone API`
- API Key: Your Pinecone API key

**Google Sheets OAuth2**:

- Follow n8n's Google OAuth setup guide

### 4 — Set Pinecone Host URL

**n8n Cloud:** Go to **Settings → Variables** and create:

- **Key**: `PINECONE_HOST`
- **Value**: `your-index-host.svc.xxx.pinecone.io` (from seed output)

**Docker:** Add to `v2/.env`:

```
PINECONE_HOST=your-index-host.svc.xxx.pinecone.io
```

### 5 — Activate & Test

Toggle the workflow **Active**, then test with your webhook URL:

```bash
# Test FAQ query (no order ID)
curl -s -X POST YOUR_WEBHOOK_URL/webhook/support-ticket-v2-gsheet \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}' | jq .

# Test with order ID (goes to order flow)
curl -s -X POST YOUR_WEBHOOK_URL/webhook/support-ticket-v2-gsheet \
  -H "Content-Type: application/json" \
  -d '{"query": "Where is my order 542417?"}' | jq .
```

Or run the full test suite:

```bash
chmod +x test/test-workflow.sh
./test/test-workflow.sh
```

---

## Workflow Nodes

| #   | Node                | Type         | Purpose                                             |
| --- | ------------------- | ------------ | --------------------------------------------------- |
| 1   | User Message        | Webhook      | Receives POST `{"query": "...", "order_id": "..."}` |
| 2   | Preprocessing       | Code         | Extracts order ID, generates ticket ID              |
| 3   | Read Excel File     | Read/Write   | Loads binary Excel file                             |
| 4   | Extract from XLSX   | Extract      | Parses Excel into JSON rows                         |
| 5   | Merge Data          | Merge        | Combines preprocessing + order data                 |
| 6   | Merge Order History | Code         | Finds matching order by ID                          |
| 7   | Coordinator Agent   | HTTP Request | LLM analyzes sentiment, category, routing           |
| 8   | Parse Coordinator   | Code         | Extracts JSON from LLM response                     |
| 9   | Recognized?         | If           | Routes unrecognized to manual queue                 |
| 10  | Resolution Agent    | HTTP Request | LLM generates personalized response                 |
| 11  | Parse Resolution    | Code         | Extracts response + confidence                      |
| 12  | Confidence?         | If           | Routes low confidence to manual queue               |
| 13  | Response Nodes      | Respond      | Returns final response to webhook caller            |

---

## API Request Format

```json
{
 "query": "Customer's message here",
 "order_id": "770487", // Optional - 6 digit order ID
 "channel": "Website", // Optional - Website, Mobile App, External Marketplace
 "email": "customer@example.com" // Optional
}
```

---

## Example Responses

### ✅ Resolved (High Confidence)

```json
{
 "ticket_id": "TKT-1739712345678",
 "order_id": "770487",
 "status": "resolved",
 "sentiment": "negative",
 "category": "Order Inquiry",
 "department": "Logistics",
 "resolution": "Hi there — thanks for reaching out. I've reviewed your order #770487 and can see from the history that it was shipped via DPD on September 26th. The tracking shows it was delivered on September 30th. I notice you previously contacted us about a wrong size issue — if that's still unresolved, please let me know and I'll prioritize getting that sorted for you.",
 "action_items": ["Verify delivery status", "Follow up on size issue"],
 "confidence_level": "high",
 "confidence_score": 0.85,
 "resolved_at": "2026-02-16T19:45:00.000Z"
}
```

### ⏳ Manual Queue (Low Confidence)

```json
{
 "ticket_id": "TKT-1739712345679",
 "status": "manual_processing",
 "resolution": "Thank you for contacting CandleKeep support. Your request has been received and a member of our team will follow up shortly.",
 "escalation_needed": true,
 "escalation_reason": "Low confidence - requires human review",
 "confidence_level": "low"
}
```

### 🚫 Unrecognized Request

```json
{
 "ticket_id": "TKT-1739712345680",
 "status": "manual_processing",
 "resolution": "This request requires manual processing by a human agent. Your ticket has been forwarded to our support team.",
 "escalation_needed": true,
 "escalation_reason": "Unrecognized request"
}
```

---

## Project Structure

```
v2/
├── .env.example                                    ← API key template
├── .env                                            ← Your API keys (git-ignored)
├── docker-compose.yml                              ← n8n on port 5679
├── README.md                                       ← This file
├── data/
│   ├── CandleKeep Data.xlsx                        ← Order history (Excel)
│   └── test-cases.json                             ← Test cases for evaluation
├── seed/
│   ├── faq-data.json                               ← CandleKeep FAQ data (20 items)
│   └── seed-pinecone.py                            ← Seeds FAQ to Pinecone
├── workflow/
│   ├── customer-support-multi-agent.json           ← Excel workflow
│   └── customer-support-multi-agent-gsheet.json    ← Google Sheets + FAQ workflow
└── test/
    └── test-workflow.sh                            ← Test suite
```

---

## Example Responses

### ✅ FAQ Match

```json
{
 "ticket_id": "TKT-1740000000000",
 "status": "resolved",
 "source": "faq",
 "original_query": "What is your return policy?",
 "category": "returns",
 "resolution": "CandleKeep offers a 30-day return policy on all furniture items. Items must be unused, in original packaging, and with all tags attached...",
 "faq_question": "What is CandleKeep's return policy?",
 "faq_score": 0.92,
 "confidence_level": "high"
}
```

### ✅ Order Resolved (High Confidence)

```json
{
 "ticket_id": "TKT-1739712345678",
 "order_id": "770487",
 "status": "resolved",
 "sentiment": "negative",
 "category": "Order Inquiry",
 "department": "Logistics",
 "resolution": "Hi there — thanks for reaching out. I've reviewed your order #770487...",
 "confidence_level": "high",
 "confidence_score": 0.85
}
```

### ⏳ Manual Queue (Low Confidence / Unrecognized)

```json
{
 "ticket_id": "TKT-1739712345680",
 "status": "manual_processing",
 "resolution": "This request requires manual processing by a human agent.",
 "escalation_needed": true,
 "escalation_reason": "Unrecognized request"
}
```

---

## Troubleshooting

| Issue                    | Fix                                                                 |
| ------------------------ | ------------------------------------------------------------------- |
| Webhook returns 404      | Toggle the workflow **Active** in n8n                               |
| 401 from Nebius          | Check OpenAI credential in n8n (Credentials → Nebius Token Factory) |
| FAQ not matching         | Run `python seed/seed-pinecone.py` to seed FAQ data                 |
| Pinecone 401             | Check `PINECONE_API_KEY` in `.env`                                  |
| Order not found          | Ensure order ID exists in data source (Excel or Google Sheet)       |
| Google Sheets 404        | Check Sheet ID and gid in workflow, verify OAuth2 credential        |
| All queries go to manual | Check Pinecone index has data, verify FAQ score threshold (≥0.75)   |
| Node shows `?` icon      | Wrong node version — re-import the workflow                         |
| Port 5679 in use         | Stop conflicting service or change port in `docker-compose.yml`     |

---

## Differences from v1

| Aspect        | v1 (Root folder)        | v2 (This folder)                      |
| ------------- | ----------------------- | ------------------------------------- |
| Data source   | Pinecone (FAQ + KB)     | Google Sheets + Pinecone (FAQ only)   |
| FAQ data      | Generic SaaS product    | CandleKeep furniture-specific         |
| Order history | None                    | Google Sheets lookup                  |
| Port          | 5678                    | 5679                                  |
| Agents        | 2 (Triage + Resolution) | 2 (Coordinator + Resolution)          |
| Flow          | FAQ → Agent             | Order ID check → FAQ fallback → Agent |
