# Customer Support Multi-Agent v2

A multi-agent AI customer support system built with **n8n** and **Nebius Token Factory**. This version implements a two-agent architecture with **FAQ matching** and **order history lookup**.

- [Customer Support Multi-Agent v2](#customer-support-multi-agent-v2)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Tech Stack](#tech-stack)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Test](#test)


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

## Architecture

See [architecture](architecture.md)

---

## Tech Stack

| Component                | Detail                                     | Free tier? |
| ------------------------ | ------------------------------------------ | ---------- |
| **n8n**                  | Workflow engine — n8n Cloud or self-hosted | ✅         |
| **Nebius Token Factory** | LLM `Llama-3.3-70B-Instruct` + embeddings  | ✅         |
| **Pinecone**             | Vector database for FAQ search             | ✅         |
| **Google Sheets**        | Cloud-hosted order data                    | ✅         |

---


## Prerequisites

You will need 

- [N8N account](https://n8n.io/) (free tier is fine)
- [Nebius Token factory](https://tokenfactory.nebius.com/) account (free tier is fine)
- a Google account (free tier is fine)
- Details of Pinecone database (you will be provided this during the class) 

## Getting Started

See [getting started](getting-started.md)

---

## Test

[test workflow](test-workflow.md)

---

