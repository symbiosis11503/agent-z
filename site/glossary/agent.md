---
title: 名詞表 — Agent 機制 + CLI Agent / Claude Code 生態系 + Multi-Agent 安全
description: Agent / Tool Use / ReAct / Plan-and-Solve / Reflection / Runaway / stop_reason / Computer Use / Subagent / Deep Research / Headless Agent + CLI Agent / MCP / Skill / Progressive Disclosure / Slash Command / Hook / Plugin / Agent SDK / MCP Scope + ICE / Consensus Trap / Slopsquatting
---

# 名詞表 · Agent 機制 + CLI Agent / Claude Code 生態系

[← 回名詞表總覽](../glossary)

## 3. Agent 機制

### 智能體 / Agent
- **專業**：LLM + 工具集 + 控制循環的系統。Agent 能根據目標自主決定下一步 action（call tool / 給回答 / 結束）。
- **白話**：會自己跑流程的 LLM。你給目標、它自己決定要查什麼 / 點什麼 / 做什麼步驟。
- **範例**：你說「幫我訂下週去東京的便宜機票」、agent 自己 search 機票網、比價、填表、回報。ChatGPT 只會建議你去哪查；agent 真的去查。
- **章節**：[Ch 3](../chapters/ch03_what_is_agent/)

### 工具呼叫 / Tool Use / Function Calling
- **專業**：LLM 在生成回應時，依 prompt 中提供的 tool schema，emit 一個 `tool_use` block（含 tool name + JSON input），由外部 agent harness 真實執行後把 result 塞回 messages，LLM 繼續推論。
- **白話**：LLM 不會真的點滑鼠、按按鈕。它寫「我想呼叫這個函式」的便條紙、外部程式幫它跑，把結果回去給它看。
- **範例**：你問「台北現在幾度」、LLM 回 `{"type":"tool_use","name":"get_weather","input":{"city":"Taipei"}}`、你的 agent 真的去打 weather API、把 26°C 回去、LLM 再回給你「台北 26°C」。
- **章節**：[Ch 3 §2](../chapters/ch03_what_is_agent/#2-tool-use-llm-怎麼呼叫工具)

### ReAct / ReAct (Reason + Act)
- **專業**：2022 年 Yao et al. 提出的 agent 循環模式。每一步 LLM 先 reason（用自然語言講「我下一步該做什麼」）再 act（call tool），observe 工具結果後再 reason 下一步。
- **白話**：agent 的「想一下 → 做 → 看結果 → 再想 → 再做」迴圈。是 2025 年多數 agent 的核心。
- **範例**：Claude Code / Codex / OpenCode 內部都是 ReAct 的變體 + 多 polish。
- **章節**：[Ch 3 §3](../chapters/ch03_what_is_agent/#3-react-reason--act-循環)

### 計畫先行 / Plan-and-Solve
- **專業**：把 agent 跑分兩階段——planner 先用 LLM 生出完整步驟、executor 再照 plan 一步步執行。
- **白話**：先列 to-do list、再照做。不是邊做邊想。
- **範例**：「研究 3 個 framework 寫比較表」——先 plan「1. 各自 google 2. 抓官網 3. 比較 4. 整合」、再執行。
- **章節**：[Ch 10 §3](../chapters/ch10_react_paradigms/#3-plan-and-solve)

### 反思 / Reflection (Reflexion)
- **專業**：agent 完成 task 後，self-critique 答案品質、不滿意就 redo。需要可驗證的 reward signal（test pass / 評分 / 比對）。
- **白話**：做完自己挑毛病、不滿意重做。多 LLM call 換高品質。
- **範例**：寫 code 後跑 test、test 失敗就根據 error message 改 code 再跑。
- **章節**：[Ch 10 §4](../chapters/ch10_react_paradigms/#4-reflection)

### 失控 / Runaway / Tool Loop
- **專業**：agent 因 reasoning bug 或 environment feedback 不穩，重複 call 同一個 tool 或無限擴張 scope，導致成本失控。
- **白話**：agent 跑著跑著瘋掉了：一直 retry / 一直改 / 一直跑 test，停不下來。
- **範例**：你說「修這個 bug」、它變「修 bug + 重構 module + 加 test + 寫 doc」——一個 task 燒 $20。Ch 8 §3 教 3 個 pattern 怎麼防。
- **章節**：[Ch 8 §3](../chapters/ch08_cost_observability/#3-三個常見-燒錢失敗模式)

### 停止原因 / stop_reason
- **專業**：Anthropic API response 的終止狀態欄位：`end_turn`（自然結束）/ `tool_use`（要 call tool）/ `max_tokens`（超 token limit）/ `stop_sequence`（撞 stop_sequences）/ `pause_turn`（長 server-tool 暫停）/ `refusal`（safety reject）。
- **白話**：LLM 為什麼停下來？分手對方說「我講完了」/「該你了去 call tool」/「字數爆了」/「碰到禁字」。寫 agent loop 必須對每種反應。
- **範例**：`if resp.stop_reason == "tool_use": run tool 然後 append tool_result; elif "end_turn": done; elif "max_tokens": 提示 user / 縮 prompt 重試`。
- **章節**：[Ch 9](../chapters/ch09_function_calling/) + [速查卡 SDK](../cheatsheet/sdk#anthropic-sdk-速查)

### 電腦使用 / Computer Use
- **專業**：2024-10 Anthropic 推出的 Claude 能力。Claude 透過 screenshot tool + mouse/keyboard tool 操作真實桌面 GUI（不是 API）。包在 `computer_20241022` tool type。
- **白話**：讓 Claude 真的看你螢幕、移動滑鼠、打字。可以填網頁表單、跑沒 API 的軟體。
- **範例**：Claude in Chrome / claude-in-chrome MCP / Anthropic computer-use demo container。要 sandbox 跑（不然它真的會點你的 email）。**Ch 18 Maker 路線會用到**。
- **章節**：[Ch 18](../chapters/ch18_maker_educator/)

### 子代理 / Subagent
- **專業**：透過 Task / Agent tool 由主 agent 啟動的隔離子 conversation。子 agent 有自己 context / system prompt / tool 集，跑完只回傳結果給主 agent，原始 trace 不污染主 context。
- **白話**：「派下去做的小弟」。主 agent 把「搜尋 codebase 30 個檔」這種大任務外包給 subagent、自己保持乾淨 context。
- **範例**：Claude Code 的 Task tool / Explore agent / Plan agent；自己寫 agent 用 sub-LLM 處理子任務。**節省 context 是 multi-agent 的入門用法**。
- **章節**：[Ch 14](../chapters/ch14_multi_agent/)

### 深度研究 / Deep Research
- **專業**：長 horizon agent，跨 10-50 個 web search / paper read / cross-reference 後產出研究報告。需要 cost cap + DOI 驗證 + reflection critique 防幻覺。
- **白話**：「丟一個問題、讓 agent 跑半小時、給我一份報告」的研究模式。ChatGPT / Claude / Gemini 都有 Deep Research mode。
- **範例**：OpenAI Deep Research、Gemini Deep Research、Claude Research、ChatGPT Atlas Agentic Search。AgentZ Ch 16 教你自己寫一個。
- **章節**：[Ch 16](../chapters/ch16_researcher/)

### 後台 / 排程代理 / Headless / Scheduled Agent
- **專業**：無人盯著、由 cron / launchd / systemd timer 觸發的 agent，跑完寫 log / 發通知。架構必含 cost cap、retry policy、failure alert。
- **白話**：「不開電腦也會自己跑的 agent」。例：每天早上 6:00 抓新聞重點寄你 mailbox。
- **範例**：morning briefing agent（Ch 18）、夜跑 deep research、定時 codebase audit。AFK 執行的具體實作形式。
- **章節**：[Ch 18 §3](../chapters/ch18_maker_educator/) + [Ch 8](../chapters/ch08_cost_observability/)

---

## 4. CLI Agent / Claude Code 生態系

### 命令列代理 / CLI Agent
- **專業**：以 Terminal / shell 為介面的 agent harness，內建 file read/write / Bash / Edit / Glob / Grep 等工具，啟動會載入 CLAUDE.md 等 config。
- **白話**：在你電腦 Terminal 跑、會做事的 agent 殼。打字跟它說「修這個 bug」、它真的去改你的程式碼。
- **範例**：Claude Code（`claude` 指令）、OpenAI Codex CLI、OpenCode、Gemini CLI 是 2026 Q1 四大主流。
- **章節**：[Ch 4](../chapters/ch04_cli_agents/)

### 模型上下文協議 / MCP (Model Context Protocol)
- **專業**：2024-11 Anthropic 提出的開放標準。透過 JSON-RPC（stdio / SSE 傳輸）讓 agent client 跟外部 server 對話，server 暴露 Tools / Resources / Prompts 三類能力。
- **白話**：「agent ↔ 工具」的共通語言。寫一次 MCP server，Claude Code / Codex / OpenCode 全都能接，不用為每家 agent 各寫一次。
- **範例**：裝 `notion-mcp-server` → 你的 Claude Code 立刻能讀寫 Notion；裝 `github-mcp-server` → 能 review PR / 開 issue。62-entry catalog 在 WenyuChiou repo。
- **章節**：[Ch 6](../chapters/ch06_mcp/)

### 技能 / Skill
- **專業**：給 LLM 的 markdown 文件（含 frontmatter description）+ 可選 reference files + 可選 scripts。LLM 看到觸發條件自動載入 SKILL.md 主體，按需展開 reference。
- **白話**：給 LLM 看的「規格書 / SOP / cheat sheet」。MCP 是「函式庫」，Skill 是「教戰手冊」。
- **範例**：寫一個 `email-customer` skill，含「寫客戶信的 5 步驟 SOP」+ tone-guide.md reference。下次你說「幫客戶 X 寫詢價信」、Claude Code 自動載入 skill 按 SOP 走。
- **章節**：[Ch 7](../chapters/ch07_skills_plugins/)

### 漸進式揭露 / Progressive Disclosure
- **專業**：Skill 設計 pattern。Level 1 frontmatter always-loaded（10 行）、Level 2 SKILL.md body 觸發後載入（< 500 行）、Level 3 reference/ subdir LLM 主動 fetch（細節 SOP / scripts）。
- **白話**：別把所有資料塞一份大文件給 LLM 看（耗 token + 失焦）。先給目錄、要用到細節再讀。
- **範例**：`email-customer/SKILL.md` 只列 5 步驟、tone 風格詳細寫在 `reference/tone-guide.md`、客戶寫信範本在 `reference/examples.md` — LLM 需要時才讀。
- **章節**：[Ch 7 §3](../chapters/ch07_skills_plugins/#3-progressive-disclosure-skill-的核心設計-pattern)

### 斜線指令 / Slash Command
- **專業**：Claude Code 中 `/<name>` 觸發的預存 prompt，存在 `.claude/commands/<name>.md`（專案級）或 `~/.claude/commands/`（全域）。可帶參數。
- **白話**：把常用的長 prompt 存檔、打 `/<名字>` 就觸發。省每次重打 + 確保格式一致。
- **範例**：`/commit` → 看 staged changes 寫 commit message 等你 confirm；`/translate-zh <text>` → 帶參數翻譯。
- **章節**：[Ch 5 §3](../chapters/ch05_cli_workflow/#3-slash-command-自製)

### 鉤子 / Hook
- **專業**：Claude Code settings.json 的 `hooks` 區塊，定義 PreToolUse / PostToolUse 等事件觸發時跑的 shell 指令。可攔截 / 修改 / 紀錄工具行為。
- **白話**：「agent 動之前 / 之後幫我跑這個」的自動化規則。
- **範例**：PostToolUse 配 `Write|Edit` → 自動 `npm run lint --fix`；PreToolUse 配 `Bash` → 看到 `rm -rf` 直接擋。
- **章節**：[Ch 5 §6](../chapters/ch05_cli_workflow/#6-hook-在工具呼叫前後跑你的-code)

### 插件 / Plugin
- **專業**：Claude Code 的擴充封裝單位。一個 plugin 可以同時帶 commands / agents / hooks / MCP server / skills，透過 marketplace.json 散發。比起單純 Skill / MCP，是更完整的「功能套件」。
- **白話**：「一包裝好的功能」。裝一個 plugin 等於同時加幾個 slash command、subagent、hook、MCP server。
- **範例**：`claude-config plugin install @anthropic/example-plugin`；公司內部 marketplace 散發部門通用工具集。
- **章節**：[Ch 7](../chapters/ch07_skills_plugins/)

### Agent SDK / Claude Agent SDK
- **專業**：Anthropic 官方的 Python / TypeScript SDK（npm `@anthropic-ai/claude-agent-sdk`），把 Claude Code 內部 agent loop 抽出來給開發者直接用：載 system prompt / 工具集 / hooks / subagent 等。
- **白話**：「把 Claude Code 變成你 app 的一部分」的 SDK。不只 API call，是完整 agent loop。
- **範例**：用 Agent SDK 寫一個只跑你公司 SOP 的內部 agent、嵌入 Slack bot 或 web app。
- **章節**：[Ch 12](../chapters/ch12_mini_framework/) + [Ch 18](../chapters/ch18_maker_educator/)

### MCP 範圍 / MCP Scope
- **專業**：Claude Code 註冊 MCP server 的層級，影響可見性：`user` 範圍寫到 `~/.config/claude/claude.json`（全域）/ `project` 範圍寫到 `.mcp.json`（per-repo）/ `local` 範圍寫到 `.claude/claude.json`（per-repo 隱私）。
- **白話**：「這個 MCP server 哪些 session 看得到」。個人工具放 user；公司 repo 共用放 project；不想 git commit 的私人 key 放 local。
- **範例**：`claude mcp add notion-mcp ... --scope user` vs `--scope project`；專案內 mcp.json 進 git，個人 key 用 user-scope。
- **章節**：[Ch 6](../chapters/ch06_mcp/)

---

## 5. Multi-Agent Verification / 安全（2026 新加）

### 迭代共識集成 / ICE (Iterative Consensus Ensemble)
- **專業**：跨 LLM ensemble 方法。讓 3 個（或 N 個）獨立 LLM 各自產出 → 互相 critique 一輪 → 收斂到 consensus。2025 醫療 benchmark 顯示 +7-15 點 accuracy（無 fine-tune），GPQA-diamond 從 46.9% → 68.2%。Agenvoy 用 4-CLI × ≤3 輪是同一家族。
- **白話**：「3 個 AI 互相吵架直到吵出一致答案」。比單一 LLM 更可靠，但成本 × 3-9。
- **範例**：critical action（金錢 / 不可逆 / 對外發布）強制走 ICE — 三家 LLM 一致 vote 通過才執行；任一家反對就 escalate 給人。
- **章節**：[Ch 14 multi_agent](../chapters/ch14_multi_agent/) + [Ch 15 §3](../chapters/ch15_deploy_audit_replay/)

### 共識陷阱 / Consensus Trap
- **專業**：response-level voting 的數學漏洞 — 當 corrupted agents 形成 local majority 時，傳統「投票決勝」會 collapse（多數決變成多數錯）。2026 arXiv 2604.17139 點出 + 提出 token-level collaboration 作為解。
- **白話**：「3 個 AI 投票，如果其中 2 個被偷偷植入後門，多數決就被綁架」。要改成 token 層級對齊不是 response 層級。
- **範例**：multi-agent 系統用 majority-vote 決定執行 → 攻擊者只要污染 2/3 agent prompt 即可改變決策。防護：token-level aggregation + Byzantine-resilient consensus (HDETM / DDHR)。
- **章節**：[Ch 14 §6](../chapters/ch14_multi_agent/) + [Ch 15 §3](../chapters/ch15_deploy_audit_replay/)

### 幻覺搶註 / Slopsquatting
- **專業**：供應鏈攻擊變體。LLM 約 20% 建議的 package 名實際不存在於 npm / PyPI；攻擊者監測 LLM 輸出，搶註那些 hallucinated 名稱、放上惡意 payload。Stanford AI Index 列 2026 三大新攻面之一（與 agent identity / orchestration layer 並列）。命名 by Seth Larson (Python Software Foundation) 2025。
- **白話**：「AI 推薦的包名可能是它自己編的，攻擊者就去搶註那個假名等你裝」。比傳統 typosquatting 更狠 — typo 至少還是真名打錯，slopsquat 是 AI 編的「不存在的名」。
- **範例**：Copilot 建議 `pip install awesome-llm-helper` → 那 package 不存在 → 攻擊者註冊它 → 含 wallet stealer → 用戶照 LLM 建議裝 → 中招。防護：① 不直 install LLM 推薦包 ② pin registry source of truth ③ 隔離 container 內測 install ④ Aikido SafeChain / Socket 等掃工具。
- **章節**：[Ch 15 §3](../chapters/ch15_deploy_audit_replay/) + [Ch 6 §8](../chapters/ch06_mcp/#8-mcp-server-的安全性)

---

**其他類別** → [基礎](./foundation) · [Agent / CLI](./agent) · [實務](./practice) · [Production](./production) · [台灣/混淆 pair](./taiwan-misc)
