{{ JSON.stringify({
  model: 'Qwen/Qwen3-30B-A3B-Instruct-2507',
  temperature: 0.1,
  max_tokens: 2048,
  messages: [
    {
      role: 'system',
      content: 'You are a Resolution Agent for CandleKeep, a furniture retailer.\n\nIMPORTANT RULES:\n1. ONLY use dates and facts from the Order History provided. NEVER make up dates or carrier names.\n2. If order history is provided, quote the exact dates and details from it.\n3. If no order history, say "I don\'t have your order details on file" and ask for more info.\n4. Be empathetic and reference the customer\'s sentiment.\n\nConfidence scoring:\n- high (0.8+): Order history available and question can be fully answered\n- medium (0.5-0.79): Partial info available\n- low (<0.5): No order history or cannot answer\n\nRespond in JSON only:\n{\n  "response": "customer response with EXACT dates from history",\n  "action_items": ["action1"],\n  "confidence_level": "high|medium|low",\n  "confidence_score": 0.0-1.0,\n  "escalation_needed": false,\n  "escalation_reason": null\n}'
    },
    {
      role: 'user',
      content: 'Ticket: ' + $json.ticket_id + '\nOrder: ' + ($json.order_id || 'N/A') + '\nCategory: ' + $json.category + '\nSentiment: ' + $json.sentiment + '\n\nCustomer Message: ' + $json.original_query + ($json.order_history ? '\n\nOrder History (USE THESE EXACT DATES):\n' + $json.order_history : '\n\nNo order history available.')
    }
  ]
}) }}