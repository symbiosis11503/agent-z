# AgentZ — 從零到 AI Agent 構建者（繁中）

> 從完全沒寫過 code 的零基礎開始，走到能自己構建 multi-agent 系統的熟練技術人員

**👉 線上閱讀**：<https://symbiosis11503.github.io/agent-z/>
**👉 5 分鐘 Quick Win**：<https://symbiosis11503.github.io/agent-z/quickwin>
**👉 PDF 離線版**：[最新 Release](https://github.com/symbiosis11503/agent-z/releases/latest)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/v1-complete-green.svg)](CHANGELOG.md)
![Language](https://img.shields.io/badge/language-繁體中文-red)
![Chapters](https://img.shields.io/badge/chapters-20-blue)
![Starter%20code](https://img.shields.io/badge/starter--code-10%20dirs-blueviolet)

---

## 為什麼又一本？

中文圈的 AI Agent 學習資源有兩個空缺：

1. **沒有繁中 first 的 curriculum**。簡中圈 `datawhalechina/hello-agents` 已經很強（47K⭐），但繁中只有 `WenyuChiou/awesome-agentic-ai-zh` 是學習地圖，不是 curriculum。
2. **多數教程綁特定 vendor**：Azure / HuggingFace / 單一框架。實務上我們需要在 Claude / OpenAI / Gemini / Groq / OpenRouter 之間切換。

AgentZ 補上這兩塊，並且把 **Claude Code 生態系**（MCP / Skills / Plugins / Marketplace）當一級題材深入講——這是其他教程多數一筆帶過、但 2025-2026 實務上最重要的工作環境。

## 你會走什麼路？

```
零基礎          → Watcher          → Operator         → Builder         → 進階分流
（連 Terminal     （理解 LLM、       （CLI agent、     （從 0 寫 agent、 （Researcher /
  都沒打開）       prompt、agent）   MCP、Skills）     framework、deploy） Builder / Maker /
                                                                       Educator）
```

四層 ladder，每層都有「milestone evidence」——做完該章節，你會有一個 GitHub repo / run ID / portfolio entry 證明你真的會了，不是看過。

## 章節目錄（v1，20 章 + capstone）

### Part 0 — 真零基礎 onramp（完全沒寫過 code 的人從這裡開始）
- [Ch-1 完全沒寫過 code 也能讀的 AI Agent 全景](./chapters/ch-1_zero_basics/) — 30 分鐘讀完
- [Ch 0 把工具裝好](./chapters/ch00_setup/) — Terminal / Python / git / API key 從 0

### Part 1 — Watcher（理解）
- Ch 1 [LLM 是什麼](./chapters/ch01_llm_basics/) — token / context / 各家比較
- Ch 2 [Prompt 設計](./chapters/ch02_prompt/) — system / few-shot / CoT
- Ch 3 [什麼是 Agent](./chapters/ch03_what_is_agent/) — 工具呼叫 / ReAct / 為何需要

### Part 2 — Operator（操作）
- Ch 4 [CLI Agent 入門](./chapters/ch04_cli_agents/) — Claude Code / Codex / OpenCode 比較選擇
- Ch 5 [CLI Workflow](./chapters/ch05_cli_workflow/) — CLAUDE.md / slash command / 多步驟拆解
- Ch 6 [MCP](./chapters/ch06_mcp/) — 什麼是 MCP / 怎麼裝 / 接 Notion / Obsidian / GitHub
- Ch 7 [Skills / Plugins / Marketplace](./chapters/ch07_skills_plugins/)
- Ch 8 [Cost 觀測 + token 預算 + 介入](./chapters/ch08_cost_observability/)

### Part 3 — Builder（構建）
- Ch 9 [Function calling 跟 tool use](./chapters/ch09_function_calling/)
- Ch 10 [ReAct / Plan-and-Solve / Reflection](./chapters/ch10_react_paradigms/)
- Ch 11 [框架比較](./chapters/ch11_frameworks/) — LangGraph / CrewAI / Smolagents
- Ch 12 [自寫 mini agent framework](./chapters/ch12_mini_framework/)
- Ch 13 [Memory & RAG](./chapters/ch13_memory_rag/)
- Ch 14 [Multi-agent](./chapters/ch14_multi_agent/) — 協作 / handoff / 主從
- Ch 15 [Deploy + audit + replay + cost cap](./chapters/ch15_deploy_audit_replay/) — 用 Helix V3 完整 case study

### Part 4 — 進階分流
- Ch 16 [Researcher 路線](./chapters/ch16_researcher/) — paper summary / deep research / peer review
- Ch 17 [Builder 進階](./chapters/ch17_builder_advanced/) — Agentic-RL / SFT / GRPO / DeepSeek-R1 復現
- Ch 18 [Maker / Educator 路線](./chapters/ch18_maker_educator/) — 個人助理 / 教學設計

### Capstone — 畢業作品集
依進階分流交一個完整可運行的 agent 系統。[Rubric 5 條 + 範例](./chapters/ch18_maker_educator/#5-結尾capstone-是什麼)。

## 額外資源頁

- 🚀 [5 分鐘 Quick Win](https://symbiosis11503.github.io/agent-z/quickwin) — 不用裝 Python、5 min 看 agent 真的在做事
- 🔑 [LLM / API 申請指南](https://symbiosis11503.github.io/agent-z/llm-providers) — 11 家 LLM 申請流程 + curl/Python 範例 + 費用
- 📋 [速查卡 Cheatsheet (7 個分頁)](https://symbiosis11503.github.io/agent-z/cheatsheet) — A4 可印（CLI / SDK / Pricing / Patterns / MCP / Governance / **Compliance** ISO·NIST·EU AI Act·OTel）
- 🛠 [故障排除](https://symbiosis11503.github.io/agent-z/troubleshooting) — 12 大類常見錯誤 + 症狀 + 解法
- 📖 [70+ 名詞表 (5 分類)](https://symbiosis11503.github.io/agent-z/glossary) — 繁中/English + 4 欄（基礎/Agent/實務/Production/台灣 pair，含 ICE / Consensus Trap / Slopsquatting / ISO 42001 / NIST AI RMF / EU AI Act / OTel GenAI）
- ✅ [進度檢核表](https://symbiosis11503.github.io/agent-z/progress) — localStorage 記你跑到哪
- 📜 [更新紀錄 What's New](https://symbiosis11503.github.io/agent-z/whatsnew) — v1.0 → v1.8 改版重點
- 📚 [引用 AgentZ](https://symbiosis11503.github.io/agent-z/cite) — BibTeX / APA 7th / Chicago 17th / CITATION.cff / Markdown 5 格式 (researcher / 教材作者 / blog)
- 📋 [CONTRIBUTING.md](./CONTRIBUTING.md) — 5 條投稿路徑

## Starter Code（跑得起來的真實 code，10 dirs）

| 對應章 | 目錄 | 內容 |
|---|---|---|
| Ch 6 | [`starter-code/ch06_mcp/`](./starter-code/ch06_mcp/) | FastMCP server 3 tools + Claude Code 接法 |
| Ch 7 | [`starter-code/ch07_skills_plugins/`](./starter-code/ch07_skills_plugins/) | SKILL.md template + project/user-scope install |
| Ch 8 | [`starter-code/ch08_cost_observability/`](./starter-code/ch08_cost_observability/) | drop-in Anthropic SDK wrap + SQLite log + daily cap |
| Ch 9 | [`starter-code/ch09_weather_agent/`](./starter-code/ch09_weather_agent/) | function calling weather agent |
| Ch 10 | [`starter-code/ch10_paradigms/`](./starter-code/ch10_paradigms/) | ReAct / Plan-and-Solve / Reflection 三範式 |
| Ch 11 | [`starter-code/ch11_frameworks/`](./starter-code/ch11_frameworks/) | vanilla / LangGraph / CrewAI / Smolagents / Pydantic AI 5 對照 |
| Ch 12 | [`starter-code/ch12_mini_framework/`](./starter-code/ch12_mini_framework/) | mini agent framework from scratch |
| Ch 13 | [`starter-code/ch13_memory_rag/`](./starter-code/ch13_memory_rag/) | session memory + Chroma RAG |
| Ch 14 | [`starter-code/ch14_multi_agent/`](./starter-code/ch14_multi_agent/) | Pipeline / Supervisor / Blackboard 三架構 |
| Ch 15 | [`starter-code/ch15_v3_governance/`](./starter-code/ch15_v3_governance/) | audit + replay + cost cap (V3 case study) |

跑：每個 dir 內 `uv sync && uv run <file>.py`，設好 `ANTHROPIC_API_KEY` 即可。

## 怎麼學？

- **動手練習不准跳**：每章最後有 1-3 個練習，做完才能往下。
- **跟著 milestone evidence 走**：練習完成放 GitHub / 截圖 / run log，章節右上角從 ☐ → ✅。
- **不確定先讀 Ch-1**：如果你連「AI Agent 跟 ChatGPT 有什麼差別」都還不確定，從 Ch-1 開始；如果你已經會寫 Python 也用過 Claude Code，直接從 Ch 4 跳。

## 載體規劃

- **v1**（你在看的這個）：純 markdown + GitHub Pages 線上閱讀 + PDF release ✅
- **v2**：每章「動手練習」可選擇打開 `learn.symbiosis.tw` sandbox，串 Helix V3 multi-provider + audit / replay / cost / MCP primitives 真跑
- **v3**：自動 zh-CN / EN 翻譯 + 社群投稿 + portfolio leaderboard

## 跟其他教程的關係

- **datawhalechina/hello-agents**：簡中圈標竿，內容深、訓練/Agentic-RL 重。本書繁中、vendor-neutral、Claude Code 深、含真零基礎。
- **WenyuChiou/awesome-agentic-ai-zh**：繁中學習地圖；本書是 curriculum 不是 roadmap，建議搭配閱讀。
- **microsoft/ai-agents-for-beginners**：英文 + 50 語翻譯，Azure-centric；本書 vendor-neutral。
- **huggingface/agents-course**：英文，HF-centric；本書多 framework 並列。

## License

[MIT](./LICENSE) — 章節內容跟 starter code 都可以 copy 進你自己的商業專案。

## Contributing

繁體中文 + 動手練習 patterns 為主。詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

歡迎：bug / typo 修、章節 common pitfalls 補、starter code 投稿、翻譯（zh-CN / EN）、Capstone gallery 投稿。

### 本地預覽（給投稿者）

```bash
git clone https://github.com/symbiosis11503/agent-z
cd agent-z
npm install                # 拉 VitePress
npm run dev                # http://localhost:5173/agent-z/
# 邊改 markdown 邊看，hot reload
npm run build              # 產 site/.vitepress/dist（最終驗證）
```

Node 18+ 即可。沒 lint / test，但 PR 前請至少 `npm run build` 確認 build 不破。

## Status

**v1 complete** (2026-05-11) — 20 章 / ~6,200 行繁中 / 60+ 動手練習 / 10 starter code dirs / 互動 Web App live + PDF release ✅
**v1.1** (2026-05-11) — Ch 16/17/18 深度補完、starter code 全 coverage、5 分鐘 Quick Win + LLM API 指南 + glossary rewrite ✅
**v1.2** (2026-05-12) — Ralph-loop polish wave (22 iter): 速查卡 / 故障排除 / What's New / 跟其他教程比較 / 自訂 404 + 名詞表 53→62 + nav 14→7 dropdown + A4/mobile responsive CSS + 11 章「🛟 卡關時看這裡」 footer + per-page SEO ✅
**v1.3-1.5** (2026-05-12) — 三大長頁拆分（glossary 5 分類 / cheatsheet 6 分頁 / llm-providers 3 分頁）+ SEO canonical 51 頁 + JSON-LD Course + BreadcrumbList + 20 章 frontmatter + /chapters landing ✅
**v1.6** (2026-05) — Ralph-loop 第三輪雙 cycle (~17 iter): **70+ 名詞** (+ICE / Consensus Trap / Slopsquatting / ISO 42001 / NIST AI RMF / EU AI Act / OTel GenAI) + ch08 vendor 單價表 + ch11 A2A 協議 + ch15 OpenTelemetry GenAI + **速查卡 7th page · Compliance** + ch5/6/9/14/15 章節 cross-link ✅
**v1.7 cycle 1** (2026-05-13) — Ralph-loop 第四輪「讓人帶走它」(6 iter): **/cite** (BibTeX/APA/Chicago/CITATION.cff) + **CODE_OF_CONDUCT.md** + nav 💬 Discussions + Issues + about「社群場合對照表」+ **og-image 1200×630** Twitter/FB link preview + per-page meta inject + **PWA manifest** (Add to Home Screen) ✅
**v1.8** (2026-05-20) — 競品 Survey 內化 (7 iter): 5 大 Agent Platform survey 精華→教學內容。Ch 3 Agent 演化路線圖 / Ch 11 Agent Platform/OS 品類 / Ch 13 Self-Learning Loop / Ch 14 Cross-Model Review / Ch 15 4-Layer Security Hardening。7,200+ 行 / 65+ 練習 ✅
**v2 規劃中** — 章節內動手練習串 Helix V3 sandbox 真跑 + portfolio leaderboard

請查 [CHANGELOG.md](./CHANGELOG.md)。

---

維護：[Symbiosis (SBS)](https://symbiosis.tw) 團隊
線上閱讀：<https://symbiosis11503.github.io/agent-z/>（learn.symbiosis.tw DNS 規劃中）
