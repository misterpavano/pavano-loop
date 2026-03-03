#!/usr/bin/env python3
"""
Pavano Loop — Multi-agent orchestration
Usage: python3 pavano-loop.py "your task here"

The loop: Kimi specs → Opus plans → You execute → Opus reviews → Kimi ships
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from loop import run

def simple_executor(plan, issues=None, iteration=1):
    """
    Default executor: asks the human to do the work.
    Replace this with your actual executor (Codex, a script, etc.)
    """
    print("\n" + "="*40)
    print("YOUR TURN — implement this:")
    print("="*40)
    if issues:
        print(f"\nFix these issues:\n{issues}\n")
    else:
        print(f"\nPlan:\n{plan}\n")
    print("Paste your output below (type END on a new line when done):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pavano-loop.py \"your task here\"")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    output, status = run(task, simple_executor)

    print(f"\n{'='*60}")
    print(f"RESULT: {status}")
    print('='*60)
    print(output)
