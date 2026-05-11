# What's New — 更新紀錄

AgentZ 持續迭代中。這頁是 site-side 「最近一個月做了什麼」的高訊號摘要。完整時間序列見 [CHANGELOG.md](https://github.com/symbiosis11503/agent-z/blob/main/CHANGELOG.md)。

> **Watch the repo** 不定時 polish — [GitHub Watch](https://github.com/symbiosis11503/agent-z) → Releases-only 抓重大改版。

[[toc]]

---

## 2026-05-12 — v1.2 Ralph polish wave

連續 ralph-loop session (iter 28-37) 把 v1.1 散落的 gap 收尾。

### 新頁

- 📋 [**速查卡 Cheatsheet**](./cheatsheet) — A4 可印單頁濃縮 (465 行)，含 Claude Code CLI / Anthropic SDK / pricing / ReAct / cost cap / MCP boilerplate + scope / Computer Use / Subagent / Skill 載入順序 / V3 治理 4 道閘門 / 模型路由 / SDK 速比較
- 🛠 [**故障排除 Troubleshooting**](./troubleshooting) — 12 大類常見錯誤 + 症狀 + 解法，瀏覽器 Ctrl-F 友好
- 📜 [**更新紀錄 What's New**](./whatsnew) — 你正在看的這頁

### 章節補完

- **18/20 章「常見地雷」結構化** — Ch -1 / Ch 18 by design 不適用，其餘全章補完統一格式表（症狀 → 原因 → 解法 → 章節錨點）
- **Starter code discovery** — 10 章加 🛠 callout 直連 `starter-code/` 對應 dir，避免孤兒
- **名詞表 53 → 62 條** — 補 2025-2026 emerging 詞：Prompt Cache / stop_reason / Computer Use / Subagent / Deep Research / Headless Agent / Plugin / Agent SDK / MCP Scope

### 治理 / UX

- nav 14 → 7 top items + 2 dropdown — 解決 mobile / tablet 溢出
- `@media print` A4 stylesheet — Cmd-P 直接清爽 A4，不用手動縮放
- 自訂 404 頁面引導 9 個主要入口（不再「PAGE NOT FOUND」裸頁）

### Cross-link 補完

- index / quickwin / roadmap / troubleshooting / 404 互指
- `public/llms.txt` 補 cheatsheet + troubleshooting + whatsnew URL，AI agent 抓站更精準

---

## 2026-05-11 — v1.1 章節深度補完

從 v1.0 initial release 起 ~半天時間補強。

### 4 章重寫加深

- **Ch 16 Researcher** 135 → 358 行：完整 arxiv API code / multi-agent pipeline / Deep research 4 步 / Peer review 4-reviewer / verify_doi 實作 / 8 條常見地雷 / Anthropic multi-agent case
- **Ch 17 Builder Advanced** 157 → 374 行：SFT 真實 TRL code / GRPO trainer / Unsloth/Axolotl 對照 / reward function 4 類 / 9 條常見地雷 / DeepSeek-R1 復現浪潮（open-r1/TinyZero）
- **Ch 18 Maker/Educator** 227 → 332 行：家庭氣候 agent / Mac menubar Tauri / 教學地雷 6 條 / Capstone Rubric 5 條
- **Ch -1 Zero Basics** 164 → 213 行：Agent in-action 5 範例 / 自我檢查 / 5 個常見誤解

### Starter code 擴充

- `starter-code/ch11_frameworks/` — 5 framework 對照（vanilla / LangGraph / CrewAI / Smolagents / Pydantic AI）
- `starter-code/ch14_multi_agent/` — Pipeline / Supervisor / Blackboard 三架構

### 新頁

- 📋 [`/quickwin`](./quickwin) — 5 分鐘不裝 Python 體驗 agent
- 🔑 [`/llm-providers`](./llm-providers) — 11 家 LLM 申請流程 + curl/Python 範例 + 費用 + 決策矩陣
- 📖 [`/glossary` rewrite](./glossary) — 4 欄完整解釋格式（專業 / 白話 / 範例 / 章節）

### 治理 + UX

- SEO 完整（sitemap / robots.txt / canonical / OG/Twitter meta）
- editLink 函式處理 symlinked chapters/
- Homepage hero CTA 改 Quick Win
- README 重整 + CONTRIBUTING

---

## 2026-05-11 — v1.0 initial complete release

20 章繁中 curriculum 全完工 + 互動 Web App + Live URL 上線。

### 課程

- **前言（Ch-1, 0）** — 真零基礎 onramp
- **Part 1 Watcher（Ch 1-3）** — LLM / Prompt / Agent
- **Part 2 Operator（Ch 4-8）** — CLI agent / MCP / Skills / Cost
- **Part 3 Builder（Ch 9-15）** — tool use → 範式 → mini framework → memory → multi-agent → V3 deploy case
- **Part 4 進階（Ch 16-18）** — Researcher / Builder-RL / Maker+Educator 三分流

5,280 行繁中、60+ 動手練習。

### 平台

- VitePress 1.6 + custom theme + dark mode
- 4-part sidebar 折疊
- 本地搜尋（繁中 i18n）
- `<LLMTryout />` 4-provider vendor-neutral 即時試 API
- `<ProgressTracker />` localStorage milestone tracker
- GitHub Pages auto-deploy
- Live URL: <https://symbiosis11503.github.io/agent-z/>

---

## 路線

- **v1.x**（current）— markdown + VitePress + PDF release，持續 ralph-loop polish
- **v2**（規劃中）— 每章動手練習可在頁面內串 Helix V3 sandbox 真跑
- **v3**（規劃中）— 自動 zh-CN / EN 翻譯、社群投稿、portfolio leaderboard

---

## 訂閱方式

- **GitHub Watch** — Releases-only：重大改版才提醒
- **GitHub Discussions** — [#announcements](https://github.com/symbiosis11503/agent-z/discussions)
- **RSS** — Releases atom feed：<https://github.com/symbiosis11503/agent-z/releases.atom>

---

[首頁](/) · [完整 CHANGELOG](https://github.com/symbiosis11503/agent-z/blob/main/CHANGELOG.md) · [GitHub](https://github.com/symbiosis11503/agent-z)
