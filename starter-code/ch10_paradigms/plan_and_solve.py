"""Ch 10 Plan-and-Solve skeleton — 練習 10.1。"""
from __future__ import annotations

import os
import sys

import anthropic

PLAN_SYSTEM = """\
你是 task planner。看到任務，**只**輸出計畫，不要執行也不要 call 工具。
格式：
1. <步驟 1>
2. <步驟 2>
...

每步要具體，能直接執行。最多 7 步。回繁中。
"""

EXEC_SYSTEM = """\
你是 task executor。依照給定的 plan 一步一步做。
每步講 (1) 我在執行第 N 步 (2) 觀察到什麼 (3) 進到下一步。
完成所有步驟後給最終回答。回繁中。
"""


def generate_plan(task: str) -> str:
    """完成這個 — 練習 10.1 plan 階段。"""
    client = anthropic.Anthropic()
    # TODO: call client.messages.create with PLAN_SYSTEM as system
    raise NotImplementedError("Complete generate_plan for exercise 10.1")


def execute_plan(plan: str, task: str) -> str:
    """完成這個 — 練習 10.1 execute 階段。"""
    # TODO: call LLM with EXEC_SYSTEM, plan + task as user message
    raise NotImplementedError("Complete execute_plan for exercise 10.1")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)

    task = " ".join(sys.argv[1:]) or "研究 3 個 OSS agent framework（LangGraph / CrewAI / Smolagents）並寫一個 200 字繁中比較表。"
    print(f"=== Task ===\n{task}\n")
    plan = generate_plan(task)
    print(f"=== Plan ===\n{plan}\n")
    answer = execute_plan(plan, task)
    print(f"=== Answer ===\n{answer}")
