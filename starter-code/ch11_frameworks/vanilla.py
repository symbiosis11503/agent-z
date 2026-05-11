"""Ch 11 vanilla baseline — 不用 framework, 直接 Anthropic SDK 寫 tool-use loop。

跑：
    uv run vanilla.py "vibe coding"

對比點: 沒 framework 你會看到 (1) 自己寫 ReAct loop (2) 自己處理 tool call/result
serialization (3) 自己決定 max_steps。其他 framework 都把這些包掉。
"""
from __future__ import annotations

import json
import os
import sys

import anthropic


# === Tool 實作 (這裡用假 search，學習用，真的接 Tavily/Serper 一行的事) ===
FAKE_DB = {
    "vibe coding": "Vibe coding 是 Andrej Karpathy 2025 年提出的詞，指用 LLM/agent 寫 code 不用每行 review，靠氛圍跟結果驗證。",
    "react": "ReAct (Reason + Act) 是 2022 年 Yao et al. 提出的 agent 範式，LLM 交織 reasoning trace + tool action。",
    "grpo": "GRPO (Group Relative Policy Optimization) 是 DeepSeek 2024 提出的 RL 方法，從 group 內 sample 算 advantage 不用 reference model。",
}


def fake_search(query: str) -> str:
    """假 search — 真實使用換成 Tavily / Serper / Brave。"""
    q = query.lower().strip()
    for key, val in FAKE_DB.items():
        if key in q:
            return val
    return f"沒有資料: {query} (請改 query)"


TOOLS = [{
    "name": "search",
    "description": "Search the web for facts. Input: 1 line query string.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
}]


def run_agent(topic: str, max_steps: int = 5) -> str:
    client = anthropic.Anthropic()
    system = (
        "你是研究 agent。用 search 工具找 1-2 個事實後，輸出 200 字內繁中摘要。"
        "找到就停，不要重複搜尋。"
    )
    messages = [{"role": "user", "content": f"研究: {topic}"}]

    for step in range(max_steps):
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1000,
            tools=TOOLS,
            system=system,
            messages=messages,
        )

        # 收 assistant block
        messages.append({"role": "assistant", "content": resp.content})

        # stop_reason == "end_turn" → 結束
        if resp.stop_reason == "end_turn":
            return "".join(b.text for b in resp.content if b.type == "text")

        # 處理 tool_use
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                print(f"  [step {step+1}] tool={block.name} input={block.input}")
                if block.name == "search":
                    result = fake_search(block.input["query"])
                else:
                    result = f"unknown tool: {block.name}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
        messages.append({"role": "user", "content": tool_results})

    return "(max_steps reached)"


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "vibe coding"
    print(f"=== Vanilla agent (Anthropic SDK only) ===")
    print(f"Topic: {topic}\n")
    answer = run_agent(topic)
    print(f"\n=== Answer ===\n{answer}")
