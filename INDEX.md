# AgentZ — 從零到 AI Agent 構建者

老闆 directive 2026-05-11: 「專案：ai agent學習系統」+ 路線 C + AgentZ / learn.symbiosis.tw / monorepo / MIT / 隨時 public / 做 PDF / Web App + CSS + 互動式 / 做到成品先不用問

## v1.x 狀態：持續迭代擴充 (2026-05 v1.6 cycle)

**Live**: https://symbiosis11503.github.io/agent-z/
**Repo**: https://github.com/symbiosis11503/agent-z
**License**: MIT
**PDF**: [GitHub Releases](https://github.com/symbiosis11503/agent-z/releases/latest)

## Phases
- ✅ Phase 0 Survey (`survey/phase0_survey_20260511.md`)
- ✅ Phase 1 UltraThink (`design/phase1_ultrathink_20260511.md`)
- ✅ Phase 2 設計（boss 拍板 7 項 + 載體升級指令）
- ✅ Phase 3 v1 內容生產：20 章 / 5280 行 / 60+ 動手練習
- ✅ Phase 4 v1 載體：VitePress 互動站 + GitHub Pages auto-deploy
- ✅ Phase 5 v1.1 迭代：章節深度補完 + 新頁 + 治理 UX + starter-code 全 coverage
- ✅ Phase 6 v1.2-1.5 ralph-loop polish: 速查卡 / 故障排除 / 三大長頁拆分 / SEO canonical / JSON-LD / 章節索引
- ✅ Phase 7 v1.6 ralph-loop 雙 cycle (2026-05): 70+ 詞名詞表 + 合規對照 (ISO/NIST/EU) + 框架校準 (A2A 協議) + OTel GenAI + 速查卡 7 個分頁

## Truth boundary
- AgentZ = 獨立專案，與 V3 / SBS / ERP / Helix 分開
- V3 = AgentZ Ch 15 case study + v2 sandbox 後端
- 目標受眾: 完全新手 → 熟練技術人員（4 層 ladder）
- 載體: VitePress + GitHub Pages（v1 live）→ V3 sandbox 串接（v2）→ 多語 + 社群（v3）

## 20 章完成（v1.1 行數 snapshot）
- [x] Ch-1 完全沒寫過 code 也能讀的 AI Agent 全景（213 行 / iter 5 ↑49）
- [x] Ch 0 把工具裝好（322 行）
- [x] Ch 1 LLM 是什麼（285 行）— Watcher 開
- [x] Ch 2 Prompt 設計（265 行）
- [x] Ch 3 什麼是 Agent（326 行）— Watcher 收
- [x] Ch 4 CLI Agent 入門（195 行）— Operator 開
- [x] Ch 5 CLI Workflow（293 行）
- [x] Ch 6 MCP（310 行）
- [x] Ch 7 Skills / Plugins / Marketplace（304 行）
- [x] Ch 8 Cost 觀測 / 介入（257 行）— Operator 收
- [x] Ch 9 Function calling / Tool use（337 行）— Builder 開
- [x] Ch 10 ReAct / Plan-and-Solve / Reflection（275 行）
- [x] Ch 11 框架比較（265 行）
- [x] Ch 12 自寫 mini framework（344 行）
- [x] Ch 13 Memory & RAG（256 行）
- [x] Ch 14 Multi-agent（224 行）
- [x] Ch 15 V3 case study（360 行）— Builder 收
- [x] Ch 16 Researcher 路線（358 行 / iter 2 ↑263）— 進階開
- [x] Ch 17 Builder 進階 / Agentic-RL（374 行 / iter 3 ↑280）
- [x] Ch 18 Maker / Educator 路線（332 行 / iter 4 ↑109）— 進階收

**6,200+ 行繁中 / 60+ 動手練習**

## Starter code 10 dirs (v1.1)
- [x] `ch06_mcp/` — FastMCP server 3 tools + Claude Code 接法（iter 12）
- [x] `ch07_skills_plugins/` — SKILL.md template + install 教學（iter 14）
- [x] `ch08_cost_observability/` — drop-in Anthropic SDK wrap + SQLite log + cap（iter 13）
- [x] `ch09_weather_agent/` — function calling weather agent
- [x] `ch10_paradigms/` — ReAct / Plan-and-Solve / Reflection
- [x] `ch11_frameworks/` — vanilla/LangGraph/CrewAI/Smolagents/Pydantic AI 5 對照（iter 10）
- [x] `ch12_mini_framework/` — mini agent framework from scratch
- [x] `ch13_memory_rag/` — session memory + Chroma RAG
- [x] `ch14_multi_agent/` — Pipeline/Supervisor/Blackboard 3 架構（iter 6）
- [x] `ch15_v3_governance/` — audit + replay + cost cap V3 case

## 額外頁
- [x] `site/quickwin.md` — 5 分鐘 Quick Win 不裝 Python（iter 8）
- [x] `site/llm-providers.md` — 11 家 LLM 申請 + 範例 + 費用 → 拆 3 分頁 (商業 / 開源聚合 / 本地主權)
- [x] `site/glossary.md` — 70+ 名詞 4 欄完整 → 拆 5 分類 (基礎 / Agent / 實務 / Production / 台灣 pair)
- [x] `site/cheatsheet.md` — 7 個分頁 (CLI / SDK / Pricing / Patterns / MCP / Governance / Compliance)
- [x] `site/troubleshooting.md` — 12 大類故障排除
- [x] `site/whatsnew.md` — v1.0~v1.6 改版重點
- [x] `site/chapters.md` — 20 章索引 landing
- [x] `CONTRIBUTING.md` — 社群投稿閘門（iter 7）

## NOT_YET_DONE
- learn.symbiosis.tw custom domain DNS（CNAME committed 等 Cloudflare）
- v2 sandbox 串 Helix V3 真實 audit / replay / cost
- 自動翻譯（zh-CN / EN co-op-translator）
- 社群投稿機制 + portfolio leaderboard live
- 各章 inline `<LLMTryout />` 元件 100% coverage（目前 5/7/10/11/12/16/18 已有）
- Capstone gallery (Ch 18 投稿)
- Quiz / self-check 每章末
