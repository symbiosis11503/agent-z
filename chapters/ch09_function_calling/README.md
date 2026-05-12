---
title: Ch 9 — Function Calling / Tool Use 第一原理
description: tools schema / tool_use / tool_result / stop_reason 6 種處理 / parallel tool use / 從零寫 weather agent。
---

# Ch 9 — Function Calling / Tool Use 第一原理

> **75-90 分鐘**。讀完你會懂：tool use 完整 protocol、Anthropic vs OpenAI tool schema、手寫 tool-use loop、parallel tools、error recovery。
>
> 動手練習：寫一個 weather agent 從零開始（不靠 CLI agent）+ 加 parallel tool + 加錯誤處理。
>
> 前置：完成 [Ch 8](../ch08_cost_observability/) — Operator 階段全完。
>
> 🛠 **Starter code**: [`starter-code/ch09_weather_agent/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch09_weather_agent) — function calling weather agent 從 0 寫起、含 tool schema / loop / parallel tools。

---

## 1. 為什麼要回到 raw API？

Operator 階段你用 Claude Code 跑 task。**Builder 階段你要寫 agent**——這代表你不能再靠 CLI agent 的 ReAct loop 包裝，要自己控。

具體要解決的問題：
- **自訂工具**：CLI agent 內建工具是固定的，你想加業務專屬工具（查訂單 / 結帳 / 發 webhook）。
- **embedded agent**：把 agent 嵌進你的 web / mobile / API 服務。
- **multi-agent 編排**：好幾個 agent 互相 handoff，這需要你寫 orchestrator。
- **自訂 cost / audit / replay**：production 用 agent 一定要有自己的觀測層。

所以這章開始我們**回 Python，從 raw `messages.create()` 寫 tool use loop**。

---

## 2. Tool Use 完整流程（Anthropic）

### 2.1 定義工具

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name in English, e.g. 'Taipei'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius"
                }
            },
            "required": ["city"]
        }
    }
]
```

3 個欄位：
- `name` — LLM 要 call 的時候用這個名字
- `description` — **這是 LLM 判斷「要不要 call」的依據**，寫好至關重要
- `input_schema` — JSON Schema，LLM 會照填

### 2.2 第一次 call LLM

```python
import anthropic
client = anthropic.Anthropic()

messages = [{"role": "user", "content": "台北現在幾度？"}]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=500,
    tools=tools,
    messages=messages,
)
```

`response.stop_reason` 可能值：
- `"end_turn"` — LLM 直接答完
- `"tool_use"` — LLM 要 call 工具，**你要執行 + 回去**
- `"max_tokens"` — 超過 token 上限
- `"stop_sequence"` — 撞到 stop sequence

### 2.3 處理 tool_use

```python
if response.stop_reason == "tool_use":
    # 把 LLM 的回應加進 messages
    messages.append({"role": "assistant", "content": response.content})

    # 找出 tool_use block 並執行
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
            })

    # 把結果包成 user 訊息塞回去
    messages.append({"role": "user", "content": tool_results})

    # 再 call 一次 LLM
    response = client.messages.create(...)
```

### 2.4 完整 loop

```python
def run_agent(user_message: str, max_iter: int = 10):
    messages = [{"role": "user", "content": user_message}]
    for i in range(max_iter):
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1000,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            # 結束：LLM 給最終答案
            final = next((b.text for b in response.content if b.type == "text"), "")
            return final

        # 執行所有 tool_use
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})

    return "達到最大迭代次數，未完成"

def execute_tool(name: str, input: dict) -> str:
    if name == "get_weather":
        # 真實會 call weather API；範例假資料
        return f"{input['city']}: 26°C, 晴"
    return f"Unknown tool: {name}"
```

這就是 **agent 的核心 loop**。Claude Code / Codex 內部就是這樣（外加更多 polish）。

---

## 3. OpenAI Function Calling vs Anthropic Tool Use

OpenAI 用詞略不同但概念一樣：

| 概念 | Anthropic | OpenAI |
|---|---|---|
| 定義工具 | `tools=[{...}]` 用 `input_schema` | `tools=[{type: "function", function: {parameters: ...}}]` |
| LLM 要 call 工具 | content 含 `type=tool_use` block | message 含 `tool_calls` |
| 回 tool 結果 | user 訊息含 `tool_result` block | role=`tool` 訊息 |
| 停止訊號 | `stop_reason="tool_use"` | `finish_reason="tool_calls"` |

OpenAI 版範例：
```python
from openai import OpenAI
client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "台北現在幾度？"}],
    tools=tools,
)

if response.choices[0].finish_reason == "tool_calls":
    tool_call = response.choices[0].message.tool_calls[0]
    # tool_call.function.name == "get_weather"
    # tool_call.function.arguments == '{"city": "Taipei"}' (JSON string!)
    ...
```

> 💡 **小坑**：OpenAI 的 tool arguments 是 **JSON string** 要自己 parse；Anthropic 是已 parsed 的 dict。

---

## 4. Parallel Tools — 一次 call 多個

LLM 可能一次回**多個** tool_use block，要你並行執行：

```python
import asyncio

async def execute_tool_async(name, input):
    # 你自己決定要不要真的 async
    return execute_tool(name, input)

# 在 tool_use 處理階段：
tool_uses = [b for b in response.content if b.type == "tool_use"]
results = await asyncio.gather(*[
    execute_tool_async(b.name, b.input) for b in tool_uses
])
```

**為什麼重要**：LLM 想「同時查 3 個城市的天氣」如果你序列執行就慢 3x。

---

## 4a. Computer Use — Anthropic 的特殊 tool use 模式

`computer use` 是 Anthropic 在 2024 Q4 推的特殊 tool-use type。**API 結構長一樣，差別在「工具」不是你寫的 function，而是 Anthropic 內建的虛擬桌面操作**——LLM 可以 screenshot、click、type、scroll，把整台電腦當 tool。

```python
# 跟一般 tool_use 同一個 API，只是 tools 用 type: computer_20241022
response = client.beta.messages.create(
    model="claude-sonnet-4-6",  # 或 claude-opus-4-7
    max_tokens=4096,
    tools=[{
        "type": "computer_20241022",
        "name": "computer",
        "display_width_px": 1920,
        "display_height_px": 1080,
        "display_number": 1,
    }],
    messages=[{"role": "user", "content": "幫我打開瀏覽器找天氣"}],
    betas=["computer-use-2024-10-22"],
)
```

回應裡 `tool_use` 的 `input` 會是 `{"action": "screenshot"}` 或 `{"action": "left_click", "coordinate": [x, y]}` 等，**你的執行端要實作這些 action**（通常用 Docker container 跑 VNC + xdotool）。

| 何時用 | 何時不用 |
|---|---|
| 沒 API / 沒 MCP / 沒 CLI 的舊系統（古老 GUI 應用） | 已有 API / MCP / CLI（永遠優先 structured tool） |
| 跨應用程式自動化（一邊 Excel 一邊瀏覽器） | 速度敏感（screenshot 很慢，per-step 1-3 秒） |
| Workflow 教學 / demo | 高頻交易 / production critical path |

> ⚠️ **危險程度高**：LLM 看 screenshot 點滑鼠、可能誤點 `刪除` `提交` `付款`。**永遠跑在 sandbox container**（Docker / VM），絕不在 host machine 直接給 root 權限。Anthropic 官方 sample 用 Docker。詳細白話：[名詞表 § Computer Use](https://symbiosis11503.github.io/agent-z/glossary/agent)。

---

## 5. Error Recovery

工具會失敗：API 502、檔案不存在、權限被拒。怎麼讓 LLM 處理？

**重點**：tool_result 的 content 可以是任何字串，**包括 error message**。LLM 看到 error 通常會自己決定 retry / 換個方法 / 告訴你失敗。

```python
def execute_tool_safely(name, input):
    try:
        return execute_tool(name, input)
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"
```

範例對話：
```
LLM: get_weather(city="Tapei")  # typo
Tool result: ERROR: city not found
LLM: 我寫錯了，再試一次：get_weather(city="Taipei")
Tool result: 26°C 晴
LLM: 台北現在 26°C、晴天。
```

LLM 會自己 self-correct。這是 ReAct 強大的地方。

但**也會無限 retry**——所以一定要有 `max_iter` 上限。

---

## 6. 觀測 token 跟 cost

每次 LLM call 的 response 有 `usage`：

```python
total_in = 0
total_out = 0

while True:
    r = client.messages.create(...)
    total_in += r.usage.input_tokens
    total_out += r.usage.output_tokens
    ...

# 算錢
PRICE_IN = 0.80 / 1_000_000  # haiku 4.5 in
PRICE_OUT = 4.00 / 1_000_000  # haiku 4.5 out
cost = total_in * PRICE_IN + total_out * PRICE_OUT
print(f"Total: ${cost:.4f}")
```

實作 cost cap：

```python
COST_CAP = 0.10  # $0.10 per run

while True:
    r = client.messages.create(...)
    total_in += r.usage.input_tokens
    total_out += r.usage.output_tokens
    cost = total_in * PRICE_IN + total_out * PRICE_OUT
    if cost > COST_CAP:
        raise RuntimeError(f"Cost cap exceeded: ${cost:.4f} > ${COST_CAP}")
    ...
```

Ch 15 會在 V3 case study 看完整 production-grade 實作。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 3 — Tools & Environments**：tool / function calling / parallel tools

---

## 8. 動手練習

### 練習 9.1：寫一個 Weather Agent

寫 `exercises/9.1_weather_agent.py`：
- 定義 `get_weather(city)` 工具（用假資料）
- 完整 `run_agent()` loop（max_iter=5）
- 跑「台北 vs 東京哪個比較熱？」

**成功標準**：agent 自動 call 兩次 `get_weather`，回比較結論。

### 練習 9.2：加 Parallel

改 9.1 用 `asyncio.gather` 並行執行工具。比較序列 vs 並行的 latency。

**成功標準**：「比較 5 個城市天氣」task 並行版比序列版快 3x 以上。

### 練習 9.3：Error Recovery

加 `get_weather` 對「不存在城市」回 `ERROR: ...`，跑「比較 Taipei / Xxxxxxxx / Tokyo」，觀察 LLM 怎麼處理。

**成功標準**：LLM 認知到 Xxxxxxxx 不存在、繼續用其他兩個城市結論。

---

## 9. 你做完這一章後 ✅

- [ ] 看到 tool_use JSON 知道哪欄是 input / id / name
- [ ] 寫得出完整 tool-use loop
- [ ] 知道 Anthropic 跟 OpenAI tool 格式差異
- [ ] 會做 parallel tool execution
- [ ] 知道 error 怎麼讓 LLM 自己 self-correct
- [ ] 知道怎麼算 cost + 設 cap
- [ ] 跑完練習 9.1 / 9.2 / 9.3

打勾 5 個以上，進 [Ch 10 — ReAct / Plan-and-Solve / Reflection](../ch10_react_paradigms/)。

---

## 9a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **forgot to append `tool_result`** | API 報「expected tool_result for tool_use_id」 | 收到 `stop_reason='tool_use'` 後必須 append `{"role":"user","content":[{"type":"tool_result", "tool_use_id":..., "content":...}]}` |
| **tool_use_id 對不上** | tool_result 被忽略 / 報錯 | id 必須 verbatim copy from tool_use block，不能自己編 |
| **回傳格式錯** | LLM 收到怪結果亂答 | tool return 要 JSON-serializable (str / dict), 不要 datetime / numpy array; `json.dumps()` 一下 |
| **沒設 max_steps** | loop 跑無限次 | 寫 `for _ in range(N):` 限步數、超過 graceful exit |
| **schema 寫太簡略** | LLM 傳錯 input shape | input_schema 用完整 JSON Schema (required / type / description) |
| **description 寫「找東西」** | LLM 不知何時 call | description 寫「**何時用 + 期望輸入 + 期望輸出**」3 段 |
| **stop_reason 沒檢查** | end_turn 跟 tool_use 混淆 | `if resp.stop_reason == "end_turn": break` 是唯一停的方式 |
| **多家 SDK 不一致** | Anthropic / OpenAI tool call 結構差很多 | 看 [Ch 11 框架](../ch11_frameworks/) 用框架幫你統一介面 |
| **`required` 漏寫** | LLM 傳少參數 | input_schema 寫 `"required": ["arg1", "arg2"]` |
| **tool 自己會 raise** | agent crash | tool 內 try/except, 失敗 return `{"error": "..."}` 讓 LLM 知道 |
| **parallel tool 漏接** | 多 tool_use blocks 只處理 1 個 | iterate `for block in resp.content if block.type == "tool_use"` 全部接 |
| **input 是 dict 還是 str** | `block.input["x"]` vs `json.loads(block.input)` | Anthropic 是 dict, OpenAI tool call arguments 是 JSON string — 看好 SDK 文件 |

---

## 9b. 在這頁直接練 tool use 風格的 prompt

> ⚠️ 真正的 tool use 需要 server 端 wire（這頁沒接工具）。這邊只練習「叫 LLM 用 JSON 表達想 call 什麼工具」的 prompt 風格——下一步就拿去 Ch 12 的 mini framework 真接。

<LLMTryout
  title="Ch 9 in-page tryout — 練「想呼叫工具」的 JSON 輸出"
  defaultSystem="你是 weather assistant。你的回應必須是合法 JSON：{tool: 'get_weather' | 'final', input?: {city: string}, answer?: string}。如果想查天氣回 tool，如果已經有資料回 final。除了 JSON 不要寫任何字。"
  defaultPrompt="台北現在天氣？" />

## 10. 補充閱讀

- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling)
- [Hugging Face Agents Course Unit 1 Bonus — Fine-tune for function calling](https://huggingface.co/learn/agents-course/bonus-unit1/introduction)
- ai-dict Tools & Environments 段

---

> 🛟 **卡關時看這裡**：
> - tool_use 報錯 / 流程不對 → [故障排除 § Tool use](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - tool_use 完整 schema + stop_reason 處理 → [速查卡 § Anthropic SDK](https://symbiosis11503.github.io/agent-z/cheatsheet/sdk#anthropic-sdk-速查)
> - 名詞看不懂 → [70+ 名詞表](https://symbiosis11503.github.io/agent-z/glossary)
