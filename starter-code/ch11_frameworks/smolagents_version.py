"""Ch 11 Smolagents 版本 — HF 出的「LLM 直接寫 Python code 當 action」風格 (CodeAct)。

裝：
    uv pip install -e ".[smolagents]"

跑：
    uv run smolagents_version.py "vibe coding"

對比點:
1. Smolagents 默認 CodeAct — LLM 寫 Python 代替「list of tool calls」
2. 更有表達力 (loops / conditionals 都能寫), 也更危險 (sandbox 要嚴)
3. 一個 file 內 ~30 行就能跑
4. 缺點: production governance 缺 (audit / replay 要自己包)
"""
from __future__ import annotations

import os
import sys

from smolagents import CodeAgent, LiteLLMModel, tool


FAKE_DB = {
    "vibe coding": "Vibe coding 是 Andrej Karpathy 2025 年提出的詞，指用 LLM/agent 寫 code 不用每行 review，靠氛圍跟結果驗證。",
    "react": "ReAct (Reason + Act) 是 2022 年 Yao et al. 提出的 agent 範式，LLM 交織 reasoning trace + tool action。",
    "grpo": "GRPO (Group Relative Policy Optimization) 是 DeepSeek 2024 提出的 RL 方法，從 group 內 sample 算 advantage 不用 reference model。",
}


@tool
def search(query: str) -> str:
    """Search the web for facts.

    Args:
        query: 1 line query string.
    """
    q = query.lower().strip()
    for key, val in FAKE_DB.items():
        if key in q:
            return val
    return f"沒有資料: {query}"


def main(topic: str) -> str:
    model = LiteLLMModel(model_id="anthropic/claude-haiku-4-5", max_tokens=1500)
    agent = CodeAgent(tools=[search], model=model, max_steps=4)
    result = agent.run(f"研究 {topic}, 用 search 工具找事實後輸出 200 字內繁中摘要。")
    return str(result)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "vibe coding"
    print(f"=== Smolagents (CodeAct) ===")
    print(f"Topic: {topic}\n")
    answer = main(topic)
    print(f"\n=== Answer ===\n{answer}")
