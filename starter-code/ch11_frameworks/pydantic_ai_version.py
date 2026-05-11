"""Ch 11 Pydantic AI 版本 — type-safe agent, schema-first 風格。

裝：
    uv pip install -e ".[pydantic_ai]"

跑：
    uv run pydantic_ai_version.py "vibe coding"

對比點:
1. Pydantic AI 強迫 output_type — 你定 Pydantic model, agent 必填出該 schema
2. 適合「結構化輸出 + 給後續程式吃」的場景
3. 不適合 free-form 對話 (那 LangGraph 更合適)
4. 缺點: ecosystem 比 LangChain 小, 但長很快 (FastAPI 同團隊出, 整合性強)
"""
from __future__ import annotations

import os
import sys

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


FAKE_DB = {
    "vibe coding": "Vibe coding 是 Andrej Karpathy 2025 年提出的詞，指用 LLM/agent 寫 code 不用每行 review，靠氛圍跟結果驗證。",
    "react": "ReAct (Reason + Act) 是 2022 年 Yao et al. 提出的 agent 範式，LLM 交織 reasoning trace + tool action。",
    "grpo": "GRPO (Group Relative Policy Optimization) 是 DeepSeek 2024 提出的 RL 方法，從 group 內 sample 算 advantage 不用 reference model。",
}


class ResearchOutput(BaseModel):
    """Type-safe output — agent 必須填這個。"""
    topic: str
    summary: str  # 200 字繁中摘要
    facts_found: list[str]  # search 得到的事實


agent = Agent(
    "anthropic:claude-haiku-4-5",
    output_type=ResearchOutput,
    system_prompt="你是研究 agent。用 search 工具找 1-2 個事實後輸出結構化結果。",
)


@agent.tool
def search(ctx: RunContext, query: str) -> str:
    """Search the web for facts. Input: 1 line query string."""
    q = query.lower().strip()
    for key, val in FAKE_DB.items():
        if key in q:
            return val
    return f"沒有資料: {query}"


def main(topic: str) -> ResearchOutput:
    result = agent.run_sync(f"研究: {topic}")
    return result.output


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "vibe coding"
    print(f"=== Pydantic AI ===")
    print(f"Topic: {topic}\n")
    output = main(topic)
    print(f"\n=== Structured output ===")
    print(f"Topic: {output.topic}")
    print(f"Summary: {output.summary}")
    print(f"Facts: {output.facts_found}")
