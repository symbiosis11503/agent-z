---
title: 章節索引 — 20 章 4 個學習層
description: AgentZ 20 章索引 — Ch-1 沙發讀全景 + Ch 0 setup + Watcher (Ch 1-3) + Operator (Ch 4-8) + Builder (Ch 9-15) + 進階分流 (Ch 16-18)。每章 60-120 min。
---

# 章節索引 — 20 章

AgentZ 全本 20 章，4 個學習層。每章獨立、有 milestone evidence、可前後跳。完整課程設計見 [課程地圖](./roadmap)。

> 沒走過、不知從哪開始？翻 [5 分鐘 Quick Win](./quickwin) 試一支 agent，再決定從哪章入。

[[toc]]

---

## 前言（真零基礎 onramp）

| 章 | 標題 | 時長 | 核心 |
|---|---|---|---|
| [**Ch -1**](./chapters/ch-1_zero_basics/) | 完全沒寫過 code 也能讀的 AI Agent 全景 | 30 min | 沙發讀完全景，沒 code 沒 API |
| [**Ch 0**](./chapters/ch00_setup/) | 把工具裝好 | 60-90 min | Terminal / Python / git / API key setup |

---

## Part 1 — Watcher（理解，看得懂別人寫的 agent）

| 章 | 標題 | 時長 | 核心 |
|---|---|---|---|
| [**Ch 1**](./chapters/ch01_llm_basics/) | LLM 是什麼 | 60 min | Token / Context / Role / Temperature / Embedding |
| [**Ch 2**](./chapters/ch02_prompt/) | Prompt 設計 | 75 min | System Prompt / Few-shot / CoT / 結構化輸出 |
| [**Ch 3**](./chapters/ch03_what_is_agent/) | 什麼是 Agent | 60 min | Tool use / ReAct / Agent vs LLM vs ChatGPT |

---

## Part 2 — Operator（操作，會用 CLI agent / MCP / Skills）

| 章 | 標題 | 時長 | 核心 |
|---|---|---|---|
| [**Ch 4**](./chapters/ch04_cli_agents/) | CLI Agent 入門 | 75 min | Claude Code / Codex CLI / OpenCode 三家對照 |
| [**Ch 5**](./chapters/ch05_cli_workflow/) | CLI Workflow | 90 min | CLAUDE.md / Slash command / Hook / Headless Agent |
| [**Ch 6**](./chapters/ch06_mcp/) | MCP (Model Context Protocol) | 90 min | FastMCP + Tools / Resources / Prompts / MCP Scope |
| [**Ch 7**](./chapters/ch07_skills_plugins/) | Skills / Plugins / Marketplace | 75 min | Skill vs MCP / Progressive Disclosure |
| [**Ch 8**](./chapters/ch08_cost_observability/) | Cost 觀測 / 介入 | 60 min | Token 預算 / cost cap fail-closed / 2026-05 多 vendor 單價 |

---

## Part 3 — Builder（構建，從零寫 agent + framework + deploy）

| 章 | 標題 | 時長 | 核心 |
|---|---|---|---|
| [**Ch 9**](./chapters/ch09_function_calling/) | Function Calling / Tool Use 第一原理 | 90 min | tools schema / stop_reason 6 種 / parallel tool use / Computer Use |
| [**Ch 10**](./chapters/ch10_react_paradigms/) | ReAct / Plan-and-Solve / Reflection | 90 min | 三大 agent 範式 + code |
| [**Ch 11**](./chapters/ch11_frameworks/) | Agent 框架比較 | 75 min | vanilla / LangGraph / CrewAI / Smolagents / Pydantic AI / **A2A 協議** |
| [**Ch 12**](./chapters/ch12_mini_framework/) | 從零造輪 Mini Agent Framework | 120 min | 200 行 Python 自己寫 harness |
| [**Ch 13**](./chapters/ch13_memory_rag/) | Memory & RAG | 90 min | Session / 長期 / RAG / Chroma / pgvector |
| [**Ch 14**](./chapters/ch14_multi_agent/) | Multi-Agent 系統 | 75 min | Subagent / Pipeline / Supervisor / Handoff / 2026 安全 (ICE / Consensus Trap / Slopsquatting) |
| [**Ch 15**](./chapters/ch15_deploy_audit_replay/) | Deploy + Audit + Replay + Cost Cap | 120 min | V3 case study — 4 道閘門 / **OTel GenAI** / 合規 (ISO 42001 / NIST RMF / EU AI Act) |

---

## Part 4 — 進階分流（選一條深入）

| 章 | 標題 | 時長 | 核心 |
|---|---|---|---|
| [**Ch 16**](./chapters/ch16_researcher/) | Researcher 路線 | 90 min | paper bot / deep research / anti-hallucination |
| [**Ch 17**](./chapters/ch17_builder_advanced/) | Builder 進階 (Agentic-RL) | 120 min | SFT / GRPO / DeepSeek-R1 復現 / reward 設計 |
| [**Ch 18**](./chapters/ch18_maker_educator/) | Maker / Educator 路線 | 75 min | 個人助理 + workshop syllabus + Capstone Rubric |

---

## 4 層 ladder

```
零基礎 → Watcher → Operator → Builder → 進階分流
（Ch -1, Ch 0）  （Ch 1-3）  （Ch 4-8） （Ch 9-15）（Ch 16-18）
```

每層做完有 milestone evidence — GitHub repo / run ID / portfolio entry 證明你真會了。

[完整課程地圖 →](./roadmap)（含難度 / 時間 / 4 種學習計畫對照）

---

[首頁](/) · [Quick Win](./quickwin) · [Roadmap](./roadmap) · [GitHub](https://github.com/symbiosis11503/agent-z)
