# Workflow

## Step-1: Webhook Node

- HTTP method: POST
- Path: customer-support-1-query

Test it:
- Click "Listen for test event'
- Note the test URL : e.g `https://YOUR-APP.app.n8n.cloud/webhook-test/customer-support-1-query`
- In the terminal 

```bash
curl -X POST URL_above \
  -H "Content-Type: application/json" \
  -d '{ "query": "hello!"}'
```

And you will get a response like 

```text
{"message":"Workflow was started"}
```

## Step-2: HTTP-Request Node

Add an HTTP Request node with these settings

- HTTP Method: POST
- URL : `https://api.tokenfactory.nebius.com/v1/chat/completions`
- Credential type: OpenAI
  - Set Nebius Token Factory Credentials
- Send Headers : ON
  - Content-Type: `application/json`
- Send Body : ON
  - Content-Type: JSON
  - Timeout: 30000
  - And the JSON is like this


```
{{ JSON.stringify(
    { 
        model: 'Qwen/Qwen3-30B-A3B-Instruct-2507', 
        temperature: 0, 
        max_tokens: 120, 
        response_format: { type: 'json_object' }, 
        messages: [ 
            { 
                role: 'system', 
                content: 'Classify the customer query into exactly one department: support, sales, billing, other. Return ONLY valid JSON in this format: {\"department\":\"support|sales|billing|other\"}.' }, 
                { 
                    role: 'user', 
                    content: (($('Customer Query Webhook').first().json.body && ($('Customer Query Webhook').first().json.body.query || $('Customer Query Webhook').first().json.body.message)) || '') 
                } 
        ] 
        }) 
}}
```

## Step-3: Add 'Respond to Webhook' node

Settings:
- Respond with : JSON
- Response body: `{{ $json }}`

Once you add the webhook, open the webhook (first node, step 1), and change the setting to
- Respond: Using 'Respond to Webhook' node

## Step-4: Testing

- Click 'Execute Workflow'
- Send some data to the webhook.  Use the **test** URL

```bash
curl -X POST  'https://sujeework.app.n8n.cloud/webhook-test/customer-support-1-query' \
  -H "Content-Type: application/json" \
  -d '{ "query": "I need to reset my password"}'
```

You will response like this 

```json
{
    "id":"chatcmpl-968dadcba6724a7093d2be9337b0adea",
    "message":{"content":
        "department": "support"
    ...
}
```

There we go!  We see the department.


## Step-5: Production Testing.

- Publish the workflow
- And note **production url** of webhook
- Send a curl request to this url like below

```bash
curl -X POST  'https://sujeework.app.n8n.cloud/webhook/customer-support-1-query' \
  -H "Content-Type: application/json" \
  -d '{ "query": "I need to reset my password"}'
```