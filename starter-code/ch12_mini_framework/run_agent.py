"""Example usage of agentz_mini — 完成 agentz_mini.py 後跑這個驗證。"""
from __future__ import annotations

import ast
import os
import sys

from agentz_mini import Agent, tool


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    fake = {"Taipei": "26°C 晴", "Tokyo": "18°C 雨", "Singapore": "31°C 雷陣雨"}
    return fake.get(city, f"unknown city: {city}")


@tool
def calc(expr: str) -> str:
    """Calculate a simple arithmetic expression (only digits + operators)."""
    return str(eval(compile(ast.parse(expr, mode="eval"), "<expr>", "eval")))


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)

    agent = Agent(
        model="claude-haiku-4-5",
        tools=[get_weather, calc],
        system="用繁中回應。",
        max_iter=8,
        cost_cap_usd=0.10,
    )
    result = agent.run("比較台北跟東京天氣，並算 26-18 是多少。")
    print(f"=== Answer ===\n{result.answer}\n")
    print(
        f"Steps: {len(result.steps)} · "
        f"in={result.usage.input} · out={result.usage.output} · "
        f"cost=${result.cost:.4f}"
    )
    for s in result.steps:
        print(f"  [{s.kind}] {s.payload}")
