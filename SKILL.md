---
name: pavano-loop
description: Multi-agent orchestration for complex build tasks using the Pavano Loop framework. Use when a task requires structured spec-writing, implementation planning, iterative execution, and quality review across multiple models. Triggers for requests involving: building a feature end-to-end, writing code that needs planning + review, tasks where "just do it" risks missing requirements, or any explicit mention of "run through the loop" or "use the Pavano Loop". NOT for simple one-shot tasks — overhead not worth it for anything under ~30 minutes of work.
---

# Pavano Loop

Multi-agent orchestration: Kimi specifies → Opus plans + reviews → Codex executes → Kimi ships.

## When to Use

- Complex builds with multiple requirements or acceptance criteria
- Code that needs planning before execution (not just "write this function")
- Tasks where silent failure is expensive (newsletters, bots, deployed code)
- Explicit user request to "run through the loop"

**Skip the loop for:** one-liners, config changes, quick fixes, research tasks.

## Stack

| Role | Model | Does |
|---|---|---|
| Orchestrator | Kimi k2.5 | Writes spec, does final ship/rework call |
| Planner/Reviewer | Opus 4.6 | Plans implementation, reviews output, confirms fixes |
| Executor | Codex gpt-5.3-codex | Builds, triages issues, applies fixes |
| Lightweight | Haiku 4.5 | Humanizer, summaries |

## The Loop

```
Task → Kimi: spec (goal, requirements, constraints, success criteria)
     → Opus: implementation plan
     → Codex: executes
     → Opus: reviews → PASS or numbered issues
     → if issues: Codex triages (locks issue list) → fixes
     → Opus: confirms only locked items
     → Kimi: final check → SHIP or REWORK (back to Opus)
     → max 3 iterations before escalating to human
```

Key design: Codex locks its own issue list after triage — can't renegotiate mid-fix. Opus only re-reviews what was locked. Kimi is the only one who can call SHIP.

## Usage

### CLI
```bash
cd ~/pavano-loop
python3 pavano-loop.py "your task description"
```

### Programmatic
```python
from loop import run

def my_executor(plan, issues=None, iteration=1):
    # call your model/tool here
    return output_string

output, status = run("task description", my_executor)
```

### Humanizer (standalone)
```python
from agents.haiku import humanize
clean = humanize("AI-generated text to clean up")
```

## Files

- `loop.py` — core loop logic (outer: Kimi, inner: Opus ↔ Codex)
- `pavano-loop.py` — CLI entry
- `config.py` — API keys, model names, MAX_ITERATIONS
- `agents/kimi.py` — spec + final check
- `agents/opus.py` — plan, review, confirm
- `agents/codex.py` — execute, triage, fix
- `agents/haiku.py` — humanize
- `prd.json` — live spec + status (source of truth)
- `progress.txt` — append-only log across all iterations

## What to Hand Off

Write a clear task string. The better the task, the better Kimi's spec. Include:
- What you're building
- Key constraints (shell only, no agent-browser, deploy to GitHub Pages, etc.)
- Success criteria if non-obvious

Bad: `"build the newsletter"`
Good: `"Build the Mandy Intel HTML newsletter from /tmp/mandy-content-today.json. Use shell only to write files. Match the existing template at https://misterpavano.github.io/mandy-intel/. Publish via ~/scripts/publish-newsletter.sh."`

## Escalation

If the loop hits MAX_ITERATIONS (default: 3) without SHIP, it returns `("last_output", "ESCALATE")`. Surface `prd.json` and `progress.txt` to Wally — don't guess at a fix.
