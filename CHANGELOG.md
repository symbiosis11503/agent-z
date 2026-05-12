# Changelog

All notable changes to AgentZ.

## v1.6 — 2026-05 (Ralph loop iter 21-30: 合規 + 框架校準 + 標準觀測性)

> 第三輪 ralph-loop (`UltraThink持續迭代優化agnetZ`) — 把 2026 業界三大缺口補上：合規標準 / 框架地位變動 / OpenTelemetry GenAI 業界 observability。10 commit 連推 origin/main，每 commit 都 GitHub Actions auto-deploy 到 Pages。

### 名詞表 加 7 個 2026 新詞
- **glossary/agent §5「Multi-Agent Verification / 安全」** — ICE (Iterative Consensus Ensemble) / Consensus Trap (arXiv 2604.17139) / Slopsquatting (Stanford 2026 三大新攻面之一)
- **glossary/production §10「合規 / 國際標準」** — ISO/IEC 42001:2023 / NIST AI RMF + GenAI Profile (NIST-AI-600-1) / EU AI Act 2026-08-02 / OpenTelemetry GenAI Semantic Conventions
- 60+ → **70+ 詞** 標記全站同步

### 章節內容補強
- **Ch 8 §5.1** — 2026-05 多 vendor token 單價對照表 (8 model: DeepSeek V3 / Gemini Flash / Haiku 4.5 / Sonnet 4.6 / GPT-4o / Opus 4.7 …) + 快速估算公式 + 省錢三招
- **Ch 11 §4a** — 2026-05 採用度快照: LangGraph / CrewAI 45.9k★ / AutoGen v0.4 / OpenAI Agents SDK / Smolagents / Pydantic AI + **A2A 協議介紹** (Google + 150+ orgs)
- **Ch 15 §5a** — OpenTelemetry GenAI 業界標準 observability: 標準 span/metric 表 + OpenLLMetry Python SDK 5 分鐘上手範例

### 速查卡新 7th page · Compliance
- **`/cheatsheet/compliance`** — ISO 42001 / NIST AI RMF / EU AI Act / OpenTelemetry GenAI 4 大標準速查 + 何時該做哪個決策樹 + 罰款 + 時程
- 從速查卡「6 個分頁」→「**7 個分頁**」全站 sync (cheatsheet/all include + index hero + quickwin + roadmap + about + 404 + llms.txt + VitePress navbar/sidebar)

### Iter 21-30 commits

| iter | commit | 主題 |
|---|---|---|
| 21 | [4f09afd](https://github.com/symbiosis11503/agent-z/commit/4f09afd) | glossary/production 加合規 4 詞 |
| 22+23 | [0e91588](https://github.com/symbiosis11503/agent-z/commit/0e91588) + [1aeaaf6](https://github.com/symbiosis11503/agent-z/commit/1aeaaf6) | glossary/agent 加 multi-agent 安全 3 詞 (iter 22 漏 Read 跳過, iter 23 fix-up) |
| 24+25 | [089434b](https://github.com/symbiosis11503/agent-z/commit/089434b) + [9171867](https://github.com/symbiosis11503/agent-z/commit/9171867) | ch08 §5.1 vendor 單價表 + 版本命名 align commercial.md (Sonnet 4.6 / Opus 4.7) |
| 26 | [9166a00](https://github.com/symbiosis11503/agent-z/commit/9166a00) | ch11 §4a 採用快照 + A2A 協議 |
| 27 | [e6ce812](https://github.com/symbiosis11503/agent-z/commit/e6ce812) | ch15 §5a OpenTelemetry GenAI |
| 28 | [cfa3a7b](https://github.com/symbiosis11503/agent-z/commit/cfa3a7b) | 速查卡 7th page · Compliance 新建 |
| 29 | [2f5eda6](https://github.com/symbiosis11503/agent-z/commit/2f5eda6) | 全站「6 → 7 個分頁」sync |
| 30 | [7126bc7](https://github.com/symbiosis11503/agent-z/commit/7126bc7) | whatsnew v1.6 entry |

---

## v1.2 — 2026-05-12 (Ralph loop polish wave ✅ sealed @ iter 50/50)

> 連續 ralph-loop session (`UltraThink持續迭代優化agnetZ`)：22 次 iteration (iter 28-49) + iter 50 closeout 把 v1.1 散落的 gap 收尾。Loop 達 max-iterations 50 自然 cap，每次 commit 都 push origin/main。

### 新頁
- **`/cheatsheet`** — A4 可印單頁速查卡（465 行）：Claude Code CLI / Anthropic SDK / pricing / ReAct / cost cap / MCP boilerplate + scope / Computer Use / Subagent / Skill auto-load 順序 / SKILL.md / V3 governance 4 道閘門 / 模型路由 / SDK 速比較
- **`/troubleshooting`** — 12 大類故障排除指南（環境/安裝、API/金鑰、Cost/預算、Agent loop、Tool use、MCP、Memory/RAG、Multi-agent、Production deploy、框架/Skills、Researcher/RL、Web/VitePress）
- **`/whatsnew`** — site-side 版本變動 high-signal 摘要（互指 GitHub CHANGELOG）
- **`/404`** — friendly 找不到頁面 redirect 9 個主要入口

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
- quickwin / roadmap / troubleshooting / 404 互指
- `public/llms.txt` AI-agent 抓站友好的「額外資源」段補 cheatsheet + troubleshooting + whatsnew

### 治理 / UX
- nav 14 → 7 top-bar items + 2 dropdown (工具箱 / 進度&社群) — 解決 mobile / tablet 多列溢出
- `@media print` A4 stylesheet — Cmd-P 就直接清爽 A4 出，不再要手動縮放
- `@media (max-width: 768px)` table 水平 scroll + 緊密 code — 不爆版
- 自訂 404 頁面引導 9 個主要入口
- per-page SEO `description` 4 頁 (cheatsheet / troubleshooting / whatsnew / compare)
- /chapters 符號鏈接 path resolve for editLink

### 章節內 cross-link
- 11/20 章新增「🛟 卡關時看這裡」 footer block — Ch 4/5/6/7/8/9/10/12/13/14/15 各自指 troubleshooting + cheatsheet + glossary chapter-specific anchor
- 同時抓到並修兩個 self-introduced regression:
  - `../../site/X.md` 路徑（GitHub readme OK 但 VitePress deployed broken）→ 絕對 URL
  - VitePress 對 numeric-leading slug 加 `_` 前綴（`#11-...` → `#_11-...`）

### Process notes
- Loop pattern：每 iter 改 → build → commit → push，無 stash / 無 force-push / 無 rebase
- 每個 iter 都單一明確意圖（new page / fix / extend）
- 後半段（iter 47-49）發現自己引入的 regression 並修，比繼續加新功能更有 net value
- Iter 50 為自然 cap（max-iterations 50 命中），DONE 不發 — 因為「持續迭代」directive open-ended 永不 unequivocally true。後續改良走 v1.3 / v2 規劃路線

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
