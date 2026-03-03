import json, urllib.request
from config import KIMI_API_KEY, KIMI_MODEL, KIMI_BASE_URL

def call(system, user, max_tokens=4000):
    payload = {
        "model": KIMI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    req = urllib.request.Request(
        KIMI_BASE_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KIMI_API_KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["choices"][0]["message"]["content"]

def spec(task):
    return call(
        "You are Kimi, the orchestrator of the Pavano Loop. Your job is to turn a vague task into a precise spec.",
        f"""Turn this task into a structured spec with:
1. GOAL: One sentence on what success looks like
2. REQUIREMENTS: Numbered list of what must be true in the final output
3. CONSTRAINTS: What to avoid or not do
4. SUCCESS CRITERIA: How to verify it's done correctly

Task: {task}"""
    )

def final_check(task, spec_text, output):
    return call(
        "You are Kimi, the final reviewer. You check if the output meets the original requirements.",
        f"""Original task: {task}

Spec:
{spec_text}

Final output:
{output}

Does this meet all requirements? Reply with either:
SHIP — followed by a one-line summary
REWORK — followed by a numbered list of what's still missing""",
        max_tokens=1000
    )
