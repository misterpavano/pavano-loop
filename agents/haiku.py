import json, urllib.request
from config import ANTHROPIC_KEY, HAIKU_MODEL, ANTHROPIC_BASE_URL

def call(system, user, max_tokens=2000):
    payload = {
        "model": HAIKU_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }
    req = urllib.request.Request(
        ANTHROPIC_BASE_URL,
        data=json.dumps(payload).encode(),
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["content"][0]["text"]

def humanize(text):
    return call(
        "You remove AI writing patterns. No em dashes. Natural, human voice. Return only the rewritten text.",
        f"Humanize this:\n\n{text}"
    )

def summarize(text):
    return call(
        "You write tight, accurate summaries.",
        f"Summarize in 3 bullet points:\n\n{text}"
    )
