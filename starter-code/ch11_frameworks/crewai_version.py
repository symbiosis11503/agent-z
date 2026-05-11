"""Ch 11 CrewAI 版本 — 用 role-based 的 agent + task + crew 抽象。

裝：
    uv pip install -e ".[crewai]"

跑：
    uv run crewai_version.py "vibe coding"

對比點:
1. CrewAI 強迫你「給 agent 一個 role」(researcher / writer / etc.)
2. 多 agent 場景 (例如 Ch 14) CrewAI 寫起來最自然
3. 單 agent 場景反而 verbose, vanilla.py 用 1/3 行
4. 缺點: 預設綁 OpenAI, 換 Claude 要設 env var ANTHROPIC_API_KEY + model 字串前綴 "anthropic/"
"""
from __future__ import annotations

import os
import sys

from crewai import Agent, Crew, Task
from crewai.tools import tool


FAKE_DB = {
    "vibe coding": "Vibe coding 是 Andrej Karpathy 2025 年提出的詞，指用 LLM/agent 寫 code 不用每行 review，靠氛圍跟結果驗證。",
    "react": "ReAct (Reason + Act) 是 2022 年 Yao et al. 提出的 agent 範式，LLM 交織 reasoning trace + tool action。",
    "grpo": "GRPO (Group Relative Policy Optimization) 是 DeepSeek 2024 提出的 RL 方法，從 group 內 sample 算 advantage 不用 reference model。",
}


@tool("search")
def search(query: str) -> str:
    """Search the web for facts. Input: 1 line query string."""
    q = query.lower().strip()
    for key, val in FAKE_DB.items():
        if key in q:
            return val
    return f"沒有資料: {query}"


def main(topic: str) -> str:
    researcher = Agent(
        role="研究員",
        goal=f"找關於 {topic} 的事實後寫摘要",
        backstory="你是專業繁中研究助理。用 search 工具找 1-2 個事實後輸出 200 字內繁中摘要。",
        tools=[search],
        llm="anthropic/claude-haiku-4-5",  # CrewAI 用 litellm 字串
        verbose=False,
    )
    task = Task(
        description=f"研究: {topic}。用 search 工具找事實後寫 200 字繁中摘要。",
        expected_output="200 字以內的繁中摘要，包含 search 找到的事實。",
        agent=researcher,
    )
    crew = Crew(agents=[researcher], tasks=[task], verbose=False)
    result = crew.kickoff()
    return str(result)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "vibe coding"
    print(f"=== CrewAI agent ===")
    print(f"Topic: {topic}\n")
    answer = main(topic)
    print(f"\n=== Answer ===\n{answer}")
