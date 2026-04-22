# Architecture Customer support agent

- [Architecture Customer support agent](#architecture-customer-support-agent)
  - [Workflow](#workflow)
  - [Order Database](#order-database)


## Workflow

This is the workflow.

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

## Order Database

We approximate an order database lookup by reading data from a Google spreadsheet.

It has the following attributes

| Column                   | Description                               |
| ------------------------ | ----------------------------------------- |
| Request Text             | Customer's message                        |
| Submission Channel       | Website, Mobile App, External Marketplace |
| Order ID                 | 6-digit order number                      |
| Timestamp                | When request was received                 |
| Order History            | Pipe-separated timeline of order events   |


