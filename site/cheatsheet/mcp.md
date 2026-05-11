---
title: 速查卡 — MCP / Computer Use / Subagent / Skill
description: FastMCP server boilerplate + MCP scope (user/project/local) + Computer Use 2024-10+ + Subagent (Anthropic Agent SDK) + Skill auto-load 順序 + SKILL.md 標準格式。
---

# 速查卡 · MCP / Skills

[← 回速查卡總覽](../cheatsheet)

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

**MCP scope 三層**：
- `user` → `~/.config/claude/claude.json`（全域）
- `project` → repo 內 `.mcp.json`（git commit、團隊共用）
- `local` → repo 內 `.claude/claude.json`（個人 key，**.gitignore**）

```bash
claude mcp add my-server --scope project ./server.py
claude mcp list                     # 看現有 server
claude mcp remove my-server         # 拔
```

---

## Computer Use（Anthropic 2024-10+）

讓 Claude 看 screenshot、移動滑鼠、打字：

```python
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    tools=[
        {"type": "computer_20241022", "name": "computer",
         "display_width_px": 1024, "display_height_px": 768},
        {"type": "text_editor_20241022", "name": "str_replace_editor"},
        {"type": "bash_20241022", "name": "bash"},
    ],
    messages=[{"role": "user", "content": "打開瀏覽器搜尋 'AgentZ'"}],
)
# 處理 tool_use blocks 跑 pyautogui / Selenium / xdotool
```

**必 sandbox**（不然它真的會 click 你的 email）：Docker / VM / 隔離 user。範例容器：`ghcr.io/anthropics/anthropic-quickstarts/computer-use-demo`。

---

## Subagent / Task delegation

主 agent context 太擠時，把子任務外包：

```python
# Anthropic Agent SDK (TypeScript)
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const msg of query({
  prompt: "Survey codebase 30 files, identify 5 hotspots",
  options: {
    agents: {
      "code-surveyor": {
        description: "Read-only file surveyor",
        prompt: "You are a thorough but fast code reader...",
        tools: ["Read", "Grep", "Glob"],
        model: "haiku",
      },
    },
  },
})) {
  console.log(msg);
}
```

Claude Code 用 builtin `Task` tool；自寫 agent 用 sub-`messages.create` call。

---

## Skill auto-load 順序

Claude Code 啟動時依序找 SKILL.md 並讀 frontmatter（only Level 1 always-loaded）：

1. `.claude/skills/<name>/SKILL.md`（project）
2. `~/.claude/skills/<name>/SKILL.md`（user）
3. Plugin marketplace 提供的（裝過後）

要 trigger 一個 skill：description 寫得清楚（< 150 字、含「何時用」），LLM 才會在 conversation 看到正確 signal 後自己叫起來。

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

**下一頁** → [Governance](./governance) · [CLI / Git](./cli) · [SDK](./sdk) · [Pricing](./pricing) · [Patterns](./patterns)
