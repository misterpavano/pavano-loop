"""
Pavano Loop — Multi-agent iteration loop

Architecture (learned from Ralph):
- prd.json: source of truth for requirements + acceptance criteria
- progress.txt: append-only log, survives iterations, gives context to each pass
- Fresh Codex context each iteration (no context bloat)
- Opus owns the locked issue list — Codex can't renegotiate mid-fix
- Kimi is entry and exit — writes the spec, confirms ship

The inner loop (Opus <-> Codex):
  Codex executes
  Opus reviews → issues list
  Codex triages → locks down what it will fix (can't change this list after)
  Codex fixes
  Opus checks ONLY the locked list
  Repeat until Opus says CONFIRMED or max inner iterations hit

The outer loop (Kimi):
  When inner loop resolves → Kimi checks all original requirements
  SHIP → done
  REWORK → back to Opus with Kimi's notes, inner loop restarts
"""

import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from agents import kimi, opus, codex
from config import MAX_ITERATIONS

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.txt")
PRD_FILE = os.path.join(os.path.dirname(__file__), "prd.json")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with open(PROGRESS_FILE, "a") as f:
        f.write(entry + "\n")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return f.read()
    return ""

def save_prd(data):
    with open(PRD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_prd():
    if os.path.exists(PRD_FILE):
        with open(PRD_FILE) as f:
            return json.load(f)
    return None

def run(task):
    print(f"\n{'='*60}")
    print("PAVANO LOOP")
    print(f"Task: {task[:80]}...")
    print('='*60)

    # Init progress log
    with open(PROGRESS_FILE, "w") as f:
        f.write(f"# Pavano Loop — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Task: {task}\n---\n")

    # === OUTER LOOP: Kimi ===
    for outer in range(1, MAX_ITERATIONS + 1):
        log(f"OUTER {outer}/{MAX_ITERATIONS} — Kimi: writing spec...")

        if outer == 1:
            spec_text = kimi.spec(task)
            save_prd({"task": task, "spec": spec_text, "status": "in_progress"})
        else:
            # Kimi sent it back with notes — load existing prd
            prd = load_prd()
            spec_text = prd["spec"]
            kimi_notes = prd.get("kimi_notes", "")
            log(f"Kimi notes from last pass:\n{kimi_notes}")

        log(f"Spec:\n{spec_text}")

        log("Opus: planning...")
        plan = opus.plan(spec_text + (f"\n\nKimi notes:\n{kimi_notes}" if outer > 1 else ""))
        log(f"Plan:\n{plan}")

        output = None
        locked_issues = None

        # === INNER LOOP: Codex <-> Opus ===
        for inner in range(1, MAX_ITERATIONS + 1):
            log(f"  INNER {inner}/{MAX_ITERATIONS} — Codex: executing...")

            progress_context = load_progress()

            if locked_issues:
                # Codex fixes only the locked list
                output = codex.fix(plan, output, locked_issues, progress_context)
                log(f"  Codex fixed. Output:\n{output[:500]}...")
            else:
                output = codex.execute(plan, progress_context)
                log(f"  Codex executed. Output:\n{output[:500]}...")

            log("  Opus: reviewing...")
            review = opus.review(spec_text, output)
            log(f"  Opus review:\n{review}")

            if review.strip().startswith("PASS"):
                log("  Opus: PASS")
                locked_issues = None
                break

            # Codex triages and locks the issue list
            log("  Codex: triaging issues...")
            locked_issues = codex.triage(review, output)
            log(f"  Codex locked issues:\n{locked_issues}")

            if inner < MAX_ITERATIONS:
                # Opus confirms only locked items
                log("  Opus: checking locked items...")
                confirm = opus.confirm_fixes(locked_issues, output)
                log(f"  Opus confirmation:\n{confirm}")
                if confirm.strip().startswith("CONFIRMED"):
                    log("  Opus: CONFIRMED — inner loop done")
                    break
            else:
                log(f"  Inner loop max ({MAX_ITERATIONS}) hit")

        # === Kimi final check ===
        log("Kimi: final requirements check...")
        verdict = kimi.final_check(task, spec_text, output)
        log(f"Kimi verdict:\n{verdict}")

        prd = load_prd()
        prd["last_output"] = output
        prd["kimi_verdict"] = verdict

        if verdict.strip().startswith("SHIP"):
            prd["status"] = "shipped"
            save_prd(prd)
            log("STATUS: SHIP")
            return output, "SHIP"
        else:
            # Extract Kimi's notes and loop back
            kimi_notes = verdict.replace("REWORK", "").strip()
            prd["kimi_notes"] = kimi_notes
            prd["status"] = "rework"
            save_prd(prd)
            log(f"STATUS: REWORK — going back to Opus")

    log(f"Outer loop max ({MAX_ITERATIONS}) hit — escalating")
    return output, "ESCALATE"
