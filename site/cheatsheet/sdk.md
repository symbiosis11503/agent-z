---
title: 速查卡 — Anthropic SDK / Prompt Cache / 多家 SDK 對照
description: Anthropic SDK basic call + tool_use + streaming + Prompt Cache (省 90% cost) + OpenAI / Gemini function calling 對照。
---

# 速查卡 · SDK

[← 回速查卡總覽](../cheatsheet)

## Anthropic SDK 速查

```python
import anthropic
client = anthropic.Anthropic()  # 自動讀 ANTHROPIC_API_KEY

# 基本 call
resp = client.messages.create(
    model="claude-haiku-4-5",  # or sonnet-4-6, opus-4-7
    max_tokens=1000,
    system="你是 X",
    messages=[
        {"role": "user", "content": "..."},
    ],
)
print(resp.content[0].text)
print(f"in={resp.usage.input_tokens} out={resp.usage.output_tokens}")

# Tool use
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }],
    messages=[{"role": "user", "content": "Tokyo 天氣"}],
)

# 處理 stop_reason
if resp.stop_reason == "tool_use":
    for block in resp.content:
        if block.type == "tool_use":
            result = my_tool(**block.input)  # 真跑 tool
            # 把 tool_result 加回 messages, 再 call 一次
elif resp.stop_reason == "end_turn":
    # 結束，最終 text 是 resp.content[0].text
    pass

# Streaming
with client.messages.stream(model=..., max_tokens=..., messages=[...]) as s:
    for delta in s.text_stream:
        print(delta, end="", flush=True)
```

## Prompt Cache (省 90% cost)

```python
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system=[
        {
            "type": "text",
            "text": "<長 system prompt 5K+ token>",
            "cache_control": {"type": "ephemeral"},  # cache 1 hr
        },
    ],
    messages=[...],
    extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
)
# cache hit: input cost × 0.1
```

## SDK 速比較 (function calling)

```python
# Anthropic
resp.content                 # list of blocks
block.type == "tool_use"     # tool block
block.input                  # dict (parsed)
block.id                     # for tool_result reference

# OpenAI
resp.choices[0].message.tool_calls  # list
tc.function.name             # string
tc.function.arguments        # JSON string (要 json.loads)
tc.id                        # for tool_result reference

# Gemini (google-generativeai)
resp.candidates[0].content.parts
part.function_call.name
part.function_call.args      # proto.MapComposite
```

---

**下一頁** → [Pricing](./pricing) · [Patterns](./patterns) · [MCP / Skills](./mcp) · [Governance](./governance) · [CLI / Git](./cli)
