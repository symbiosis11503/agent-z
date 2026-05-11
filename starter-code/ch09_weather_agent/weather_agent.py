"""
AgentZ Ch 9 — Weather Agent (Exercise 9.1 / 9.2 / 9.3 starter)

完成順序：
  - 9.1: 把 run_agent() 完成、能跑「比較台北跟東京天氣」
  - 9.2: 改 _execute_tools_parallel 用 asyncio.gather
  - 9.3: get_weather 對不存在的城市回 ERROR 字串、觀察 LLM 怎麼處理

跑：
    uv run weather_agent.py "比較台北跟東京哪個比較熱"
"""
from __future__ import annotations

import os
import sys
import anthropic


# Fake weather data — 練習 9.3 把不存在的城市改成 raise / return ERROR string
WEATHER_DB = {
    "Taipei": "26°C, 晴",
    "Tokyo": "18°C, 雨",
    "Singapore": "31°C, 雷陣雨",
    "Seoul": "8°C, 多雲",
}


def get_weather(city: str) -> str:
    """Get current weather for a city. (Fake — 換成真實 API 也行)"""
    if city not in WEATHER_DB:
        # 練習 9.3：故意回 ERROR 觀察 LLM self-correct
        return f"ERROR: city {city!r} not found"
    return f"{city}: {WEATHER_DB[city]}"


TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a given city. City name in English.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name in English, e.g. 'Taipei'",
                }
            },
            "required": ["city"],
        },
    }
]


def run_agent(user_message: str, max_iter: int = 8) -> str:
    """
    完成這個 function 是練習 9.1 的主要目標。

    Reference flow (從 Ch 9 §2.4 抄下來改):
      1. messages = [{"role": "user", "content": user_message}]
      2. for i in range(max_iter):
           a. call client.messages.create(model, tools, messages)
           b. append assistant response 進 messages
           c. if stop_reason != "tool_use": return final text
           d. find tool_use blocks, execute_tool() each
           e. append tool_results as {"role": "user", "content": [...]}
      3. return "(max_iter reached)"
    """
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    for i in range(max_iter):
        # TODO 9.1: call LLM
        # TODO 9.1: handle response — final text or tool_use loop
        # TODO 9.2: parallel execute tool_uses (use asyncio.gather if you want true async)
        raise NotImplementedError("Complete run_agent for exercise 9.1")

    return "(max_iter reached)"


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    question = " ".join(sys.argv[1:]) or "比較台北跟東京哪個比較熱"
    print(f"=== Question ===\n{question}\n")
    answer = run_agent(question)
    print(f"=== Answer ===\n{answer}")
