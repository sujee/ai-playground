const query = $input.first().json.body?.query || '';

const orderMatch = query.match(/\b(\d{6})\b/);

const providedOrderId = $input.first().json.body?.order_id || null;

// Supports both n8n Cloud (Variables) and Docker (.env)
// const pineconeHost = $vars?.PINECONE_HOST || $env.PINECONE_HOST;
const pineconeHost = 'support-faq-fx69yh6.svc.aped-4627-b74a.pinecone.io' // do not include HTTPS !

return [{
  json: {
    original_query: query,
    order_id: providedOrderId || (orderMatch ? orderMatch[1] : null),
    customer_email: $input.first().json.body?.email || null,
    submission_channel: $input.first().json.body?.channel || 'API',
    timestamp: new Date().toISOString(),
    ticket_id: 'TKT-' + Date.now(),
    pinecone_host: pineconeHost
  }
}];