# Testing n8n agent

## Step 1: note the producion web hook url

- Open 'web hook' node
- select **production**
- Note the URL

ON your terminal set this 

```bash
export BASE_URL='your production url here'
```

## API Request Format

```json
{
 "query": "Customer's message here",
 "order_id": "770487", // Optional - 6 digit order ID
 "channel": "Website", // Optional - Website, Mobile App, External Marketplace
 "email": "customer@example.com" // Optional
}
```


## Step 2: Test FAQ branch

```bash
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How long does delivery take?",
    "channel": "Mobile App"
  }' | jq '.'
```

## Step 3:  agent confident response

```bash
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Where is my order? I placed it almost two weeks ago and the tracking link still shows processing. Can someone check the status for me urgently?",
    "order_id": "770487",
    "channel": "External Marketplace"
  }' | jq '.'
```

## Step 4: manual response

```bash
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I would like to discuss a potential partnership with your company. Please connect me with your legal and business development team.",
    "channel": "Website"
  }' | jq '.'
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



<!-- Or run the full test suite:

```bash
chmod +x test/test-workflow.sh
./test/test-workflow.sh
``` -->


