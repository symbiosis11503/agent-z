"""Ch 13 Self-Learning Loop skeleton — 練習 13.4。

Agent 完成任務後萃取「步驟摘要」存入 skills.json，
下次遇到類似任務先查 match，看步數是否減少。

成功標準：第一次做某任務花 N 步，第二次做類似任務步數減少。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import anthropic

SKILLS_PATH = Path(__file__).parent / "skills.json"
MODEL = "claude-haiku-4-5"


def load_skills() -> dict[str, list[str]]:
    if SKILLS_PATH.exists():
        return json.loads(SKILLS_PATH.read_text())
    return {}


def save_skills(skills: dict[str, list[str]]) -> None:
    SKILLS_PATH.write_text(json.dumps(skills, ensure_ascii=False, indent=2))


def find_matching_skill(task: str, skills: dict) -> list[str] | None:
    """Check if any existing skill keyword matches the task."""
    task_lower = task.lower()
    for keyword, steps in skills.items():
        if keyword.lower() in task_lower:
            return steps
    return None


def extract_skill(client: anthropic.Anthropic, task: str, steps: list[str]) -> tuple[str, list[str]]:
    """Call LLM to extract a reusable skill from completed task steps.

    Returns (trigger_keyword, condensed_steps).
    """
    # TODO 13.4: call LLM with the task description + steps list
    # Ask it to return JSON: {"keyword": "...", "steps": ["step1", "step2", ...]}
    # The keyword should be a short trigger phrase for matching future tasks.
    # The steps should be a condensed version (fewer than original).
    raise NotImplementedError("Complete extract_skill for exercise 13.4")


def run_task(client: anthropic.Anthropic, task: str) -> list[str]:
    """Run a multi-step task using ReAct-style loop. Returns list of steps taken."""
    skills = load_skills()
    prior = find_matching_skill(task, skills)

    if prior:
        print(f"  [skill hit] Found prior skill with {len(prior)} steps — using as guide")
        # TODO 13.4: incorporate prior steps as a hint in the system prompt
        # e.g. "You have done a similar task before. Follow these steps: ..."
        system = f"You are a helpful assistant. You previously solved a similar task with these steps:\n" + \
                 "\n".join(f"  {i+1}. {s}" for i, s in enumerate(prior)) + \
                 "\nAdapt and follow them. Be concise. Respond with numbered steps only."
    else:
        print("  [no skill match] Solving from scratch")
        system = "You are a helpful assistant. Break the task into numbered steps and execute each. Be concise."

    resp = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=system,
        messages=[{"role": "user", "content": task}],
    )
    text = resp.content[0].text

    # Parse numbered steps from response
    steps = [line.strip() for line in text.strip().split("\n") if line.strip() and line.strip()[0].isdigit()]
    if not steps:
        steps = [text.strip()]

    return steps


def main():
    client = anthropic.Anthropic()

    tasks = [
        "Write a Python function that reads a CSV file and returns the average of a numeric column",
        "Write a Python function that reads a JSON file and returns the average of a numeric field",
    ]

    for i, task in enumerate(tasks):
        print(f"\n{'='*60}")
        print(f"Task {i+1}: {task}")
        print(f"{'='*60}")

        steps = run_task(client, task)
        print(f"\nCompleted in {len(steps)} steps:")
        for s in steps:
            print(f"  {s}")

        # After completing, extract and save skill
        skills = load_skills()
        try:
            keyword, condensed = extract_skill(client, task, steps)
            skills[keyword] = condensed
            save_skills(skills)
            print(f"\n  [learned] Saved skill '{keyword}' with {len(condensed)} condensed steps")
        except NotImplementedError:
            print("\n  [skip] extract_skill not implemented yet — complete the TODO!")

    print(f"\n{'='*60}")
    print("Compare step counts: task 2 should use fewer steps than task 1")
    print(f"Skills file: {SKILLS_PATH}")


if __name__ == "__main__":
    main()
