---
title: 速查卡 — V3 治理 + 模型路由 + Anti-hallucination
description: V3 Production agent 4 道閘門 (cost cap / tool sandbox / audit / replay) + 11 種任務的模型路由建議 + Anti-hallucination 5 條 (Researcher 用)。
---

# 速查卡 · Governance

[← 回速查卡總覽](../cheatsheet)

## V3 Governance pattern (Production agent)

每次 LLM call → 必走 4 道閘門：

```
1. Cost cap check    (pre-flight, fail-closed)
2. Tool sandbox      (allowed list, deny-by-default)
3. Audit log         (SQLite: ts/run_id/event/payload/cost)
4. Replay record     (input + output + model + temperature)
```

[完整 V3 case →](../chapters/ch15_deploy_audit_replay/)

---

## 模型路由建議

| 任務類型 | 推薦 model |
|---|---|
| Routing / 分類 | Haiku 4.5 / Gemini Flash |
| 摘要 / 整理 | Haiku 4.5 / GPT-4o-mini |
| Coding 修 bug | Sonnet 4.6 / DeepSeek V3 |
| Coding 大重構 | Opus 4.6 |
| 數學 / 推理 | DeepSeek R1 / Opus 4.6 / o1 |
| Embedding | text-embedding-3-small (OpenAI) / cohere multilingual |
| Function calling | Haiku 4.5 (cost) / Sonnet 4.6 (穩) |
| Multi-agent supervisor | Sonnet 4.6 |
| Multi-agent worker | Haiku 4.5 |
| Reviewer / Critic | Sonnet 4.6 |
| Long context (>200K) | Sonnet 4.6 (1M) / Gemini 1.5 Pro (2M) |

---

## Anti-hallucination 5 條 (Researcher 用)

1. 每 citation 必經 DOI / arxiv ID verify
2. 區分 [直接引用] vs [基於 X 推論] vs [推測]
3. Reflection critique 必含 fact-check
4. 多 source 對比 (≥ 2 source 才寫進報告)
5. uncertainty 標記 (不確定日期就只標年份)

[完整 Ch 16 →](../chapters/ch16_researcher/)

---

**下一頁** → [CLI / Git](./cli) · [SDK](./sdk) · [Pricing](./pricing) · [Patterns](./patterns) · [MCP / Skills](./mcp)
