---
title: 速查卡 — Pricing + 章節練習 cost 估算
description: 11 家主流 LLM pricing 2026-05 snapshot + AgentZ 章節練習推薦 model + 預估 cost (全本 < $10 USD)。
---

# 速查卡 · Pricing

[← 回速查卡總覽](../cheatsheet)

## Pricing (2026-05 snapshot, USD / 1M token)

| Model | Input | Output |
|---|---|---|
| Haiku 4.5 | $1 | $5 |
| Sonnet 4.6 | $3 | $15 |
| Opus 4.7 | $15 | $75 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4o | $2.5 | $10 |
| Gemini 2.5 Flash | $0.30 | $2.50 |
| Gemini 2.5 Pro | $1.25-2.50 | $10-15 |
| Groq Llama 3.3 70B | $0.59 | $0.79 |
| DeepSeek V3 | $0.27 | $1.10 |
| DeepSeek R1 | $0.55 | $2.19 |
| Mistral Large | $2 | $6 |

**Cache hit**：input × 10% (Anthropic / OpenAI 都有)。
**Cache write**：input × 1.25x（首次寫的 overhead）。

[完整 LLM 申請指南 →](../llm-providers)

---

## 章節練習推薦 model + 預估 cost

跑 AgentZ 章節練習時最划算的 model 配置（用 Haiku 走完幾乎不到 $5）：

| 章 | 練習類型 | 推薦 model | 預估 cost / 跑 |
|---|---|---|---|
| Ch 1-3 | 概念 prompt 試 | Haiku 4.5 / Gemini Flash | < $0.01 |
| Ch 4-5 | Claude Code real task | Sonnet 4.6 (Claude Code default) | $0.05-0.15 |
| Ch 6 | MCP server hello world | Haiku 4.5 | < $0.01 |
| Ch 7 | Skill 觸發測試 | Sonnet 4.6 | $0.02-0.05 |
| Ch 8 | cost cap 測試 | Haiku 4.5（故意設低 cap）| < $0.05 |
| Ch 9 | function call loop | Haiku 4.5 | < $0.02 |
| Ch 10 | ReAct + Reflection | Sonnet 4.6（Reflection 需穩定）| $0.05-0.20 |
| Ch 11 | framework 4 對照 | Haiku 4.5 | $0.05-0.10 |
| Ch 12 | mini framework 自寫 | Sonnet 4.6 | $0.10-0.30 |
| Ch 13 | session memory + RAG | Haiku 4.5 + embedding | $0.05-0.15 |
| Ch 14 | multi-agent 3 架構 | Sonnet (supervisor) + Haiku (worker) | $0.10-0.40 |
| Ch 15 | V3 governance 完整 case | 自選（建 cost cap 練習）| $0.30-1.00 |
| Ch 16 | research agent + DOI 驗證 | Sonnet 4.6（防幻覺）| $0.20-0.50 |
| Ch 17 | SFT / GRPO 訓練 | GPU local（非 API）| GPU 電費 |
| Ch 18 | menubar / 個人助理 | Haiku 4.5 | $0.05-0.20 / 天 |

**全本走完總估**：< $10 USD（Haiku 為主、Sonnet 必要時切）；省更多用 Groq Llama 3.3 70B / Gemini Flash 免費 tier。

---

**下一頁** → [Patterns](./patterns) · [MCP / Skills](./mcp) · [Governance](./governance) · [CLI / Git](./cli) · [SDK](./sdk)
