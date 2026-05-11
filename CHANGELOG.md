# Changelog

All notable changes to AgentZ.

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

- 各章 inline `<LLMTryout />` 嵌入（v1 元件就緒，但沒進每章 body）
- learn.symbiosis.tw custom domain DNS（需 Cloudflare CNAME）
- v2 sandbox 串 Helix V3 真實 audit / replay / cost
- 自動 zh-CN / EN 翻譯（co-op-translator）
- 社群投稿 + portfolio leaderboard
