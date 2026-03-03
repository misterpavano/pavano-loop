import json, urllib.request
from config import OPENAI_API_KEY, CODEX_MODEL, OPENAI_BASE_URL

def call(system, user, max_tokens=4000):
    payload = {
        "model": CODEX_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }
    req = urllib.request.Request(
        OPENAI_BASE_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]

def execute(plan, progress_context=""):
    return call(
        "You are Codex, the executor in the Pavano Loop. Implement exactly what the plan says. Be precise and complete.",
        f"""Implement this plan. Return the complete output.

Plan:
{plan}

{f'Progress so far:{chr(10)}{progress_context[-2000:]}' if progress_context else ''}"""
    )

def triage(issues, output):
    """
    Codex reads Opus issues, decides which are real, locks the list.
    Returns a locked issue list as a string. This list cannot be changed.
    """
    return call(
        "You are Codex. You triage reviewer feedback honestly. Accept real issues, reject wrong or out-of-scope ones.",
        f"""Opus raised these issues about your output. Triage them.

Issues:
{issues}

Your output:
{output}

Reply with LOCKED ISSUES (the ones you will fix, numbered):
- Accept: genuine bugs, missing requirements, real errors
- Reject: style opinions, wrong assumptions, out-of-scope requests

Format:
WILL FIX:
1. [issue]
2. [issue]

SKIPPING:
- [issue]: [one-line reason]

This list is final. You will be held to only these items.""",
        max_tokens=800
    )

def fix(plan, output, locked_issues, progress_context=""):
    """
    Codex fixes only the locked issue list. No scope creep.
    """
    return call(
        "You are Codex. Fix ONLY the items in the locked issue list. Do not change anything else.",
        f"""Fix only these locked issues. Do not touch anything else.

Locked issues to fix:
{locked_issues}

Original plan:
{plan}

Current output:
{output}

{f'Progress log:{chr(10)}{progress_context[-1000:]}' if progress_context else ''}

Return the complete updated output with ONLY those issues fixed."""
    )
