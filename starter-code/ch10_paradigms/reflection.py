"""Ch 10 Reflection skeleton — 練習 10.2。"""
from __future__ import annotations

import os
import re
import sys

import anthropic

CRITIQUE_SYSTEM = """\
你是 code reviewer。看一段 agent 的答案，**只**回兩件事：
1. 評分 0-10（10 = 完美）
2. 改進建議（如果 < 8 分）

格式：
SCORE: 7
FEEDBACK: 答案少了 X 部分，建議補上 Y。
回繁中。
"""


def parse_score(critique: str) -> int:
    m = re.search(r"SCORE:\s*(\d+)", critique)
    return int(m.group(1)) if m else 0


def parse_feedback(critique: str) -> str:
    m = re.search(r"FEEDBACK:\s*(.+)", critique, re.S)
    return m.group(1).strip() if m else ""


def reflection(task: str, max_iter: int = 3, target_score: int = 8) -> str:
    """完成這個 — 練習 10.2 critique loop。"""
    client = anthropic.Anthropic()
    history: list[dict] = []

    for i in range(max_iter):
        # TODO 10.2a: call LLM 用 history feedback 寫一次答案
        # TODO 10.2b: critique 答案 (用 CRITIQUE_SYSTEM)
        # TODO 10.2c: parse score + feedback → 加進 history
        # TODO 10.2d: 如果 score >= target 直接 return；否則 redo
        raise NotImplementedError("Complete reflection for exercise 10.2")

    # max_iter 到了 — 回最高分版本
    return max(history, key=lambda h: h["score"])["attempt"] if history else ""


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)

    task = " ".join(sys.argv[1:]) or "寫一個 Python function 計算 fibonacci，含 unit test。"
    print(f"=== Task ===\n{task}\n")
    answer = reflection(task)
    print(f"=== Final Answer ===\n{answer}")
