# 關於 AgentZ

## 為什麼存在

中文圈的 AI Agent 學習資源有兩個空缺：

1. **沒有繁中 first 的 curriculum**。簡中圈 [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)（47K⭐ 16 章）已經很強，但繁中只有 [`WenyuChiou/awesome-agentic-ai-zh`](https://github.com/WenyuChiou/awesome-agentic-ai-zh)（818⭐）是學習地圖，**不是 curriculum**。
2. **多數教程綁特定 vendor**：Microsoft for Beginners = Azure / HuggingFace Course = HF 生態 / Hello-Agents = 自建 HelloAgents 框架。實務上你需要在 Claude / OpenAI / Gemini / Groq 之間切換。

AgentZ 補上這兩塊，並且把 **Claude Code 生態系**（MCP / Skills / Plugins / Marketplace）當一級題材深入講——這是其他教程多數一筆帶過、但 2025-2026 年最重要的工作環境。

## 5 個差異化定位

1. **繁中 first-class curriculum**（不是 roadmap、不是翻譯）
2. **Vendor-neutral**（Claude / OpenAI / Gemini / Groq / OpenRouter / DeepSeek 一視同仁，每章範例多家並列）
3. **Claude Code 生態系**（MCP / Skills / Plugins 各章獨立、Progressive Disclosure 設計 pattern）
4. **真零基礎 onramp**（Ch-1 沙發讀完不打開工具，Ch 0 從怎麼開 Terminal 教起）
5. **動手 platform**（v2 後串 Helix V3 sandbox 真跑 + 真實 audit / replay / cost 觀測，本書 Ch 15 是完整 V3 case study）

## 課程結構

- **前言（Ch-1, 0）** — 真零基礎 onramp
- **Part 1 Watcher（Ch 1-3）** — 理解：LLM / Prompt / Agent
- **Part 2 Operator（Ch 4-8）** — 操作：CLI agent / CLAUDE.md / MCP / Skills / Cost
- **Part 3 Builder（Ch 9-15）** — 構建：tool use / 範式 / 框架 / memory / multi-agent / **deploy 用 V3 case study**
- **Part 4 進階（Ch 16-18）** — Researcher / Builder 進階 / Maker / Educator 分流
- **Capstone** — GitHub portfolio 作品集（[Gallery](./capstone)）

## v1.x 規模

- 20 章 / 6,700+ 行繁中
- 60+ 動手練習
- 10 個 starter-code dirs（Ch 6/7/8/9/10/11/12/13/14/15）— 全部可跑
- 18/20 章「常見地雷」結構化 section
- 5 個額外資源頁：[Quick Win](./quickwin) / [Roadmap](./roadmap) / [LLM / API (3 分頁)](./llm-providers) / [FAQ](./faq) / [Capstone Gallery](./capstone)
- 完整 [Progress 追蹤](./progress)、[60+ 名詞表 (5 分類)](./glossary)、[速查卡 (6 個分頁)](./cheatsheet) — 全部 A4 可印
- VitePress sitemap + editLink + SEO meta + `llms.txt`（AI agent 抓站友好）

## 關於 Symbiosis (SBS)

Symbiosis (SBS) 是台灣的 AI Agent 系統研發團隊。我們同時維護：

- **Helix Framework** — 開源 agent runtime（npm `helix-agent-framework`）
- **Helix V3** — Helix 的旗艦 agentic platform（含 multi-provider catalog / MCP server / audit / replay / cost cap）
- **OpenClaw** — 個人助理 agent
- **AgentZ**（本站）— 從零到 AI Agent 構建者學習系統

## 下載

- 🌐 線上互動版（本網站）— 含 4-provider 即時試 API、進度檢核
- 📄 PDF 離線版 — [GitHub Releases](https://github.com/symbiosis11503/agent-z/releases/latest) 抓最新 `AgentZ_v*.pdf`
- 📦 完整 source — `git clone https://github.com/symbiosis11503/agent-z`

## License

[MIT](https://github.com/symbiosis11503/agent-z/blob/main/LICENSE) — 章節內容跟 starter code 都可以 copy 進你自己的商業專案。

## 貢獻

詳見 [CONTRIBUTING.md](https://github.com/symbiosis11503/agent-z/blob/main/CONTRIBUTING.md)。我們特別歡迎：

- 繁中 / 简中 / 英文翻譯
- 章節內動手練習的範例 code（Python / TS / Go 都收）
- 新案例 / 新 MCP server / 新 Skill
- 你走完這本書做的 portfolio 作品

## 聯絡

- GitHub Issues: https://github.com/symbiosis11503/agent-z/issues
- 維護者：CC（Symbiosis SBS Acting Boss）+ 社群貢獻者
