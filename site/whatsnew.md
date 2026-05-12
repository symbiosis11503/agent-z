---
title: What's New — AgentZ 更新紀錄
description: AgentZ 版本變動 high-signal 摘要：v1.0 initial / v1.1 章節深度補完 / v1.2 ralph-loop polish / v1.3 三大長頁拆分 / v1.4 SEO canonical / v1.5 結構化資料 / v1.6 合規 + 框架 + 標準觀測性。
---

# What's New — 更新紀錄

AgentZ 持續迭代中。這頁是 site-side 「最近一個月做了什麼」的高訊號摘要。完整時間序列見 [CHANGELOG.md](https://github.com/symbiosis11503/agent-z/blob/main/CHANGELOG.md)。

> **Watch the repo** 不定時 polish — [GitHub Watch](https://github.com/symbiosis11503/agent-z) → Releases-only 抓重大改版。

[[toc]]

---

## 2026-05-13 — v1.7 cycle 1 社群與分享化

第一波「讓人引用、加好友、分享 link」基建。重點不是補章節，是讓 AgentZ 從「自閉好內容」升級成「真的能 spread 的開源教程」。

### 引用 / 學術可用化

- 新建 **[引用 AgentZ (`/cite`)](./cite)** — BibTeX / APA 7th / Chicago 17th / CITATION.cff / Markdown 5 種引用格式都列出來，CC-BY-4.0 授權清楚標示
- 從 nav「進度 & 社群」入口進得來，researcher / 教材作者 / blog 引用一鍵 copy

### Community 正式邊界

- 新建 **[CODE_OF_CONDUCT.md](https://github.com/symbiosis11503/agent-z/blob/main/CODE_OF_CONDUCT.md)** — 改寫 Contributor Covenant 2.1，繁中口語化，包含 24h 通報窗口 + 5 級處理 + 範圍說明
- **about.md「社群」章節** 改成 6 行對照表：bug 報哪、討論去哪、PR 走哪、Capstone 投稿、學術引用、CoC 通報 — 每個場合一個入口不混
- **全站 nav 加 💬 Discussions + Issues** 兩個外部入口（之前只有 GitHub 主頁連結）

### 分享 / Link preview 化

- **[og-image.png](https://symbiosis11503.github.io/agent-z/og-image.png)** 1200×630 — Twitter / FB / LinkedIn / Slack / Discord 貼 AgentZ URL 終於有正式 link preview（之前只看到 64px logo）
- 4 chip 標：20 章 / Vendor-neutral / Claude Code 一級 / v1.6 · 2026
- **per-page meta inject** — 每頁 og:title / og:description / og:url / twitter:image 都自動帶當前頁面，不只首頁

### PWA installable

- **[manifest.json](https://symbiosis11503.github.io/agent-z/manifest.json)** — Chrome / Edge / iOS Safari 可「Add to Home Screen」把 AgentZ 變 standalone web app
- Apple meta 4 條 (mobile-web-app-capable / status-bar-style / title `AgentZ` / theme-color #5b21b6)

### 不一樣的精神

v1.6 是「**內容變強**」（合規 / 框架 / OTel）；v1.7 cycle 1 是「**讓人帶走它**」（cite / share / install）。AgentZ 從「我寫得多用心」進到「別人能多容易引用」這層。

---

## 2026-05 — v1.6 合規 + 框架校準 + 標準觀測性

把 2026 業界三大缺口補上：**合規標準**（ISO / NIST / EU AI Act）、**框架地位變動**（A2A 協議 / LangGraph production standard / CrewAI 45.9k★）、**OpenTelemetry GenAI**（替代各家自家 dashboard）。

### 名詞表加 7 個 2026 新詞

- **[名詞表 · Agent](./glossary/agent)** §5「Multi-Agent Verification / 安全」加 **ICE (Iterative Consensus Ensemble) / Consensus Trap (arXiv 2604.17139) / Slopsquatting (Stanford 2026 三大新攻面之一)**
- **[名詞表 · Production](./glossary/production)** §10「合規 / 國際標準」加 **ISO/IEC 42001:2023 / NIST AI RMF + GenAI Profile / EU AI Act 2026-08-02 / OpenTelemetry GenAI Semantic Conventions**
- 60+ → **70+ 詞** 標記同步到 [glossary index](./glossary) / [index hero](/) / [about](./about)

### 章節內容補強

- **[Ch 8 §5.1](./chapters/ch08_cost_observability/#51-2026-05-多-vendor-token-單價對照)** — 加「2026-05 多 vendor token 單價對照表」(8 model: DeepSeek V3 / Gemini Flash / Haiku 4.5 / Gemini 2.5 Pro / Sonnet 4.6 / GPT-4o / GPT-4 / Opus 4.7) + 快速估算公式 + 省錢三招 + 跨頁 cross-link
- **[Ch 11 §4a](./chapters/ch11_frameworks/#4a-2026-05-採用度快照)** — 加「2026-05 採用度快照」: LangGraph 14k / CrewAI 45.9k / AutoGen v0.4 38k / OpenAI Agents SDK 12k / Smolagents 10k / Pydantic AI 8k + **A2A 協議介紹** (Google + 150+ orgs 2026-04 launch) + 選框架判斷表
- **[Ch 15 §5a](./chapters/ch15_deploy_audit_replay/#5a-opentelemetry-genai--業界標準-observability)** — 加 OpenTelemetry GenAI: 標準 span/metric 表 + OpenLLMetry Python SDK 5 分鐘上手範例

### 速查卡新 7th page · Compliance

- 新建 **[/cheatsheet/compliance](./cheatsheet/compliance)** — ISO 42001 / NIST AI RMF / EU AI Act / OpenTelemetry GenAI 4 大標準速查 + 何時該做哪個決策樹 + 罰款 + 時程
- 從速查卡「6 個分頁」→「**7 個分頁**」全站 sync (cheatsheet index / all.md / index hero / quickwin / roadmap / about / 404 / llms.txt / sidebar)

### Glossary 新詞反向 cross-link 進章節（iter 30-32）

新加的詞光在名詞表看不夠，讀者翻章節要在原生 context 遇得到。iter 30-32 把新詞下放到對應章節：

- **[Ch 14 §8c](./chapters/ch14_multi_agent/#8c-2026-multi-agent-新興安全議題)** — 加 ICE / Consensus Trap / Slopsquatting 3 個 multi-agent 安全議題 + 影響 Ch 14 哪段 + 防禦方式
- **[Ch 15 §5b](./chapters/ch15_deploy_audit_replay/#5b-合規--iso-42001--nist-ai-rmf--eu-ai-act)** — 加合規對照：ISO 42001 / NIST RMF / EU AI Act 三大標準 → V3 四 pillar 映射 + 風險分級 + incident reporting
- **[Ch 6 §5a](./chapters/ch06_mcp/#5a-mcp-scope--server-放哪一層作用範圍不同)** — 加 MCP Scope (user/project/local) 3 層作用範圍 + 敏感 token 安全準則
- **[Ch 9 §4a](./chapters/ch09_function_calling/#4a-computer-use--anthropic-的特殊-tool-use-模式)** — 加 Computer Use Anthropic 特殊 tool-use 模式 + sandbox 安全
- **[Ch 5 §6a](./chapters/ch05_cli_workflow/#6a-headless-agent--claude-code-進-cron--ci--shell-pipe)** — 加 Headless Agent (`claude -p`) + cron / CI / shell pipe 用法 + 不問 permission 的安全提醒

### Memory 生態地景（iter 34）

boss 5/12 ping `rohitg00/agentmemory` (4.9K★, BM25+Vec+Graph RRF, 16+ agent 共用 memory) 後加：

- **[Ch 13 §6a](./chapters/ch13_memory_rag/#6a-2026-production-memory-生態--不一定要自己造輪)** — mem0 (53K★) / Letta (22K★) / agentmemory (4.9K★) / Helix Memory 四家對照表 + 怎麼選 + benchmark caveat（自家數字第三方未驗證）+ 學習路徑建議（先自拼 §3-6 理解 mechanic、production 前再決定要不要切）

### boss 推薦 11 個 GitHub repo 編寫進 AgentZ（iter 37）

boss 5/12 ping 「40 GITHUB REPOS THAT ARE ACTUALLY USEFUL」清單，篩出 11 個跟 AgentZ 主題對得上、boss 確認後寫進對應章節：

- **[Ch 0 §11](./chapters/ch00_setup/#_11-想要-chatgpt-風-gui-open-webui)** — open-webui (136K★) 自架 ChatGPT GUI + Docker run cheat
- **[Ch 1 §6 開源 fine-tuned](./chapters/ch01_llm_basics/#開源-fine-tuned-模型家族)** — NousResearch/Hermes-Function-Calling + huggingface/transformers (160K★) + stable-diffusion-webui (163K★) 平行領域標記
- **[Ch 9 §4a](./chapters/ch09_function_calling/#4a-computer-use--anthropic-的特殊-tool-use-模式)** — browser-use (93K★) 補 Computer Use 的 DOM-based 替代 + 何時 DOM / 何時 screenshot 判斷
- **[Ch 11 §5a](./chapters/ch11_frameworks/#_5a-visual--low-code-路線--不寫-code-也想拼-agent-workflow)** Visual/Low-code 新節 — n8n (187K★) / Langflow (148K★) / Lobe Chat (76K★) / Dify + 何時 visual / 何時 code 判斷準則
- **[Ch 13 §5](./chapters/ch13_memory_rag/#_5-rag-retrieval-augmented-generation)** RAG 起點 — markitdown (122K★) 17 格式 → md 一行 cheat
- **[Ch 13 §6a](./chapters/ch13_memory_rag/#6a-2026-production-memory-生態--不一定要自己造輪)** memory 表 — cocoindex (9.6K★) 加入長 horizon agent 增量 indexing 一欄
- **[Ch 14 §9](./chapters/ch14_multi_agent/#9-補充閱讀)** 補充閱讀 — TradingAgents (74K★) production-grade multi-agent 金融案例

跳過 4 個（boss 5/12 確認）: `ruflo` / `agency-agents` / `browserbase-skills`（找不到對應 repo） + `the-book-of-secret-knowledge`（偏 OSINT 不適合 AgentZ 主軸）

### Iter 21-32 commits

11. iter 21 [4f09afd](https://github.com/symbiosis11503/agent-z/commit/4f09afd) — glossary/production 加合規 4 詞
12. iter 22 [0e91588](https://github.com/symbiosis11503/agent-z/commit/0e91588) + iter 23 [1aeaaf6](https://github.com/symbiosis11503/agent-z/commit/1aeaaf6) — glossary/agent 加 multi-agent 安全 3 詞
13. iter 24 [089434b](https://github.com/symbiosis11503/agent-z/commit/089434b) + iter 25 [9171867](https://github.com/symbiosis11503/agent-z/commit/9171867) — ch08 §5.1 vendor 單價對照表 + 版本命名校準 (Sonnet 4.6 / Opus 4.7 align commercial.md)
14. iter 26 [9166a00](https://github.com/symbiosis11503/agent-z/commit/9166a00) — ch11 §4a 2026 採用快照 + A2A 協議
15. iter 27 [e6ce812](https://github.com/symbiosis11503/agent-z/commit/e6ce812) — ch15 §5a OpenTelemetry GenAI
16. iter 28 [cfa3a7b](https://github.com/symbiosis11503/agent-z/commit/cfa3a7b) — 速查卡 7th page · Compliance
17. iter 29 [2f5eda6](https://github.com/symbiosis11503/agent-z/commit/2f5eda6) — 全站「6 → 7 個分頁」sync
18. iter 27 (v1.6 cycle 2) [d2db5e5](https://github.com/symbiosis11503/agent-z/commit/d2db5e5) — 60+ → 70+ 名詞表 truth-sync (4 files)
19. iter 28 [f824b37](https://github.com/symbiosis11503/agent-z/commit/f824b37) — ch14 加 §8c multi-agent 安全 (ICE / Consensus Trap / Slopsquatting)
20. iter 29 (cycle 2) [57a9e08](https://github.com/symbiosis11503/agent-z/commit/57a9e08) — ch15 加 §5b 合規對照 (ISO 42001 / NIST RMF / EU AI Act → V3 四 pillar)
21. iter 30 [0a3c732](https://github.com/symbiosis11503/agent-z/commit/0a3c732) — ch06 加 §5a MCP Scope (user/project/local)
22. iter 31 [d3d58a1](https://github.com/symbiosis11503/agent-z/commit/d3d58a1) — ch09 加 §4a Computer Use + sandbox 安全
23. iter 32 [87d8da6](https://github.com/symbiosis11503/agent-z/commit/87d8da6) — ch05 加 §6a Headless Agent + cron/CI 安全提醒
24. iter 34 [f0f1009](https://github.com/symbiosis11503/agent-z/commit/f0f1009) — ch13 §6a 2026 production memory 生態 (mem0 / Letta / agentmemory / Helix) + 怎麼選 + benchmark caveat
25. iter 36 [3f27feb](https://github.com/symbiosis11503/agent-z/commit/3f27feb) — ch13 §6a 拿掉 SBS-K 內部代號 (A/B boundary scrub)
26. iter 37 [53a30aa](https://github.com/symbiosis11503/agent-z/commit/53a30aa) — 11 個 boss-curated repo 編寫進 AgentZ — Ch 0/1/9/11/13/14 各補對應 repo

### v1.6 收尾 polish（iter 33-41）

兩 cycle 完工後又連推 9 次收尾 polish，把零散的 truth-sync / cross-link / 版本一致性全清掉：

- **iter 33** — whatsnew cycle 2 entry
- **iter 34** — CHANGELOG v1.6 entry 加 cycle 2 部分（之前只列 cycle 1）
- **iter 35** — README.md Status 段加 v1.3 / v1.4 / v1.5 / v1.6 完整描述 + 70+ 名詞 + 7 個分頁
- **iter 36** — INDEX.md Phase 7 加 + 額外頁 list 完整化
- **iter 37** — Gemini 2.0 Flash → 2.5 Flash truth-sync (4 files: llm-providers / cheatsheet/pricing / glossary/foundation / ch01)
- **iter 38** — compliance 速查卡 cross-link 到 cycle 2 章節 (ch14 §8c / ch15 §5b)
- **iter 39** — chapters landing 7 章「核心」column 加 v1.6 新內容標記
- **iter 40** — glossary 7 新詞「章節」連結指向具體 §5b/§5a/§8c 而非 generic Ch 15 §3
- **iter 41** — ch16 §4 加 ICE 進階 anti-hallucination + Consensus Trap 注意

---

## 2026-05-12 — v1.5 結構化資料 + 章節索引 + 章節 SEO 補齊

延續 v1.4 SEO 路線，把剩下的 gap 一次清掉。

### JSON-LD 結構化資料

- **首頁加 schema.org/Course** — Google 把 AgentZ 當「Online Course / Curriculum」識別，含 inLanguage / educationalLevel / teaches / license / courseInstance 完整欄位。Knowledge Graph 友好。
- **所有 subpage 加 BreadcrumbList** — Google SERP 結果顯示 `AgentZ > glossary > foundation` 麵包屑而非裸 URL。所有 50+ subpage 自動產出，從 URL segment 動態解構。

### 20 章 chapter SEO 補齊

iter 11 加 per-page og/twitter 後發現所有 chapter README 沒 frontmatter description, 社群 share 還是顯示 fallback。
- **Ch -1 / Ch 0 / Ch 1-18 全部加 YAML frontmatter** (title + description), 每章 60-100 字描述核心內容。
- Share 任何 chapter 到 Twitter / Discord / Slack 都顯示 per-chapter 標題 + 描述。

### [章節索引](./chapters) 新 landing page

iter 16 BreadcrumbList 對 chapter 頁面產的中間段 URL `/chapters` 是 404（沒 landing）。Fix:
- 新建 [/chapters](./chapters) — 20 章索引，按前言 / Watcher / Operator / Builder / 進階分流 5 層分組，每章帶時長 + 核心關鍵字
- nav「章節」改指 /chapters landing（之前直接跳 Ch -1）
- sidebar /chapters/ 加「🏠 章節索引」入口

### 404 page truth-sync

- 加章節索引 entry
- 速查卡 / 名詞表 / LLM-providers 補「6 分頁 / 5 分類 / 3 分頁」標記
- 加底部 callout 提醒打字 URL 必含 `/agent-z/` base path（boss 5/11 23:07 撞 GitHub.io 預設 404 incident 教訓內化）

### Iter 14-18 commits

5. iter 14 [0d7a4a5](https://github.com/symbiosis11503/agent-z/commit/0d7a4a5) — JSON-LD Course schema 首頁
6. iter 15 [be48dfd](https://github.com/symbiosis11503/agent-z/commit/be48dfd) — 20 章 frontmatter title + description
7. iter 16 [e24053a](https://github.com/symbiosis11503/agent-z/commit/e24053a) — BreadcrumbList JSON-LD 所有 subpage
8. iter 17 [0302611](https://github.com/symbiosis11503/agent-z/commit/0302611) — /chapters 索引 landing
9. iter 18 [7401ce8](https://github.com/symbiosis11503/agent-z/commit/7401ce8) — 404 truth-sync + base-path hint

---

## 2026-05-12 — v1.4 SEO 大修 + 第二條哲學金句

### SEO canonical / og: / twitter: 全 51 頁修對

bug 抓出來：iter 1-4 拆完 14 個 subpage 後，發現原本所有 page（含拆前的）的 `<link rel="canonical">` 都指向 home URL — Google 會把全站當 home 的 duplicate，只 index home。social share（Twitter / Discord / Slack）也都顯示 home title / description。

**Fix (iter 10-11)**：

- 砍 `head[]` 裡寫死的 canonical + 社群 meta
- 加 `transformPageData` hook 算每 page 自己的 URL → 自動產 `canonical` / `og:url` / `og:title` / `og:description` / `twitter:title` / `twitter:description`
- 處理 cleanUrls + base + chapter symlink 重寫 3 個邊界
- 例：[/glossary/foundation](./glossary/foundation) 的 canonical = `https://symbiosis11503.github.io/agent-z/glossary/foundation`、og:title = `名詞表 — 基礎概念 · AgentZ`

51 個 page 每個都自己的 SEO identity 了。

### @kojenchieh 哲學金句並入 3 處 (boss 5/11 23:18 「素材」 ping)

[@kojenchieh on Threads](https://www.threads.com/@kojenchieh/post/DYNwkBekqVz) 講效能測試精神：「工具 10%、定義+觀測+人類判斷 90%」、金句「AI 可以幫你寫腳本，但『什麼叫好』，還是要人來定義」。跟 AgentZ「Don't build smarter LLMs—build smarter integrations」+「prompt = specification」同源 — 並入 3 處：

- [Ch -1 沙發讀](./chapters/ch-1_zero_basics/)開頭 — 入門時就建立「工具 10%、定義 90%」 framing
- [Ch 17 §Reward function 設計](./chapters/ch17_builder_advanced/#reward-function-設計-最容易踩坑的地方) — RL「AI 寫 reward function、你定義 good」直接對應
- 首頁 [## 哲學段](./) — 兩條金句並列

每處附原連結署名作者，不曲解原意。

---

## 2026-05-12 — v1.3 三大長頁拆分（boss directive「分頁的方式，不要擠在一頁」）

長頁面三個 (cheatsheet 465 行 / glossary 470 行 / llm-providers 447 行) 各自拆成獨立焦點分頁 + 一個 VitePress include 合成的「全本一頁」（給 Ctrl-F 搜全本或 A4 一次印的人）。

### 拆分結構

| 原單頁 | 拆後 | landing 保留 |
|---|---|---|
| `/cheatsheet` 465 行 | `cli` / `sdk` / `pricing` / `patterns` / `mcp` / `governance` 6 焦點分頁 + `/cheatsheet/all` 合成印刷版 | 6 category card + 15-row Quick lookup table + 卡關速查 |
| `/glossary` 470 行 | `foundation` / `agent` / `practice` / `production` / `taiwan-misc` 5 分類分頁 + `/glossary/all` 合成搜尋版 | 5 category card + 4-field 結構說明 + 外部詞典清單 |
| `/llm-providers` 447 行 | `commercial` / `opensource-aggregator` / `local-sovereign` 3 分類分頁 + `/llm-providers/all` 合成版 | 11-LLM 比較表 + 8-row 怎麼選矩陣 + 7 條安全守則 |

### Sidebar 跟 nav 更新

- 工具箱 dropdown 加 9 sub-link（速查卡 6 + 名詞表 5 + LLM 3，不展平太密用「— 子頁名」前綴）
- 路徑 prefix sidebar：`/cheatsheet/` / `/glossary/` / `/llm-providers/` 各自顯示分頁列表 + 列印 / Ctrl-F 入口
- 14 個 chapter cross-link 自動 anchor 遷移（Ch 7/10/13/14 footer 改點向 `glossary/taiwan-misc#_11-常被混淆的-pair-對比`）

### 為什麼這樣拆

- A4 列印需求保留：每個分頁可單獨 Cmd-P A4 印（focus 內容）；要印全本翻 `all` 頁
- 內容同步零維護：`all.md` 用 VitePress `<!--@include: ./X.md-->` 自動 compose，分頁改、全本同步
- discovery：landing 改 card + lookup table，比 465 行單頁更快找到「我要的那節」
- mobile 友好：分頁短，sidebar 結構清楚不溢出

### Iter 1-4 commits

1. iter 1 [55c508b](https://github.com/symbiosis11503/agent-z/commit/55c508b) — cheatsheet 6-split
2. iter 2 [f467df2](https://github.com/symbiosis11503/agent-z/commit/f467df2) — cheatsheet `all.md`
3. iter 3 [8e6fb91](https://github.com/symbiosis11503/agent-z/commit/8e6fb91) — glossary 5-split + `all.md`
4. iter 4 [8cc77ce](https://github.com/symbiosis11503/agent-z/commit/8cc77ce) — llm-providers 3-split + `all.md`

---

## 2026-05-12 — v1.2 Ralph polish wave ✅ sealed @ iter 50

連續 ralph-loop session (iter 28-49 + iter 50 closeout) 把 v1.1 散落的 gap 收尾。22 次 iteration，每次 commit push origin/main，build clean。Loop 達 max-iterations 50 自然 cap。

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
- `public/llms.txt` 補 cheatsheet + troubleshooting + whatsnew + compare URL，AI agent 抓站更精準

### 章節內 cross-link

- 11/20 章補「🛟 卡關時看這裡」 footer：Ch 4/5/6/7/8/9/10/12/13/14/15 各自連 troubleshooting + cheatsheet 章節 anchor + glossary
- 中途抓到 2 個 self-introduced regression: `site/X.md` 相對路徑 / numeric-leading anchor 缺 `_` 前綴, 都修完

### 新增頁

- 📋 [速查卡](./cheatsheet) — Claude Code CLI / Anthropic SDK / pricing / ReAct / cost cap / MCP / Computer Use / Subagent / V3 governance / 章節 cost 估算
- 🛠 [故障排除](./troubleshooting) — 12 大類常見錯誤
- 📜 [What's New](./whatsnew) — 你正在看的這頁
- 🔍 [跟其他教程比較](./compare) — AgentZ vs hello-agents / MS / HF / OpenAI Cookbook 14 維度誠實對照
- 🤖 [404](./404) — friendly redirect 9 個主要入口

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
