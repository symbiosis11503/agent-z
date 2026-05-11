# Ch 6 — 你的第一個 MCP server

對應 [AgentZ Ch 6](../../chapters/ch06_mcp/)。

寫一個最簡單的 MCP server，3 個工具：

| 工具 | 用途 |
|---|---|
| `count_lines` | 數一個檔案有幾行 |
| `search_in_file` | 在檔案裡 grep |
| `list_files` | 列一個資料夾 |

接 Claude Code 後，你可以直接問「幫我數一下 /tmp/foo.txt 有幾行」，Claude Code 會 call 這個 server。

## 1. 跑

```bash
cd starter-code/ch06_mcp
uv sync   # 裝 mcp lib

# 測試 server 起得來（stdio mode）
uv run server.py
# Ctrl-C 結束（這只是測試啟動，正式用是 Claude Code 自己 spawn）
```

## 2. 接 Claude Code

### Mac / Linux

編輯 `~/.config/claude/claude.json`（沒有就建一個）：

```json
{
  "mcpServers": {
    "agentz-demo": {
      "command": "uv",
      "args": [
        "--directory",
        "/絕對路徑/to/starter-code/ch06_mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

把 `/絕對路徑/to/starter-code/ch06_mcp` 換成你的真實路徑（`pwd` 一下就知道）。

重啟 Claude Code（`/exit` 後重開 `claude`）。

### 確認接上

在 Claude Code 裡敲：
```
/mcp
```
應該看到 `agentz-demo` 在 server 清單裡，狀態 connected。

或敲：
```
什麼 MCP tools 可以用？
```
Claude Code 會列出 `count_lines / search_in_file / list_files`。

## 3. 試用

在 Claude Code 裡：

```
幫我數一下 ~/.zshrc 有幾行
```

Claude Code 會自己 call `count_lines("~/.zshrc")`、回你答案。

```
幫我在 ~/Projects/ai-agent-learning-system/chapters 找有 "ReAct" 字串的章節
```

Claude Code 會跑 `list_files` + 逐檔 `search_in_file` 自己組合答案。

## 4. 在學什麼

| 觀念 | 程式碼在哪 |
|---|---|
| **FastMCP** | `mcp.server.fastmcp.FastMCP` — MCP server 抽象 |
| **@mcp.tool()** | decorator 把函式變 MCP tool，自動產 schema |
| **type hints + docstring** | 變成 tool input schema + description |
| **stdio transport** | Claude Code 跟 server 用 stdin/stdout JSON-RPC 通訊 |
| **return dict** | MCP 自動 serialize 給 client |
| **error handling** | tool 自己回 `{"error": "..."}`，Claude 看到會 retry 或放棄 |

## 5. 練習

- **6.1**: 在 `server.py` 加一個 `write_text_file(path, content)` tool（注意：危險，加 confirmation）
- **6.2**: 把 search_in_file 改成支援 regex（用 `re.search`）
- **6.3**: 加 `git_log(repo_path)` tool 跑 `git log --oneline -10`（用 `subprocess.run`）

## 6. 常見地雷

| 症狀 | 原因 | 解法 |
|---|---|---|
| `/mcp` 顯示 disconnected | `command` 找不到 | 改用絕對路徑、或先 `which uv` |
| server 啟動就 crash | dep 沒裝 | `uv sync` 確認 mcp lib 裝起來 |
| tool 不出現 | docstring 寫錯 / decorator 漏 | `@mcp.tool()` 不能省、docstring 必填 |
| stdio 訊息亂跑 | 你 print() 到 stdout | **不能** `print()` 到 stdout — 用 stderr (`import sys; print(..., file=sys.stderr)`) |
| 改完不生效 | Claude Code 沒重啟 | `/exit` 重新 `claude` |
| Claude 不會用工具 | 沒主動講需要 | 在 prompt 提示「用 agentz-demo 工具」會強些 |

## 7. 進階：把這個跑到 production

```
你的 dev box
    │ stdio
    ▼
Claude Code ──MCP── agentz-demo (這個 server)
    │
    │ HTTP
    ▼
（你想接的東西：DB、API、檔案系統）
```

production 版要加：
- **權限**：哪些路徑能 read / write、用 allowlist
- **rate limit**：避免 LLM 失控狂 call
- **observability**：log 每個 tool call（[Ch 15 audit](../../chapters/ch15_deploy_audit_replay/)）
- **transport**：除了 stdio，MCP 也支援 SSE / WebSocket（多人用、跨機器）

## 補充閱讀

- [MCP 官方 spec](https://modelcontextprotocol.io/)
- [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/mcp)
- [Anthropic — Introducing MCP](https://www.anthropic.com/news/model-context-protocol)
- [Awesome MCP servers (catalog)](https://github.com/punkpeye/awesome-mcp-servers)
- AgentZ [Ch 6 MCP 章節](../../chapters/ch06_mcp/) — 完整概念解說
