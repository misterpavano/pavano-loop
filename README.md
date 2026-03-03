# Pavano Loop

Multi-agent orchestration framework. Kimi orchestrates, Opus thinks, Codex builds.

## The Stack

- **Kimi k2.5** — Orchestrator. Writes the spec, does the final requirements check.
- **Claude Opus 4.6** — Planner + Reviewer. Plans implementation, reviews output, confirms fixes.
- **Claude Haiku 4.5** — Lightweight tasks (humanizer, summaries).
- **Executor** — Pluggable. Default is human-in-the-loop. Swap in Codex, a script, or any function.

## The Loop

```
Task in
  → Kimi: reads task, writes structured spec (goal, requirements, constraints, success criteria)
  → Opus: reads spec, writes implementation plan
  → Executor: builds it
  → Opus: reviews output vs spec → PASS or numbered issues
  → if issues: Executor triages + fixes
  → Opus: confirms only the flagged items (not full re-review)
  → Kimi: final check → SHIP or REWORK
  → max 3 iterations before escalating to human
```

## Usage

### Interactive (human executor)
```bash
python3 pavano-loop.py "write a cold outreach email for a restaurant in Apex NC"
```

### Programmatic (custom executor)
```python
from loop import run

def my_executor(plan, issues=None, iteration=1):
    # call your model/script/tool here
    return output_string

output, status = run("your task", my_executor)
```

### Humanizer (standalone)
```python
from agents.haiku import humanize
clean = humanize("your AI-generated text here")
```

## Files

- `pavano-loop.py` — CLI entry point
- `loop.py` — the loop logic
- `config.py` — API keys and model names
- `agents/kimi.py` — Kimi k2.5 client (orchestrator)
- `agents/opus.py` — Opus 4.6 client (planner + reviewer)
- `agents/haiku.py` — Haiku 4.5 client (lightweight tasks)

## Config

Keys are loaded from:
- Kimi: hardcoded in `config.py`
- Anthropic: read from `~/.openclaw/agents/main/agent/auth-profiles.json`
