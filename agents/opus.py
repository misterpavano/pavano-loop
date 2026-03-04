import json, urllib.request
from config import ANTHROPIC_KEY, OPUS_MODEL, ANTHROPIC_BASE_URL

def call(system, user, max_tokens=4000):
    payload = {
        "model": OPUS_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }
    req = urllib.request.Request(
        ANTHROPIC_BASE_URL,
        data=json.dumps(payload).encode(),
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)["content"][0]["text"]

def plan(spec_text):
    return call(
        "You are Opus, the planner. You turn specs into clear implementation plans.",
        f"""Write a step-by-step implementation plan for this spec. Be concrete and specific. No code yet, just the plan.

Spec:
{spec_text}"""
    )

def review(spec_text, output):
    return call(
        "You are Opus, the code reviewer. You check output against spec and find real issues.",
        f"""Review this output against the spec. Be strict but fair.

Spec:
{spec_text}

Output:
{output}

Reply with either:
PASS — it meets the spec
ISSUES:
1. [specific issue]
2. [specific issue]
...

Only list real problems, not style preferences.""",
        max_tokens=1000
    )

def confirm_fixes(issues, output):
    return call(
        "You are Opus, confirming that specific issues were fixed.",
        f"""Check ONLY whether these specific issues were fixed. Do not do a full review.

Issues to check:
{issues}

Updated output:
{output}

Reply with either:
CONFIRMED — all issues fixed
STILL MISSING:
[list what's still broken]""",
        max_tokens=500
    )
