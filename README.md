# AgentZ — 從零到 AI Agent 構建者（繁中）

> 從完全沒寫過 code 的零基礎開始，走到能自己構建 multi-agent 系統的熟練技術人員

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-active%20development-orange)
![Language](https://img.shields.io/badge/language-繁體中文-red)

## 為什麼又一本？

中文圈的 AI Agent 學習資源有兩個空缺：

1. **沒有繁中 first 的 curriculum**。簡中圈 `datawhalechina/hello-agents` 已經很強（47K⭐），但繁中只有 `WenyuChiou/awesome-agentic-ai-zh` 是學習地圖，不是 curriculum。
2. **多數教程綁特定 vendor**：Azure / HuggingFace / 單一框架。實務上我們需要在 Claude / OpenAI / Gemini / Groq / OpenRouter 之間切換。

AgentZ 想補上這兩塊，並且把 **Claude Code 生態系**（MCP / Skills / Plugins / Marketplace）當一級題材深入講——這是其他教程多數一筆帶過、但 2025-2026 實務上最重要的工作環境。

## 你會走什麼路？

```
零基礎          → Watcher          → Operator         → Builder         → 進階分流
（連 Terminal     （理解 LLM、       （CLI agent、     （從 0 寫 agent、 （Researcher /
  都沒打開）       prompt、agent）   MCP、Skills）     framework、deploy） Builder / Maker /
                                                                       Educator）
```

四層 ladder，每層都有「milestone evidence」——做完該章節，你會有一個 GitHub repo / run ID / portfolio entry 證明你真的會了，不是看過。

## 章節目錄（v1，18 章 + capstone）

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
- Ch 16 [Researcher 路線](./chapters/ch16_researcher/)
- Ch 17 [Builder 進階](./chapters/ch17_builder_advanced/) — Agentic-RL 入門
- Ch 18 [Maker / Educator 路線](./chapters/ch18_maker_educator/)

### Capstone — 畢業作品集
依進階分流交一個完整可運行的 agent 系統。

## 怎麼學？

- **動手練習不准跳**：每章最後有 1-3 個練習，做完才能往下。
- **跟著 milestone evidence 走**：練習完成放 GitHub / 截圖 / run log，章節右上角從 ☐ → ✅。
- **不確定先讀 Ch-1**：如果你連「AI Agent 跟 ChatGPT 有什麼差別」都還不確定，從 Ch-1 開始；如果你已經會寫 Python 也用過 Claude Code，直接從 Ch 4 跳。

## 載體規劃

- **v1**（你在看的這個）：純 markdown + GitHub Pages 線上閱讀 + PDF release
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

正體中文 + 動手練習 patterns 為主。詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)（撰寫中）。

## Status

**v1 complete** (2026-05-11) — 20 章 / ~5,280 行繁中 / 60+ 動手練習 / 互動 Web App live。
**v2 規劃中** — 章節內動手練習串 Helix V3 sandbox 真跑 + portfolio leaderboard。

請查 [CHANGELOG.md](./CHANGELOG.md)。

---

維護：[Symbiosis (SBS)](https://symbiosis.tw) 團隊；ssh `learn.symbiosis.tw`
