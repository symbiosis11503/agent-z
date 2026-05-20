# Changelog

All notable changes to AgentZ.

## v1.8 — 2026-05-20 (競品 Survey 內化)

> 5 大 Agent Platform survey 的精華變成 AgentZ 教學內容。不是翻譯 survey，是把 pattern 變成可教、可練、可帶走的知識。iter 51-55, 5 commits.

### 新增章節內容

| iter | commit | 章節 | 內容 |
|---|---|---|---|
| 51 | `3eea2d7` | Ch 11 §5b | Agent Platform/OS 品類 — 5 platform + 5 design patterns + 選擇指南 |
| 52 | `359e83a` | Ch 13 §8a | Self-Learning Loop (from Hermes) — 原理 / GovernedLearning / 練習 13.4 |
| 53 | `773a13e` | Ch 14 §7a | Cross-Model Review (from Agenvoy) — async 實作 / cost-saving variant / 練習 14.4 |
| 54 | `b6d0adc` | Ch 15 §5c | 4-Layer Security Hardening (from Klawty + OpenFang) — sandbox / policy / Merkle audit / supply chain |
| 55 | `a63357b` | Ch 3 §4a | Agent 演化路線圖 — Level 0 (LLM call) → Level 4 (Agent OS) |

### Survey 來源

- OpenClaw (372k★) / Hermes Agent (80k+★) / Agenvoy (5k★) / Klawty (2k★) / OpenFang (17.5k★)
- Zo Computer (always-on cloud agent)
- Agenvoy vs Hermes 深度比較

### NOT in this version

- index.md / chapters.md 規模數字更新（下版）
- llms.txt 全文同步（下版）
- 新 starter-code（跟新練習對應的 code 下版補）

---

## v1.7 — 2026-05-12-13 (Ralph loop cycle 1: 讓人帶走它)

> 第四輪 ralph-loop. 主軸不是補章節，是讓 AgentZ 從「自閉好內容」→「真能 spread 的開源教程」。v1.6 = 內容變強；v1.7 cycle 1 = **外帶 surface**. 6 commits push origin/main, GH Pages auto-deploy.

### Cycle 1 — 引用 / 社群 / 分享 / 安裝 (iter 39-44)

**引用化（學術可用）**
- **`/cite`** — BibTeX / APA 7th / Chicago 17th / CITATION.cff / Markdown 5 格式 — researcher / 教材作者 / blog 一鍵 copy
- CC-BY-4.0 內容 + MIT code 授權明白標註，避免引用時不確定
- 提示用 Wayback Machine 防 link rot

**社群正式邊界**
- **CODE_OF_CONDUCT.md** — 改寫 Contributor Covenant 2.1，繁中口語化，24h 通報窗口 + 5 級處理 + 範圍說明
- **about.md「社群」章節** — 6 行對照表（bug / Discussion / PR / Capstone / cite / CoC）每場合一個入口不混
- **全站 nav 加 💬 Discussions + Issues** 兩個外部入口

**分享 / Link preview 化**
- **og-image.png** 1200×630 — Twitter / FB / LinkedIn / Slack / Discord 貼 AgentZ URL 終於有正式 link preview
- 4 chip 標：20 章 / Vendor-neutral / Claude Code 一級 / v1.6 · 2026
- VitePress `transformPageData` per-page meta inject — 每頁 og:title / og:description / og:url / twitter:image 都自動帶當前頁面

**PWA installable**
- **manifest.json** — Chrome / Edge / iOS Safari 可「Add to Home Screen」標準 PWA
- Apple meta 4 條 (mobile-web-app-capable / status-bar-style / title `AgentZ` / theme-color #5b21b6)

### commits

| iter | commit | 主題 |
|---|---|---|
| 39 | [eda7975](https://github.com/symbiosis11503/agent-z/commit/eda7975) | `/cite` page (BibTeX/APA/Chicago/CITATION.cff) |
| 40 | [2579fc3](https://github.com/symbiosis11503/agent-z/commit/2579fc3) | CODE_OF_CONDUCT.md + nav Discussions/Issues + about.md 社群對照表 |
| 41 | [c21d110](https://github.com/symbiosis11503/agent-z/commit/c21d110) | og-image 1200×630 PNG (sips SVG→PNG) + per-page meta inject |
| 42 | [95dcc4e](https://github.com/symbiosis11503/agent-z/commit/95dcc4e) | PWA manifest.json + Apple meta |
| 43 | [0a505af](https://github.com/symbiosis11503/agent-z/commit/0a505af) | whatsnew v1.7 cycle 1 entry |
| 44 | [fc336c5](https://github.com/symbiosis11503/agent-z/commit/fc336c5) | index.md 規模 v1.6→v1.7 cycle 1 + 一頁看完加 /cite |

### NOT in v1.7 cycle 1

- 沒做 service worker / offline mode
- 沒做 i18n (EN / 簡中) — 留 v1.8+
- 沒做 self-check quiz per chapter — 留 cycle 2
- 沒做 skill tree visualization — 留 cycle 2

---

## v1.6 — 2026-05 (Ralph loop 雙 cycle: 合規 + 框架校準 + 標準觀測性 + 章節 cross-link)

> 第三輪 ralph-loop (`UltraThink持續迭代優化agnetZ`) — 兩 agent 平行跑：cycle 1 把 2026 業界三大缺口補上（合規 / 框架 / OTel），cycle 2 把新詞反向 cross-link 進章節原生 context。約 17 commit 連推 origin/main，每 commit 都 GitHub Actions auto-deploy 到 Pages。

### Cycle 1 — 名詞表 + 章節 §補強 + Compliance 速查卡 (iter 21-31)

**名詞表 加 7 個 2026 新詞**
- **glossary/agent §5「Multi-Agent Verification / 安全」** — ICE (Iterative Consensus Ensemble) / Consensus Trap (arXiv 2604.17139) / Slopsquatting (Stanford 2026 三大新攻面之一)
- **glossary/production §10「合規 / 國際標準」** — ISO/IEC 42001:2023 / NIST AI RMF + GenAI Profile (NIST-AI-600-1) / EU AI Act 2026-08-02 / OpenTelemetry GenAI Semantic Conventions
- 60+ → **70+ 詞** 標記全站同步

**章節內容補強**
- **Ch 8 §5.1** — 2026-05 多 vendor token 單價對照表 (8 model: DeepSeek V3 / Gemini Flash / Haiku 4.5 / Sonnet 4.6 / GPT-4o / Opus 4.7 …) + 快速估算公式 + 省錢三招
- **Ch 11 §4a** — 2026-05 採用度快照: LangGraph / CrewAI 45.9k★ / AutoGen v0.4 / OpenAI Agents SDK / Smolagents / Pydantic AI + **A2A 協議介紹** (Google + 150+ orgs)
- **Ch 15 §5a** — OpenTelemetry GenAI 業界標準 observability: 標準 span/metric 表 + OpenLLMetry Python SDK 5 分鐘上手範例

**速查卡新 7th page · Compliance**
- **`/cheatsheet/compliance`** — ISO 42001 / NIST AI RMF / EU AI Act / OpenTelemetry GenAI 4 大標準速查 + 何時該做哪個決策樹 + 罰款 + 時程
- 從速查卡「6 個分頁」→「**7 個分頁**」全站 sync (cheatsheet/all include + index hero + quickwin + roadmap + about + 404 + llms.txt + VitePress navbar/sidebar)

### Cycle 2 — 新詞反向 cross-link 進章節 (iter 27-33 平行)

把名詞表新詞跟既有舊詞下放到原生章節 context，讀者翻章節就遇得到、不用 jump 名詞表：

- **Ch 14 §8c** — 2026 multi-agent 新興安全議題（ICE / Consensus Trap / Slopsquatting 在 Ch 14 multi-agent 場景下的影響 + 防禦）
- **Ch 15 §5b** — 合規對照（ISO 42001 / NIST RMF / EU AI Act → V3 四 pillar 映射 + 風險分級 + incident reporting）
- **Ch 6 §5a** — MCP Scope（user/project/local 3 層作用範圍 + 敏感 token 安全準則）
- **Ch 9 §4a** — Computer Use（Anthropic 特殊 tool-use 模式 + sandbox 安全）
- **Ch 5 §6a** — Headless Agent（`claude -p` cron / CI / shell pipe 用法 + 不問 permission 的安全提醒）

### 全部 commits

**Cycle 1**:
| iter | commit | 主題 |
|---|---|---|
| 21 | [4f09afd](https://github.com/symbiosis11503/agent-z/commit/4f09afd) | glossary/production 加合規 4 詞 |
| 22+23 | [0e91588](https://github.com/symbiosis11503/agent-z/commit/0e91588) + [1aeaaf6](https://github.com/symbiosis11503/agent-z/commit/1aeaaf6) | glossary/agent 加 multi-agent 安全 3 詞 (iter 22 漏 Read 跳過, iter 23 fix-up) |
| 24+25 | [089434b](https://github.com/symbiosis11503/agent-z/commit/089434b) + [9171867](https://github.com/symbiosis11503/agent-z/commit/9171867) | ch08 §5.1 vendor 單價表 + 版本命名 align commercial.md (Sonnet 4.6 / Opus 4.7) |
| 26 | [9166a00](https://github.com/symbiosis11503/agent-z/commit/9166a00) | ch11 §4a 採用快照 + A2A 協議 |
| 27 | [e6ce812](https://github.com/symbiosis11503/agent-z/commit/e6ce812) | ch15 §5a OpenTelemetry GenAI |
| 28 | [cfa3a7b](https://github.com/symbiosis11503/agent-z/commit/cfa3a7b) | 速查卡 7th page · Compliance 新建 |
| 29 | [2f5eda6](https://github.com/symbiosis11503/agent-z/commit/2f5eda6) | 全站「6 → 7 個分頁」sync |
| 30 | [7126bc7](https://github.com/symbiosis11503/agent-z/commit/7126bc7) | whatsnew v1.6 entry (cycle 1) |
| 31 | [ac4ebb5](https://github.com/symbiosis11503/agent-z/commit/ac4ebb5) | CHANGELOG v1.6 entry |

**Cycle 2** (平行 agent):
| iter | commit | 主題 |
|---|---|---|
| 27 (cycle 2) | [d2db5e5](https://github.com/symbiosis11503/agent-z/commit/d2db5e5) | 60+ → 70+ 名詞表 truth-sync (4 files) |
| 28 (cycle 2) | [f824b37](https://github.com/symbiosis11503/agent-z/commit/f824b37) | ch14 §8c multi-agent 新興安全 |
| 29 (cycle 2) | [57a9e08](https://github.com/symbiosis11503/agent-z/commit/57a9e08) | ch15 §5b 合規對照 → V3 四 pillar 映射 |
| 30 (cycle 2) | [0a3c732](https://github.com/symbiosis11503/agent-z/commit/0a3c732) | ch06 §5a MCP Scope |
| 31 (cycle 2) | [d3d58a1](https://github.com/symbiosis11503/agent-z/commit/d3d58a1) | ch09 §4a Computer Use |
| 32 | [87d8da6](https://github.com/symbiosis11503/agent-z/commit/87d8da6) | ch05 §6a Headless Agent |
| 33 | [a6651e4](https://github.com/symbiosis11503/agent-z/commit/a6651e4) | whatsnew v1.6 cycle 2 |

### v1.6 收尾 polish (iter 34-49)

兩 cycle 完工後 16 次 polish 把零散 truth-sync 收乾淨：

| iter | commit | 主題 |
|---|---|---|
| 34 | [b11e669](https://github.com/symbiosis11503/agent-z/commit/b11e669) | CHANGELOG v1.6 entry 擴充 cycle 2 |
| 35 | [bc7f98b](https://github.com/symbiosis11503/agent-z/commit/bc7f98b) | README.md Status v1.3-1.6 完整化 + 70+ 名詞 + 7 個分頁 |
| 36 | [188b697](https://github.com/symbiosis11503/agent-z/commit/188b697) | INDEX.md Phase 7 + 額外頁列表 |
| 37 | [0e03087](https://github.com/symbiosis11503/agent-z/commit/0e03087) | Gemini 2.0 Flash → 2.5 Flash (4 files) |
| 38 | [9289da9](https://github.com/symbiosis11503/agent-z/commit/9289da9) | compliance 速查卡 cross-link 到 cycle 2 (ch14 §8c / ch15 §5b) |
| 39 | [ae82098](https://github.com/symbiosis11503/agent-z/commit/ae82098) | chapters landing 7 章「核心」加 v1.6 標記 |
| 40 | [cdc8267](https://github.com/symbiosis11503/agent-z/commit/cdc8267) | glossary 7 新詞「章節」連結升級到具體 §5a/§5b/§8c |
| 41 | [2669f97](https://github.com/symbiosis11503/agent-z/commit/2669f97) | ch16 §4 加 ICE 進階 anti-hallucination |
| 42 | [6d70c07](https://github.com/symbiosis11503/agent-z/commit/6d70c07) | whatsnew v1.6 收尾 polish 段 |
| 43 | [aad3e30](https://github.com/symbiosis11503/agent-z/commit/aad3e30) | 首頁 規模 段 truth-sync v1.6 |
| 44 | [a55078c](https://github.com/symbiosis11503/agent-z/commit/a55078c) | about 加第 6 條差異化定位「2026 業界對齊」 |
| 45 | [8429f07](https://github.com/symbiosis11503/agent-z/commit/8429f07) | compare 14 → 16 維度 + 2 行新維度 |
| 46 | [86c2e89](https://github.com/symbiosis11503/agent-z/commit/86c2e89) | FAQ 加 2 條 v1.6 Q&A |
| 47 | [e24f6c8](https://github.com/symbiosis11503/agent-z/commit/e24f6c8) | llms.txt truth-sync v1.6 (4 條 stale) |
| 48 | [7222a69](https://github.com/symbiosis11503/agent-z/commit/7222a69) | 7 章「卡關時看這裡」footer 60+ → 70+ |
| 49 | [01dc69b](https://github.com/symbiosis11503/agent-z/commit/01dc69b) | glossary index 加 🆕 v1.6 新詞 tip 框 |

**v1.6 總計**：~33 commit 連推（cycle 1 + cycle 2 + 收尾），每 commit 都 GitHub Actions auto-deploy 到 Pages。Ralph loop max-iter 50 自然 cap @ iter 50。

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
