---
title: 名詞表 Glossary — 65+ 詞 5 個分類
description: AgentZ 名詞表 65+ 詞分 5 個分類頁面（基礎 / Agent 機制 / 實務 / Production / 台灣&pair），每詞 4 欄完整解釋（專業介紹 / 白話 / 範例 / 章節）。涵蓋 ISO 42001 / NIST AI RMF / EU AI Act / OpenTelemetry GenAI 等 2026 合規標準。
---

# 名詞表 Glossary

AgentZ 用詞 + 業界術語的繁中對照。**65+ 詞分 5 個焦點頁面**，每詞 4 欄：專業介紹、白話解釋、應用範例、本書章節。

> 找不到的詞？[GitHub Issue](https://github.com/symbiosis11503/agent-z/issues) 告訴我們補進來。
> 想要 Ctrl-F 一次搜全本？翻 **[全本一頁](./glossary/all)**（自動合成，內容跟 5 分頁同步）。

[[toc]]

---

## 名詞 5 分類

| 分類 | 範圍 | 主要詞 |
|---|---|---|
| 🧠 [**基礎**](./glossary/foundation) | LLM 跟 Prompt 兩大基礎 | LLM / Token / Context Window / Role / Temperature / Embedding / Fine-tuning / Hallucination / Prompt / System Prompt / Few-shot / CoT / Structured Output / Compaction / **Prompt Cache** |
| 🤖 [**Agent 機制 + CLI / Claude Code**](./glossary/agent) | Agent 機制本身 + Claude Code 生態系 | Agent / Tool Use / ReAct / Plan-and-Solve / Reflection / Runaway / **stop_reason** / **Computer Use** / **Subagent** / **Deep Research** / **Headless Agent** / CLI Agent / MCP / Skill / Progressive Disclosure / Slash Command / Hook / **Plugin** / **Agent SDK** / **MCP Scope** |
| 🛠 [**實務**](./glossary/practice) | Vibe Coding / Memory / Multi-agent | Vibe Coding / AI Pair / Code-editing Agent / SDD / TDD / AFK / Delegation / Session Memory / Long-term / RAG / Contextual Retrieval / Multi-agent / Pipeline / Supervisor / Handoff |
| 🛡 [**Production**](./glossary/production) | 治理 + Agentic-RL 訓練 + 合規標準 | Budget Cap / Intervention / Audit / Replay / Guardrails / SFT / GRPO / Agentic-RL / **ISO 42001** / **NIST AI RMF** / **EU AI Act** / **OpenTelemetry GenAI** |
| 🇹🇼 [**台灣 AI / 常被混淆的 pair**](./glossary/taiwan-misc) | TAIDE / Local Inference + 7 對 pair + 外部詞典 | TAIDE / Sovereign AI / Local Inference / **7 對 pair 對比** / ai-dict / Anthropic Glossary |

---

## Quick lookup — 想找的詞在哪頁？

| 找這個詞 | 翻這頁 |
|---|---|
| LLM / Token / Context Window / Temperature / Embedding | [基礎](./glossary/foundation) |
| Prompt / System Prompt / Few-shot / CoT / Compaction / **Prompt Cache** | [基礎](./glossary/foundation) |
| Agent / Tool Use / ReAct / Plan-and-Solve / Reflection / **stop_reason** | [Agent / CLI](./glossary/agent) |
| **Computer Use** / **Subagent** / Deep Research / Headless Agent | [Agent / CLI](./glossary/agent) |
| CLI Agent / MCP / Skill / Hook / **Plugin** / **Agent SDK** / **MCP Scope** | [Agent / CLI](./glossary/agent) |
| Slash Command / Progressive Disclosure | [Agent / CLI](./glossary/agent) |
| Vibe Coding / AI Pair / SDD / TDD / AFK / Delegation | [實務](./glossary/practice) |
| Session Memory / Long-term Memory / RAG / Contextual Retrieval | [實務](./glossary/practice) |
| Multi-agent / Pipeline / Supervisor / Handoff | [實務](./glossary/practice) |
| Budget Cap / Intervention / Audit / Replay / Guardrails | [Production](./glossary/production) |
| SFT / GRPO / Agentic-RL / DPO | [Production](./glossary/production) |
| **ISO 42001 / NIST AI RMF / EU AI Act / OpenTelemetry GenAI** | [Production](./glossary/production) |
| TAIDE / Sovereign AI / Local Inference | [台灣 AI / pair](./glossary/taiwan-misc) |
| MCP vs Skill / ReAct vs Plan-and-Solve / Fine-tune vs RAG / Subagent vs Multi-agent | [台灣 AI / pair](./glossary/taiwan-misc) |
| ai-dict / Anthropic Glossary（外部詞典） | [台灣 AI / pair](./glossary/taiwan-misc) |

找不到？翻 **[全本一頁](./glossary/all)** 直接 Ctrl-F 搜。

---

## 4-field 結構（每詞）

- **專業介紹**（技術細節 + 引用 paper / spec）
- **白話解釋**（外行 / 文組也懂）
- **應用範例**（具體場景 + 真實工具名）
- **本書章節**（深入哪章）

---

## 為什麼這頁長這樣？

- **跨章一致**——詞在哪一章 first introduced、其他章節用同樣詞
- **持續長**——你發現該收的詞[發 Issue](https://github.com/symbiosis11503/agent-z/issues) 給我們
- **拆 5 分類**——v1.2 起拆，每頁 < 130 行不再「擠在一頁」

---

## 外部權威詞典（不重複造輪）

- 🔗 **[ai-dict.gh.miniasp.com](https://ai-dict.gh.miniasp.com/)** — Matt Pocock AI Coding Dictionary 繁中（保哥技術社群翻譯）。7 sections：Models / Sessions+Context / Tools+Environments / Failure Modes / Handoffs / Memory+Guidance / Work Modes。本書每章末「補充閱讀」會對應到 ai-dict 對應 section。
- 🔗 **[WenyuChiou/awesome-agentic-ai-zh resources/glossary.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/glossary.md)** — 30+ 詞，每個 30-80 字解釋。
- 🔗 **[Anthropic Glossary](https://docs.anthropic.com/en/docs/about-claude/glossary)** — 官方英文 glossary，跟本書名詞 1-1 對齊。

---

> 「Don't build smarter LLMs—build smarter integrations.」  
> —AgentZ 默認哲學
