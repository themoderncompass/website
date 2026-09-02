// Cloudflare Pages Function: POST /api/subscribe
//
// Accepts an email from our own signup form and creates a beehiiv
// subscriber server-side, so the frontend never talks to beehiiv (or
// waits on beehiiv's bot-check iframe) directly.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function onRequestPost(context) {
  const { request, env } = context;

  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ error: 'Invalid request.' }, 400);
  }

  const email = typeof body.email === 'string' ? body.email.trim() : '';
  const honeypot = typeof body.website === 'string' ? body.website.trim() : '';

  // Honeypot filled in => bot. Reject without touching beehiiv's API,
  // but don't tip the bot off with an error response.
  if (honeypot) {
    return jsonResponse({ success: true }, 200);
  }

  if (!EMAIL_RE.test(email)) {
    return jsonResponse({ error: 'Please enter a valid email address.' }, 400);
  }

  const publicationId = env.PUBLICATION_ID;
  const apiKey = env.BEEHIIV_API_KEY;

  if (!publicationId || !apiKey) {
        return jsonResponse({ error: 'Newsletter signup is temporarily unavailable.', hasPublicationId: Boolean(publicationId), hasApiKey: Boolean(apiKey) }, 500);
  }

  let beehiivRes;
  try {
    beehiivRes = await fetch(
      `https://api.beehiiv.com/v2/publications/${publicationId}/subscriptions`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      }
    );
  } catch {
    return jsonResponse({ error: 'Could not reach the subscription service. Please try again.' }, 502);
  }

  if (beehiivRes.ok) {
    return jsonResponse({ success: true }, 200);
  }

  const errorData = await beehiivRes.json().catch(() => ({}));
  const message = errorData?.errors?.[0]?.message || errorData?.message || 'Subscription failed. Please try again.';
  return jsonResponse({ error: message }, beehiivRes.status);
}

function jsonResponse(data, status) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
