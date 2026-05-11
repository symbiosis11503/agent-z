# Changelog

All notable changes to AgentZ.

## v1.2 — 2026-05-12 (Ralph loop polish wave)

> 連續 ralph-loop session (`UltraThink持續迭代優化agnetZ`)：5 次 iteration 把 v1.1 散落的 gap 收尾。

### 新頁
- **`/cheatsheet`** — A4 可印單頁速查卡（Claude Code CLI / Anthropic SDK / pricing / ReAct / cost cap / MCP boilerplate / SKILL.md / V3 governance 4 道閘門 / 模型路由 / SDK 速比較）
- **`/troubleshooting`** — 12 大類故障排除指南（環境/安裝、API/金鑰、Cost/預算、Agent loop、Tool use、MCP、Memory/RAG、Multi-agent、Production deploy、框架/Skills、Researcher/RL、Web/VitePress）

### 章節常見地雷補完
- 18/20 章補完「常見地雷」結構化 section（Ch -1, 18 by design 不適用）
- 全本「症狀 → 原因 → 解法」格式統一

### Starter code discovery
- 10 章 starter-code 加 🛠 callout 連結，避免 starter dir 成為孤兒
- 修 `pyproject.toml` optional-deps 對齊 5 framework

### 名詞表擴充
- 53 → 62 條（Prompt Cache / stop_reason / Computer Use / Subagent / Deep Research / Headless Agent / Plugin / Agent SDK / MCP Scope）

### Cross-link 補完
- index.md feature card + 「一頁看完」加 速查卡 / 故障排除
- quickwin / roadmap / troubleshooting 互指
- `public/llms.txt` AI-agent 抓站友好的「額外資源」段補 cheatsheet + troubleshooting

## v1.1 — 2026-05-11 (持續迭代擴充)

### 章節深度補完
- **Ch 16 Researcher** 135 → 358 行 — 加完整 arxiv API code / Pipeline multi-agent / Deep research 4 步 / Peer review 4-reviewer / verify_doi 實作 / 常見地雷 8 條 / Anthropic multi-agent case
- **Ch 17 Builder Advanced** 157 → 374 行 — SFT 真實 TRL code / GRPO trainer code / Unsloth/Axolotl 對照 / reward function 4 類設計 / 常見地雷 9 條 / DeepSeek-R1 復現浪潮 case (open-r1/TinyZero)
- **Ch 18 Maker/Educator** 227 → 332 行 — 家庭氣候 agent / Mac menubar Tauri / 教學地雷 6 條 / Capstone Rubric 5 條
- **Ch -1 Zero Basics** 164 → 213 行 — Agent in-action 5 範例 / 你適合讀嗎自我檢查 / 5 個常見誤解

### Starter code 擴充
- **`starter-code/ch11_frameworks/`** — 5 framework 對照：vanilla / LangGraph / CrewAI / Smolagents / Pydantic AI（同任務 5 種寫法 + 7 維度比較表）
- **`starter-code/ch14_multi_agent/`** — 3 架構：Pipeline / Supervisor / Blackboard

### 新頁
- **`/quickwin`** — 5 分鐘 Quick Win，不用裝 Python 看 agent 真的在做事 + 起始章節 Q1-Q3 決策
- **`/llm-providers`** — 11 家 LLM 申請流程 + curl/Python 範例 + 費用 + 怎麼選決策矩陣
- **`/glossary` rewrite** — 50+ 名詞 4 欄完整解釋（含 vibe coding / SDD / TDD / AFK 執行 / TAIDE）

### 治理 + UX
- VitePress sitemap + robots.txt + canonical URL + OG/Twitter meta 完整 SEO
- editLink 函式（handles symlinked chapters/）每頁 footer 「在 GitHub 編輯本頁」
- Homepage hero CTA 改 「5 分鐘 Quick Win」 為 brand action
- Homepage features 加 3 個 (LLM API / TAIDE / 名詞表 50+)
- **CONTRIBUTING.md** — 5 條投稿路徑 + PR 流程 + Style guide + Code of Conduct
- README 重整：Live URL 拉頂 / 6 starter-code 表格 / badges / Status

## v1.0 — 2026-05-11 (initial complete release)

### 20 章繁中 curriculum 全完工

- **前言（Ch-1, 0）** — 真零基礎 onramp（沙發讀 + 工具裝起）
- **Part 1 Watcher（Ch 1-3）** — LLM / Prompt / Agent 概念
- **Part 2 Operator（Ch 4-8）** — CLI agent / CLAUDE.md / MCP / Skills / Cost
- **Part 3 Builder（Ch 9-15）** — tool use → 範式 → 框架 → mini framework → memory → multi-agent → V3 deploy case study
- **Part 4 進階（Ch 16-18）** — Researcher / Builder-RL / Maker+Educator 三條分流

5,280 行繁中、60+ 動手練習。

### 互動 Web App 上線

- VitePress 1.6 + 紫綠漸層 custom theme + dark mode
- 4-part sidebar 折疊式 navigation
- 本地搜尋（繁中 i18n）
- `<LLMTryout />` Vue 元件：4-provider vendor-neutral 即時 API 試（Anthropic / OpenRouter / Groq / OpenAI）— key 留瀏覽器，直連 vendor
- `<ProgressTracker />` 互動進度檢核：localStorage backed、4-stage 分組
- `/progress` / `/glossary` / `/about` 三個輔助頁
- GitHub Pages auto-deploy via Actions
- Live URL: https://symbiosis11503.github.io/agent-z/

### 治理

- MIT License（章節 + starter code 可商用）
- 14 commits 從 init 到 v1 sealed
- Phase 0 survey + Phase 1 UltraThink 完整保留在 repo

### 拍板紀錄

- Boss directive 2026-05-11 12:49: 「ai agent學習系統 / 漸進式」
- 5 個差異化定位拍板：繁中 first / vendor-neutral / Claude Code 生態深 / 真零基礎 / V3 sandbox 整合
- 名稱：AgentZ / 網域：learn.symbiosis.tw / 載體：監修 markdown + 互動 Web App / monorepo / MIT / GitHub Pages auto-deploy

### NOT_YET_DONE (v2 / v3 路線)

- learn.symbiosis.tw custom domain DNS（需 Cloudflare CNAME，CNAME file 已 commit）
- v2 sandbox 串 Helix V3 真實 audit / replay / cost
- 自動 zh-CN / EN 翻譯（co-op-translator）
- 社群投稿 + portfolio leaderboard
- 各章 inline `<LLMTryout />` 嵌入完整 coverage（目前 5/7/10/11/12 已有，其他章節待補）
- starter code Ch 6 (MCP) / Ch 7 (Skills) / Ch 8 (Cost) 尚未補
