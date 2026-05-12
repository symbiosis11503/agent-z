---
title: Ch 4 — CLI Agent 入門
description: Claude Code / Codex CLI / OpenCode 三家對照 + 第一支 agent 跑起來 + 各家 model 綁定差別。
---

# Ch 4 — CLI Agent 入門

> **45-60 分鐘**。讀完你會懂：4 家主流 CLI agent 的差異、怎麼選、怎麼裝 Claude Code、跑出第一個真實 task。
>
> 動手練習：裝 Claude Code、跑第一個 task、讀 tool call trace。
>
> 前置：完成 [Ch 3](../ch03_what_is_agent/) — 已經懂 ReAct 跟 tool_use。

---

## 1. 為什麼開始用 CLI Agent？

Watcher 階段你寫 Python 直接 call API。能跑、能學原理，**但日常工作不會這樣用**——你不會每次想「改個 bug」都重新寫 ReAct loop。

CLI Agent 就是「把 ReAct loop 包好的殼」：
- 自帶 file read / write / bash 工具
- 自帶 git / GitHub / 編輯器 整合
- 自帶 conversation history / undo / interactive prompt
- 多數還能接 MCP server 擴充能力

**重點**：CLI Agent 不是「Web 版聊天的 Terminal 版」。它是**會做事**的——你說「改一個 bug」，它真的去改你的程式碼。

---

## 2. 四家主流 CLI Agent

2026 Q1 的 landscape：

| CLI | 出品 | 主要模型 | 安裝 | 強項 | 弱點 |
|---|---|---|---|---|---|
| **Claude Code** | Anthropic | Claude Sonnet/Haiku/Opus | `npm i -g @anthropic-ai/claude-code` | 寫程式最強、tool use 成熟、MCP/Skills 生態完整 | 綁 Anthropic（但 2026 新增多 provider） |
| **Codex CLI** | OpenAI | GPT-4o 系 | `npm i -g @openai/codex-cli` | 文件型任務強、生態完整 | tool use 比 Claude 略弱 |
| **OpenCode** | 開源社群 | 任一家（OpenRouter）| `npm i -g opencode-ai` | vendor-neutral、開源、可自 host | 沒官方 Skills/MCP 規範、學習曲線陡 |
| **Gemini CLI** | Google | Gemini 2.0/2.5 | `npm i -g @google/gemini-cli` | 1M context 便宜、多模態 | 工具生態剛起步 |

> 💡 **本書範例以 Claude Code 為主**——原因是 MCP / Skills 生態最完整，學會它再學其他家很順。但每一章都會標註「換成 Codex / OpenCode 該怎麼做」對應寫法。

---

## 3. 怎麼選？

```
你的需求？
├─ 寫程式為主 → Claude Code（首選）
├─ 已經有 OpenAI 訂閱 → Codex CLI（接你的 ChatGPT 訂閱 OAuth）
├─ 不想綁單家 vendor / 要 self-host → OpenCode
├─ 預算敏感 + 多模態 → Gemini CLI
└─ 全部都不想試 → 直接寫 Python ReAct（Ch 10 教）
```

---

## 4. 安裝 Claude Code（10 分鐘）

### 前置
- Node.js 18+（沒裝過：`brew install node` macOS / 到 https://nodejs.org 下載 Windows）
- 有 Anthropic API key（[Ch 0 §4](../ch00_setup/) 教過）

### 安裝

```bash
$ npm install -g @anthropic-ai/claude-code
$ claude --version
```

如果不想 `-g`，可以用 `npx @anthropic-ai/claude-code` 每次跑都重抓。

### 第一次啟動

```bash
$ cd ~/agentz-learning   # 用 Ch 0 建的 dir
$ claude
```

第一次會問你登入方式：
- **API key**（推薦新手）：貼 `sk-ant-...`
- **Claude 訂閱 OAuth**：如果你已經是 Claude 訂戶（$20-$200/月），可以用訂閱（不走 API token 計費）

選好之後你會看到一個 Terminal interactive prompt：

```
 ╭───────────────────────────────────────╮
 │ ✻ Welcome to Claude Code              │
 │                                       │
 │   /help for help                      │
 │   /status to view status              │
 ╰───────────────────────────────────────╯

>
```

打字、按 Enter 跟它說話。

---

## 5. 第一個真實 task

打：

```
> 在這個 dir 建一個 hello.txt，內容寫「我學完 Ch 4 了」，然後印 ls -la 確認。
```

Claude Code 會：
1. 用 `Write` 工具建檔
2. 用 `Bash` 工具跑 `ls -la`
3. 把結果整理回給你

關鍵：**你不用 copy-paste 程式碼或檔案內容**——agent 直接動手。

### 看它在做什麼

Claude Code 會在每個工具呼叫前**逐個告訴你**它要做什麼（並等你按 Enter 同意或拒絕）。這叫 **permission mode**，預設保守。

如果你想全自動：`/permission accept-all` 或在 settings.json 設 `default-mode: "accept-edits"`。但**剛開始一定要看每個動作**，學原理。

---

## 6. CLI Agent 看世界的方式

Claude Code 啟動時會：
1. 讀當前目錄 + 父目錄的 `CLAUDE.md`（agent 指令）
2. 讀 `.claude/settings.json`（權限 / hook / MCP server 設定）
3. 讀環境變數（API key / 預設值）
4. 列出可用工具（Read / Write / Edit / Bash / Glob / Grep / ...）

每跟你互動一輪：
- 把上下文（前面對話 + 工具結果）丟回給 LLM
- LLM 決定下一步 tool_use
- agent harness 執行（或問你同意）
- 結果回去給 LLM
- 重複直到 LLM 回最終答案

→ **就是 Ch 3 講的 ReAct loop**。只是有人幫你包好了。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 3 — Tools & Environments**：tools / environments / sandboxing / file system
- **Section 7 — Work Modes**：YOLO mode / human-in-the-loop / accept-all

---

## 8. 動手練習

### 練習 4.1：裝 Claude Code + 第一個 task

完成 §4 安裝、§5 跑「建 hello.txt」task。
**成功標準**：Terminal 真的多了 hello.txt 檔，內容對。**儲存截圖**。

### 練習 4.2：讀 tool call trace

跑 `claude --print "列出當前目錄所有 .py 檔的第一行"` 後，**看 Claude Code 在你 Terminal 印的 tool call 訊息**。

回答：
1. 用了哪幾個工具？
2. 每個工具的 input 大概是什麼？
3. 如果你要用 Python 重寫這個流程，需要 call 幾次 LLM？

**成功標準**：你能用一段話解釋 agent 在做什麼。

### 練習 4.3：試一家備選 CLI

挑 Codex CLI / OpenCode / Gemini CLI 任一個裝起來，做同一個任務（建 hello.txt）。比較：
- 安裝難度
- permission model 預設值
- 對中文的支持
- 你主觀偏好

**成功標準**：寫 5 句話比較。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 4 家主流 CLI agent 的差異
- [ ] 會選擇適合自己情境的 CLI
- [ ] Claude Code 裝好 + 跑過 task
- [ ] 知道 CLI agent 內部就是 ReAct loop
- [ ] 知道什麼是 permission mode、為什麼要保守
- [ ] 跑完練習 4.1 / 4.2 / 4.3

打勾 5 個以上，進 [Ch 5 — CLI Workflow](../ch05_cli_workflow/)。

---

## 9a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **API key 沒 export** | claude 起來說 `ANTHROPIC_API_KEY not set` | `echo $ANTHROPIC_API_KEY` 看是否有 / 加到 `~/.zshrc` 或 `~/.bashrc` |
| **npm 裝錯** | 路徑 / Node 版本衝突 | 用 nvm 把 Node 升到 18+ 後重裝 |
| **CLAUDE.md 沒生效** | Claude 不按你寫的規則 | 確認檔案在 cwd 或 ~/，重啟 Claude Code |
| **token 一下噴光** | $0.50 用一次 chat | 開 `/cost` 看花費；用 Haiku 而不是 Opus；設 `~/.claude/settings.json` model 預設 |
| **agent loop 失控** | 反覆跑同樣的 tool 50 次 | `Esc` 中斷、prompt 加「最多 5 步」、用 plan mode 先看計畫 |
| **改錯檔** | Claude 動了你不想動的檔 | 加 `.claudeignore`、用 git 隨時可 `git checkout` 還原 |
| **MCP server 接不上** | `/mcp` 顯示 disconnected | 看 [Ch 6 §常見地雷](../ch06_mcp/) — 多半是路徑或 dep 問題 |
| **/clear 後失憶** | 之前 context 全沒了 | 重要訊息寫進 CLAUDE.md 或用 `/resume` |
| **plan mode 跳過** | Claude 沒給 plan 就直接動手 | `/plan` 強制進入 plan mode；用 `--plan` flag 啟動時開 |
| **不能跨 session 記東西** | 重啟後不記得昨天教的事 | 寫 CLAUDE.md / SKILL 持久化、或用 memory MCP |

## 9b. 在這頁讓 LLM 幫你比較 CLI

把你的需求貼進去，看 LLM 怎麼推薦 4 家裡的哪一家：

<LLMTryout
  title="Ch 4 in-page tryout — CLI agent 推薦"
  defaultSystem="你是 CLI agent 顧問。看使用者需求，從 Claude Code / Codex CLI / OpenCode / Gemini CLI 4 家挑 1-2 家推薦，並給具體理由。最後給安裝指令。回繁中。"
  defaultPrompt="我主要寫 Python 跟 TypeScript，會用 GitHub、想接 Notion。推薦哪一家？" />

## 10. 補充閱讀

- [Claude Code 官方文件](https://docs.claude.com/en/docs/agents-and-tools/claude-code/overview)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [OpenCode 開源](https://github.com/sst/opencode)
- WenyuChiou Stage A1 CLI agent 入門：https://github.com/WenyuChiou/awesome-agentic-ai-zh
- shareAI-lab/learn-claude-code（60K⭐）— 從零打造 nano claude-code-like harness，看完這本書再讀效果好

---

> 🛟 **卡關時看這裡**：
> - 報錯 / 跑不起來 → [故障排除](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - 忘了指令 → [速查卡 Cheatsheet](https://symbiosis11503.github.io/agent-z/cheatsheet)
> - 名詞看不懂 → [70+ 名詞表](https://symbiosis11503.github.io/agent-z/glossary)
