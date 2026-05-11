# Cheatsheet — 速查卡

單頁濃縮，A4 可印、貼鍵盤旁。學完 AgentZ 後忘了哪個指令、模板、模型名、cost 公式時看這頁。

> 列印建議：瀏覽器 Cmd-P / Ctrl-P → 縮放 75-90%。

[[toc]]

---

## Claude Code CLI 核心指令

```bash
claude                          # 起 Claude Code
claude --plan                   # 開 plan mode 起手
/help                           # 看 builtin commands
/cost                           # 看當前 session 花費
/mcp                            # MCP server status
/skill                          # 看 / 切換 skill
/clear                          # 清 context
/resume                         # 從上次 session 接著跑
/exit                           # 離開
Esc                             # 中斷當前 task
Ctrl-C × 2                      # 強制 exit
```

## CLAUDE.md 推薦結構

```markdown
# 專案規則

## 角色
- 你是 X 工程師，負責 Y。

## 風格
- 繁中、簡潔、不廢話
- 改 code 前先說「我要 X」

## 規則
- 不 force push
- 不 commit 不 review 過的 secret
- 改 prod 前要 confirmation

## 不要
- 不要寫測試（這個專案沒測試框架）
- 不要重構（保持 minimal change）

## 工具
- 我們用 X 不用 Y
```

---

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

---

## Pricing (2026-05 snapshot, USD / 1M token)

| Model | Input | Output |
|---|---|---|
| Haiku 4.5 | $1 | $5 |
| Sonnet 4.6 | $3 | $15 |
| Opus 4.7 | $15 | $75 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4o | $2.5 | $10 |
| Gemini 2.0 Flash | $0.075 | $0.30 |
| Gemini 1.5 Pro | $1.25 | $5 |
| Groq Llama 3.3 70B | $0.59 | $0.79 |
| DeepSeek V3 | $0.27 | — |
| DeepSeek R1 | $0.55 | $2.19 |
| Mistral Large | $2 | $6 |

**Cache hit**：input × 10% (Anthropic / OpenAI 都有)。
**Cache write**：input × 1.25x（首次寫的 overhead）。

[完整 LLM 申請指南 →](./llm-providers)

---

## ReAct loop 範式

```python
def react_loop(goal, max_steps=5):
    history = []
    for _ in range(max_steps):
        thought = llm(prompt=f"Goal: {goal}\nHistory: {history}\nNext?")
        if "FINAL_ANSWER:" in thought:
            return thought.split("FINAL_ANSWER:")[-1]
        # parse: tool_name, args = parse_tool(thought)
        # result = run_tool(tool_name, args)
        history.append({"thought": thought, "result": result})
    return "max steps reached"
```

## Plan-and-Solve 範式

```python
plan = llm("給定 task X，列 5 步驟 plan")
for step in plan:
    result = react_loop(step, max_steps=3)
    if not ok(result):
        plan = revise(plan, result)  # 中途 revise
final = llm("整合 results 寫 answer")
```

## Reflection wrap

```python
draft = base_agent(task)
for _ in range(max_reflect_iters := 3):
    critique = critic_agent(draft)
    if critique.verdict == "pass":
        break
    draft = base_agent(task, critique=critique)
```

---

## Cost cap pattern

```python
import sqlite3, datetime
conn = sqlite3.connect("costs.db")
conn.execute("""CREATE TABLE IF NOT EXISTS calls (
    call_id TEXT, ts TEXT, model TEXT,
    input_tokens INT, output_tokens INT, cost_usd REAL
)""")

DAILY_CAP = 0.10  # USD

def safe_call(**kwargs):
    today_total = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) FROM calls WHERE date(ts)=?",
        (datetime.date.today().isoformat(),)
    ).fetchone()[0]
    if today_total >= DAILY_CAP:
        raise CostCapExceeded(f"${today_total} >= ${DAILY_CAP}")
    resp = client.messages.create(**kwargs)
    # log usage
    conn.execute("INSERT INTO calls VALUES (?, ?, ?, ?, ?, ?)", ...)
    conn.commit()
    return resp
```

[完整 Ch 8 starter →](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch08_cost_observability)

---

## MCP Server boilerplate (Python FastMCP)

```python
from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(arg: str) -> dict:
    """What this does. When to use.

    Args:
        arg: description
    """
    # 注意：不能 print 到 stdout!
    print(f"debug: {arg}", file=sys.stderr)
    return {"result": "..."}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Claude Code 設定 (`~/.config/claude/claude.json`):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/abs/path", "run", "server.py"]
    }
  }
}
```

---

## Skill (SKILL.md) 標準格式

```markdown
---
name: my-skill
description: 一句話 < 150 字, 涵蓋「何時用 + 做什麼」.
---

# Skill 名稱

## When to invoke
User says X / Y / Z.

## What you do
1. Step
2. Step
3. ...

## Constraints
- Never commit/push/delete without approval
- Use existing format

## Example
User: ...
You: ...
```

放在 `.claude/skills/my-skill/` (project) 或 `~/.claude/skills/my-skill/` (user)。

---

## V3 Governance pattern (Production agent)

每次 LLM call → 必走 4 道閘門：

```
1. Cost cap check    (pre-flight, fail-closed)
2. Tool sandbox      (allowed list, deny-by-default)
3. Audit log         (SQLite: ts/run_id/event/payload/cost)
4. Replay record     (input + output + model + temperature)
```

[完整 V3 case →](./chapters/ch15_deploy_audit_replay/)

---

## 模型路由建議

| 任務類型 | 推薦 model |
|---|---|
| Routing / 分類 | Haiku 4.5 / Gemini Flash |
| 摘要 / 整理 | Haiku 4.5 / GPT-4o-mini |
| Coding 修 bug | Sonnet 4.6 / DeepSeek V3 |
| Coding 大重構 | Opus 4.7 |
| 數學 / 推理 | DeepSeek R1 / Opus 4.7 / o1 |
| Embedding | text-embedding-3-small (OpenAI) / cohere multilingual |
| Function calling | Haiku 4.5 (cost) / Sonnet 4.6 (穩) |
| Multi-agent supervisor | Sonnet 4.6 |
| Multi-agent worker | Haiku 4.5 |
| Reviewer / Critic | Sonnet 4.6 |
| Long context (>200K) | Sonnet 4.6 (1M) / Gemini 1.5 Pro (2M) |

---

## Anti-hallucination 5 條 (Researcher 用)

1. 每 citation 必經 DOI / arxiv ID verify
2. 區分 [直接引用] vs [基於 X 推論] vs [推測]
3. Reflection critique 必含 fact-check
4. 多 source 對比 (≥ 2 source 才寫進報告)
5. uncertainty 標記 (不確定日期就只標年份)

[完整 Ch 16 →](./chapters/ch16_researcher/)

---

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

## Git / Repo conventions

```bash
git checkout -b <type>/<feature>     # type: feat / fix / docs / chore
# 寫 code
git add <specific files>             # 不要用 git add -A
git commit -m "feat: add ..."        # imperative mood
git push origin <branch>
gh pr create --title "..." --body "..."  # 用 gh, 不要去 web
```

Commit message 範例：
```
feat: add cost cap fail-closed pattern (Ch 8)

- DAILY_CAP env var
- pre-flight check today's total
- raise CostCapExceeded with explicit message

Closes #42
```

---

## 卡關速查

| 你在 | 看這頁 |
|---|---|
| 不知道哪章開始 | [Quick Win](./quickwin) / [Roadmap](./roadmap) |
| 哪家 LLM 申請 | [LLM / API 申請指南](./llm-providers) |
| 報錯不會修 | [故障排除](./troubleshooting) |
| 不確定該不該讀 | [FAQ](./faq) |
| 名詞看不懂 | [名詞表](./glossary) |
| 做完想 show off | [Capstone Gallery](./capstone) |

---

[首頁](/) · [完整章節](./chapters/ch-1_zero_basics/) · [GitHub](https://github.com/symbiosis11503/agent-z)
