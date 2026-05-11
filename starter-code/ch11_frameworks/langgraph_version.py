"""Ch 11 LangGraph 版本 — 同任務、用 LangGraph 的 graph + state machine 模型。

裝：
    uv pip install -e ".[langgraph]"

跑：
    uv run langgraph_version.py "vibe coding"

對比 vanilla.py 你會看到:
1. 不用自己寫 ReAct loop — LangGraph create_react_agent 包好
2. State 用 typed dict, graph node 自動串
3. checkpointing (memory) 一行接, 但這 demo 沒用到
4. 缺點: dependency 重 (200MB+), 學曲線陡
"""
from __future__ import annotations

import os
import sys

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


FAKE_DB = {
    "vibe coding": "Vibe coding 是 Andrej Karpathy 2025 年提出的詞，指用 LLM/agent 寫 code 不用每行 review，靠氛圍跟結果驗證。",
    "react": "ReAct (Reason + Act) 是 2022 年 Yao et al. 提出的 agent 範式，LLM 交織 reasoning trace + tool action。",
    "grpo": "GRPO (Group Relative Policy Optimization) 是 DeepSeek 2024 提出的 RL 方法，從 group 內 sample 算 advantage 不用 reference model。",
}


@tool
def search(query: str) -> str:
    """Search the web for facts. Input: 1 line query string."""
    q = query.lower().strip()
    for key, val in FAKE_DB.items():
        if key in q:
            return val
    return f"沒有資料: {query}"


def main(topic: str) -> str:
    llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=1000)
    # LangGraph 一行做掉 ReAct loop
    agent = create_react_agent(
        llm,
        tools=[search],
        prompt="你是研究 agent。用 search 工具找 1-2 個事實後輸出 200 字內繁中摘要。",
    )
    result = agent.invoke({"messages": [{"role": "user", "content": f"研究: {topic}"}]})
    # 最後一條 assistant message 為答案
    return result["messages"][-1].content


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "vibe coding"
    print(f"=== LangGraph agent ===")
    print(f"Topic: {topic}\n")
    answer = main(topic)
    print(f"\n=== Answer ===\n{answer}")
