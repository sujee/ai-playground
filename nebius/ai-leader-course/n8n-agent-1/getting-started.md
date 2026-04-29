# Getting Started

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Step 1: Get Nebius Token Factory details](#step-1-get-nebius-token-factory-details)
  - [Step 2: Login to N8N](#step-2-login-to-n8n)
  - [Step 3: Add Nebius Token Factory to N8N](#step-3-add-nebius-token-factory-to-n8n)
  - [Step 4: Import the workflow into N8N](#step-4-import-the-workflow-into-n8n)
  - [Step 5: Publish the n8n workflow](#step-5-publish-the-n8n-workflow)
  - [Step 6: Test the workflow](#step-6-test-the-workflow)
  - [Step 7: Let's send a request](#step-7-lets-send-a-request)
    - [Billing](#billing)
    - [Tech Support](#tech-support)
    - [Try a different query](#try-a-different-query)


## Prerequisites

You will need 

- [N8N account](https://n8n.io/) (free tier is fine)
- [Nebius Token factory](https://tokenfactory.nebius.com/) account (free tier is fine)



## Step 1: Get Nebius Token Factory details

- Create an account or sign into your account at [Nebius Token Factory](https://tokenfactory.nebius.com/)
- Create an API key and save this for later
- Also save this API url:  `https://api.tokenfactory.nebius.com/v1`
- And we will use this model : `Qwen/Qwen3-30B-A3B-Instruct-2507`

## Step 2: Login to N8N

Sign up / login to your [n8n](https://n8n.io/) account.


## Step 3: Add Nebius Token Factory to N8N

- In [n8n](https://n8n.io/) , go to **personal --> credentials --> create credential**
- Choose **openAI** as a provider
- - Name: `Nebius Token Factory`
- Base URL: `https://api.tokenfactory.nebius.com/v1`
- API Key: Your Nebius API key

## Step 4: Import the workflow into N8N

- In [n8n](https://n8n.io/) , go to **Workflows -->  create a new workflow**
- Click on **...** and choose import from file
- Select this file [customer-support-starter-agent.json](customer-support-starter-agent.json)


## Step 5: Publish the n8n workflow

## Step 6: Test the workflow

Let's go to testing it!

- Open 'web hook' node
- select **production**
- Note the URL

ON your terminal set this 

```bash
export AGENT_URL='your production url here'

# eg. : 
# export AGENT_URL='https://your_path.app.n8n.cloud/webhook/customer-support1-starter'
```

## Step 7: Let's send a request

### Billing

```bash
curl -s -X POST "$AGENT_URL" \
  -H "Content-Type: application/json" \
  -d '{ "query": "I was charged twice this month" }' 
```

Response should be

```json
{
  "query": "I was charged twice this month",
  "department": "billing"
}
```

### Tech Support

```bash
curl -s -X POST "$AGENT_URL" \
  -H "Content-Type: application/json" \
  -d '{  "query": "I need to reset my account password" }' 
```

Response should be

```json
{
  "query": "I need to reset my account password",
  "department": "support"
}
```

### Try a different query

Experiment with different queries.

```bash
curl -s -X POST "$AGENT_URL" \
  -H "Content-Type: application/json" \
  -d '{  "query": "I need to talk to a sales person" }' 
```

