# Getting Started

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Step 1: FAQ database (Pinecone)](#step-1-faq-database-pinecone)
  - [Step 2: Get Nebius Token Factory API Key](#step-2-get-nebius-token-factory-api-key)
  - [Step 3: Login to N8N](#step-3-login-to-n8n)
  - [Step 4: Add Pinecone credential](#step-4-add-pinecone-credential)
  - [Step 5: Add Nebius Token Factory to N8N](#step-5-add-nebius-token-factory-to-n8n)
  - [Step 6: Import the workflow into N8N](#step-6-import-the-workflow-into-n8n)
  - [Step 7: Set Pinecone host](#step-7-set-pinecone-host)
  - [Step 8: Create a copy of Google Sheets on your Google account](#step-8-create-a-copy-of-google-sheets-on-your-google-account)
  - [Step 9: Configure Google sheet access at N8N](#step-9-configure-google-sheet-access-at-n8n)
  - [Step 10: Publish the n8n workflow](#step-10-publish-the-n8n-workflow)
  - [Step 11: Now the n8n workflow is configured.](#step-11-now-the-n8n-workflow-is-configured)


## Prerequisites

You will need 

- [N8N account](https://n8n.io/) (free tier is fine)
- [Nebius Token factory](https://tokenfactory.nebius.com/) account (free tier is fine)
- a Google account (free tier is fine)
- Details of Pinecone database (you will be provided this during the class) 

## Step 1: FAQ database (Pinecone)

You will need 
- Pinecone host detail
- Pinecone API key

These would be provided to you during the class.

**Optionally** you can choose to setup your own FAQ database.  
[Follow instructions here](faq-data/README.md).

## Step 2: Get Nebius Token Factory API Key

- Create an account or sign into your account at [Nebius Token Factory](https://tokenfactory.nebius.com/)
- Create an API key and save this for later

## Step 3: Login to N8N

Sign up / login to your [n8n](https://n8n.io/) account.

## Step 4: Add Pinecone credential

- In [n8n](https://n8n.io/) , go to **personal --> credentials --> create credential**
- Choose **pinecone** as a provider
- enter the Pinecone API key (provided to you or you created it)

## Step 5: Add Nebius Token Factory to N8N

- In [n8n](https://n8n.io/) , go to **personal --> credentials --> create credential**
- Choose **openAI** as a provider
- - Name: `Nebius Token Factory`
- Base URL: `https://api.tokenfactory.nebius.com/v1`
- API Key: Your Nebius API key

## Step 6: Import the workflow into N8N

- In [n8n](https://n8n.io/) , go to **Workflows -->  create a new workflow**
- Click on **...** and choose import from file
- Select this file [workflow/customer-support-multi-agent-v3.json](workflow/customer-support-multi-agent-v3.json)

TODO: Add screenshot

## Step 7: Set Pinecone host

- Click on **pre-processing** node
- Set the pinecone host as below

```js
const pineconeHost = 'support-faq-xxxxx.pinecone.io' // do not include HTTPS !
```

TODO: Add screenshot


## Step 8: Create a copy of Google Sheets on your Google account

- Here is the link to [google sheets](https://docs.google.com/spreadsheets/d/1iOTVG_rTqOZifioRbLZOkYzYmTLRW9rz430f3qBloPQ/edit?usp=sharing)
- Choose **File --> Create Copy**
- This will create a copy of the file in your google account.

A google sheet will look like 

```
https://docs.google.com/spreadsheets/d/xxxxxxx/edit?gid=yyyyy
```

Make a note of 
- document id `xxxxxx`
- and sheet id `yyyy`

## Step 9: Configure Google sheet access at N8N

- Edit **read google sheet** node
- Enter the sheet id (`xxxxx`) into **document id**
- Select **from list** select `order-history`

## Step 10: Publish the n8n workflow

## Step 11: Now the n8n workflow is configured.

Let's go to testing it!

Go to [test workflow](test-workflow.md)