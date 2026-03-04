import json, urllib.request
from config import ANTHROPIC_KEY, ANTHROPIC_BASE_URL

# Codex role uses claude-sonnet as executor (Codex OAuth not available via raw API)
EXECUTOR_MODEL = "claude-sonnet-4-5"

def call(system, user, max_tokens=8000):
    payload = {
        "model": EXECUTOR_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }
    req = urllib.request.Request(
        ANTHROPIC_BASE_URL,
        data=json.dumps(payload).encode(),
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["content"][0]["text"]

def execute(plan, progress_context=""):
    return call(
        "You are Codex, the executor in the Pavano Loop. Implement exactly what the plan says. Be precise and complete.",
        f"""Implement this plan. Return the complete output.

Plan:
{plan}

{f'Progress so far:{chr(10)}{progress_context[-2000:]}' if progress_context else ''}"""
    )

def triage(issues, plan, output):
    return call(
        "You are Codex, triaging issues. Lock down exactly what you will fix — you cannot change this list later.",
        f"""Triage these issues and state exactly what you will fix.

Issues from review:
{issues}

Original plan:
{plan}

Your output so far:
{output}

List the issues you will fix (numbered). This list is now locked — you cannot add or remove items later.
Then fix them and return the complete updated output.""",
        max_tokens=8000
    )
