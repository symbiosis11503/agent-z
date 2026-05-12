---
title: Ch 6 — MCP (Model Context Protocol)
description: 2024-11 Anthropic 開放標準。Tools / Resources / Prompts 三類能力 + FastMCP 寫第一支 server + Claude Code 接法。
---

# Ch 6 — MCP (Model Context Protocol)

> **75-90 分鐘**。讀完你會懂：MCP 是什麼、為何 2024-2026 變主流、stdio vs SSE 兩種傳輸、怎麼裝 Notion / GitHub / 其他 MCP server、自己寫一個 MCP server。
>
> 動手練習：裝 3 個官方 MCP server + 自寫一個 Hello-MCP server。
>
> 前置：完成 [Ch 5](../ch05_cli_workflow/) — CLAUDE.md / slash command 寫得出來。
>
> 🛠 **Starter code**: [`starter-code/ch06_mcp/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch06_mcp) — FastMCP server 3 tools (count_lines / search_in_file / list_files) + Claude Code 接法 + 10 條常見地雷。

---

## 1. 為什麼需要 MCP？

Ch 4-5 你已經會用 Claude Code 內建工具（Read / Write / Bash / Edit / Glob / Grep）。但這些工具只能在**本機檔案系統**做事。如果你想：

- 讀你 Notion 的某個 page
- 改 GitHub 上的 issue
- 從 Slack 拉訊息
- 查公司 Postgres
- 操作 Figma 設計檔

**怎麼辦？**

兩個老答案，都有問題：

**A. 每家寫自己的 plugin 規範**
ChatGPT 有「GPT Actions」、Cursor 有自己的擴充、Claude Code 早期也是。結果：寫一個 Notion 工具，要為每家 agent 寫一次，地獄。

**B. 你自己 wrap API 進 Python 函式給 agent 用**
能跑，但工具 metadata（描述、input schema、auth）每次都要重寫。

**MCP（Model Context Protocol）的目的**就是解這兩題：

> **一個 server 寫一次，所有支援 MCP 的 agent 都能接**。

2024-11 由 Anthropic 提出，2025 年起 Claude Code / Codex / OpenCode / Gemini CLI / Cursor 全都支援。**這是 2025-2026 年 agent 生態最重要的標準**。

---

## 2. MCP 的世界觀

```
┌──────────────┐      MCP protocol       ┌──────────────────┐
│  Agent       │ ◄─────────────────────► │  MCP server      │
│  (Claude     │                          │  (Notion / etc)  │
│   Code)      │                          │                  │
└──────────────┘                          └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  External API    │
                                          │  (Notion / GH)   │
                                          └──────────────────┘
```

- **Agent**（也叫 client）：呼叫工具、接結果
- **MCP server**：暴露一組工具，幫 agent 跟外部 API 對話、處理 auth
- **MCP protocol**：兩邊溝通的 JSON-RPC 規範

關鍵：**MCP server 是獨立行程**——不在 agent 行程內。可能跑在本機（stdio 通訊）或遠端（SSE / WebSocket）。

---

## 3. MCP server 提供的三類東西

MCP server 可以暴露三類「能力」：

| 類別 | 是什麼 | 例子 |
|---|---|---|
| **Tools**（工具） | LLM 可主動呼叫的函式 | `notion_search`, `github_create_issue` |
| **Resources**（資源） | 可讀的內容（檔案、page、DB row） | `notion://page/abc123` |
| **Prompts**（提示模板） | 預定義的 prompt 樣板，使用者觸發 | `/review-pr` slash command 對應 |

90% 的場景只用 Tools。Resources 跟 Prompts 比較新、生態剛起步。

---

## 4. 兩種傳輸方式

### 4.1 stdio（本機）

最常見。MCP server 是個本機行程，agent 透過 stdin/stdout 講話。

特性：
- 安裝就是「裝個 npm/python 套件」
- 啟動由 agent 管理（agent 啟動時 fork server）
- 沒網路、最快
- 認證放本機（API key 在 env / 設定檔）

### 4.2 SSE / Streamable HTTP（遠端）

MCP server 跑在另一台（本機 daemon / cloud），agent 透過 HTTP+SSE 連。

特性：
- 適合「不想每台 dev 機都裝一份」、團隊共享
- 認證要做（OAuth / API token）
- 比 stdio 慢一點

> 💡 **新手先用 stdio**，能 99% 滿足需求。Remote MCP 之後再學。

---

## 5. 怎麼裝 MCP server？

### Claude Code 加 MCP server

兩種設法：

**A. 互動命令**
```bash
$ claude mcp add notion -- npx -y @notionhq/notion-mcp-server
```

**B. 改 `~/.claude/settings.json`**
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "secret_..."
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    }
  }
}
```

下次啟動 Claude Code，`/mcp` 會顯示已連的 server + 它們提供的工具。

### Codex / OpenCode 怎麼設？

Codex CLI 用 `~/.codex/config.toml` 的 `mcp_servers` 區塊。OpenCode 用 `~/.config/opencode/config.json`。**規範一樣、語法略異**。

---

## 5a. MCP Scope — server 放哪一層、作用範圍不同

Claude Code 的 MCP 設定有 3 個 scope，**放錯位置會出現「我裝了，怎麼別的 project 看不到」**：

| Scope | 設定檔位置 | 作用範圍 | 適合什麼 |
|---|---|---|---|
| **user**（全機） | `~/.claude/settings.json` 的 `mcpServers` | 任何 project 啟動 Claude Code 都看得到 | 跨 project 工具：GitHub / Notion / filesystem |
| **project**（共享） | `<repo>/.claude/settings.json` (commit 到 git) | 跟著 repo 走，team 成員 clone 即用 | 該專案專用 server（DB / staging API） |
| **local**（個人） | `<repo>/.claude/settings.local.json` (`.gitignore` 排除) | 只給自己用 | 自己的 PAT / API key 本地測試 |

```bash
# 互動命令直接帶 --scope
$ claude mcp add github --scope user  -- npx -y @modelcontextprotocol/server-github
$ claude mcp add staging-db --scope project -- npx -y @modelcontextprotocol/server-postgres
$ claude mcp add my-test-key --scope local -- ...
```

**判斷準則**：「team 成員都要用同一個 server」→ project；「只有我自己用、不要 commit」→ local；「跨 project」→ user。

> ⚠️ **常見誤解**：把 PAT 寫在 project scope `settings.json`、commit 到 GitHub → token leak。**敏感 env vars 永遠走 local 或 user scope，不 commit。**

---

## 6. 推薦先裝的 6 個 MCP server

| Server | 用途 | 安裝 |
|---|---|---|
| `@modelcontextprotocol/server-filesystem` | 限定 agent 只能存取某些 dir | `npx -y @modelcontextprotocol/server-filesystem /allowed/path` |
| `@modelcontextprotocol/server-github` | GitHub issue / PR / repo | 需 GH PAT |
| `@notionhq/notion-mcp-server` | Notion read/write | 需 Notion integration token |
| `MarkusPfundstein/mcp-obsidian` | Obsidian vault | 需 Obsidian Local REST API plugin |
| `@modelcontextprotocol/server-postgres` | Postgres 查詢 | 需 DB URL |
| `mcp-server-fetch` | 通用 web fetch | 無 auth |

完整 catalog: `WenyuChiou/awesome-agentic-ai-zh` 的 [`mcp-skills-catalog.md`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/mcp-skills-catalog.md) 列了 62 個。

---

## 7. 自己寫一個 Hello-MCP server

寫一個只有一個工具的 MCP server：問它「現在幾點」，它回時間字串。

### Python 版

```bash
$ uv add "mcp[cli]"
```

`hello_mcp.py`：

```python
import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-mcp")

@mcp.tool()
def get_time(timezone: str = "Asia/Taipei") -> str:
    """Return current time in the given IANA timezone."""
    import zoneinfo
    tz = zoneinfo.ZoneInfo(timezone)
    return datetime.datetime.now(tz).isoformat()

if __name__ == "__main__":
    mcp.run()
```

把它加到 Claude Code：

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "uv",
      "args": ["run", "/path/to/hello_mcp.py"]
    }
  }
}
```

重啟 Claude Code，打：

```
> /mcp 看看
> 現在幾點？
```

Claude 應該會呼叫你寫的 `get_time` 工具，回時間。

恭喜——你寫了第一個 MCP server。

### TypeScript 版

```bash
$ npm install @modelcontextprotocol/sdk
```

`hello_mcp.ts`：

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "hello-mcp", version: "0.1.0" });

server.tool(
  "get_time",
  "Return current time",
  { timezone: z.string().default("Asia/Taipei") },
  async ({ timezone }) => {
    const now = new Date().toLocaleString("zh-TW", { timeZone: timezone });
    return { content: [{ type: "text", text: now }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 8. MCP server 的安全性

⚠️ MCP server 拿到的權限有多大？**它能做的所有事**。如果 server 寫得爛或惡意：
- 偷你 API key（從 env 抓）
- 上傳你的檔案（filesystem server 拿到 read 權限）
- 改你的 GitHub repo

**規則**：
1. **只裝官方 / 看過 source / 大社群**的 server
2. 危險工具（filesystem write / shell exec）**限定 path 範圍**
3. 給 server 的 token 用**最小權限**（Notion 只給 read、GitHub 只給某 repo）
4. **定期 audit** mcp.json 看你裝了什麼

---

## 9. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 3 — Tools & Environments**：tools / environments
- 即將收的 MCP / stdio / SSE 條目

---

## 10. 動手練習

### 練習 6.1：裝 3 個 MCP server

從 §6 表挑 3 個你會用的（建議 filesystem + github + fetch），裝起來。
驗證 `claude` 啟動後 `/mcp` 看到它們。

**成功標準**：3 個都接得到、各 call 一次工具成功。

### 練習 6.2：自寫 Hello-MCP

照 §7 寫一個 `hello_mcp.py`（或 `.ts`），有 `get_time` 工具。

**成功標準**：Claude Code 能呼叫到、回時間。

### 練習 6.3：擴充你的 MCP server

加第 2 個工具到 `hello_mcp.py`：`count_words(text: str) -> int`，回字元數。

**進階**：再加 `list_files(dir: str) -> list[str]`，**只允許指定 dir 範圍**（防 path traversal）。

**成功標準**：兩個新工具 Claude Code 都能用、`list_files` 拒絕越界路徑。

---

## 11. 你做完這一章後 ✅

- [ ] 知道 MCP 是什麼、為什麼重要
- [ ] 知道 Tools / Resources / Prompts 三類能力
- [ ] 知道 stdio vs SSE 兩種傳輸
- [ ] 能用 settings.json 加 MCP server
- [ ] 自己寫過 MCP server（Python 或 TS）
- [ ] 知道 MCP server 的安全注意事項
- [ ] 跑完練習 6.1 / 6.2 / 6.3

打勾 5 個以上，進 [Ch 7 — Skills / Plugins / Marketplace](../ch07_skills_plugins/)。

---

## 11a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **disconnected** | `/mcp` 顯示 server status disconnected | command 路徑用絕對路徑 / 看 stderr log / `which uv` 確認 |
| **`print()` 弄壞 stdio** | server 起來但回應亂碼 | stdio mode 下**只能** `print(..., file=sys.stderr)`、stdout 給 MCP 用 |
| **沒重啟 Claude Code** | 改 SKILL.md / 加 server 後沒生效 | `/exit` 重新 `claude` |
| **schema 漏 required** | LLM 漏傳參數 | input_schema 明確列 `required: ["x", "y"]` |
| **fastmcp vs raw mcp 混用** | import / decorator 不對 | 用 `mcp.server.fastmcp.FastMCP` 一路到底，別跨 |
| **tool docstring 沒寫** | LLM 不知何時 call | docstring 寫「**何時用 + 輸入 + 輸出**」3 段 |
| **權限濫開** | server 任何路徑都能讀 / 寫 | allowlist 限白名單路徑、危險操作要 confirmation gate |
| **沒處理錯誤** | 一個 tool fail 整 server crash | 每 tool try/except, return `{"error": ...}` 給 LLM |
| **stdout 亂寫 log** | Claude 收到 JSON-RPC 解析錯誤 | log lib 預設往 stderr; print 改 `print(..., file=sys.stderr)` |
| **MCP server 失控** | LLM 連 50 次 search | server 加 rate limit / max_results cap |

---

## 11b. 在這頁讓 LLM 幫你設計 MCP server

要寫自己的 MCP server？跟 LLM 對話釐清需求：

<LLMTryout
  title="Ch 6 in-page tryout — MCP server 設計徵詢"
  defaultSystem="你是 MCP server 設計顧問。看使用者描述要做的整合，建議：(1) 應該暴露哪幾個 tool (2) 每個 tool 的 input_schema 草稿 (3) 安全注意（auth / sandbox / 權限範圍）。回繁中 + 範例 JSON。"
  defaultPrompt="我想做一個 MCP server 接公司的 Postgres 客戶資料庫，給 sales team 用。" />

## 12. 補充閱讀

- [MCP 官方文件](https://modelcontextprotocol.io)
- [MCP server 開發 SDK（Python / TS / Go / Java）](https://github.com/modelcontextprotocol)
- [Anthropic — Introducing MCP](https://www.anthropic.com/news/model-context-protocol)
- WenyuChiou 62-entry MCP catalog: https://github.com/WenyuChiou/awesome-agentic-ai-zh
- ai-dict Tools & Environments 段：https://ai-dict.gh.miniasp.com/

---

> 🛟 **卡關時看這裡**：
> - MCP server 連不上 / stdout 噪音 / scope 錯 → [故障排除 § MCP](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - FastMCP boilerplate + claude.json 設定 + scope → [速查卡 § MCP](https://symbiosis11503.github.io/agent-z/cheatsheet/mcp#mcp-server-boilerplate-python-fastmcp)
> - 名詞看不懂 → [60+ 名詞表](https://symbiosis11503.github.io/agent-z/glossary)
