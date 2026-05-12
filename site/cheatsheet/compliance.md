---
title: 速查卡 — 合規 + 國際標準 (ISO / NIST / EU / OTel)
description: ISO 42001 AIMS / NIST AI RMF + GenAI Profile / EU AI Act 2026-08-02 / OpenTelemetry GenAI 四大標準速查 + 何時該做哪個 + 罰款 + 時程。
---

# 速查卡 · 合規 + 國際標準

[← 回速查卡總覽](../cheatsheet)

agent 上 production 前必確認的 4 個合規標準。**不是法律建議**——細節找律師確認。

---

## 4 大標準 1 分鐘版

| 標準 | 出品 | 性質 | 強制？ |
|---|---|---|---|
| **ISO/IEC 42001** | ISO + IEC | AI Management System 認證 | voluntary，但 2026 EU RFP 40% 詢問 |
| **NIST AI RMF + GenAI Profile** | NIST (美) | Risk Management 4 function 框架 | voluntary，美國公部門 procurement 必查 |
| **EU AI Act** | 歐盟 | **法律**，high-risk system enforcement | **強制 2026-08-02 起**（trilogue 可能延至 2027-12） |
| **OpenTelemetry GenAI** | CNCF | observability span / metric 命名規約 | technical convention，不是合規 |

---

## ISO/IEC 42001:2023 — AI Management System

- **是什麼**：類似 ISO 9001 (品管) 之於 AI——「我有負責任做 AI 的管理流程」的認證。
- **時程**：6-12 個月全程。Stage 1 audit (scope / inventory / policy / risk 文件) → Stage 2 audit (運作測試 + sample use case) → 年度 surveillance。
- **誰拿了**：AWS / Microsoft Azure 已取得；Anthropic / OpenAI 走 SOC 2 + 自家 RSP 為主。
- **何時申請**：賣 enterprise（特別是 EU / 金融 / 政府）→ 2026 後 RFP 會問。

---

## NIST AI RMF + GenAI Profile

- **是什麼**：美國 NIST 2023 發布的 4-function 流程框架。
- **4 functions**：**GOVERN / MAP / MEASURE / MANAGE**。
- **GenAI Profile** (NIST-AI-600-1, 2024-07)：補 200+ actions 對 LLM；涵蓋 12 risks (CBRN info / Confabulation / Data privacy / InfoSec / IP / Toxicity-bias / Value chain 等)。
- **何時用**：美國公部門 vendor、銀行 OCC 監管、保險。
- **正在發展**：CSA (Cloud Security Alliance) 2026 在發展 **Agentic Profile v1**，把 agent 場景 risk 對映到 4 function。

---

## EU AI Act — 2026-08-02 強制

| 風險等級 | 範例 | 義務 | 罰款上限 |
|---|---|---|---|
| **Prohibited** | social scoring / subliminal manipulation | 禁止 | **€35M 或 7% 全球年營業** |
| **High-risk (Annex III 8 domain)** | biometric / critical infra / education / employment / credit / law enforcement / migration / justice | audit trail + risk assessment + EU database 註冊 + 強制 human oversight | €15M 或 3% |
| **Transparency** | chatbot / deepfake / emotion AI | 必標「AI-bot」/「AI generated」 | €17M 或 4% |
| **GPAI (General Purpose AI)** | foundation model (Claude / GPT / Gemini) | technical doc + copyright policy + summary of training data | 依規模 |

**8 high-risk domain**（記下來）：biometric / critical infrastructure / education / employment / credit & insurance / law enforcement / migration & border / justice & democratic process。

**實作影響**：用 agent 做 resume scanner → 自動 promote 為 high-risk → 開 audit trail + risk assessment + EU 註冊 + 強制 human oversight。對 EU 用戶必加「[AI-bot]」標籤（transparency）。

---

## OpenTelemetry GenAI Semantic Conventions

- **是什麼**：CNCF OTel 為 LLM / agent 標準化的 `gen_ai.*` 命名規約。
- **核心 span**：`invoke_agent {gen_ai.agent.name}` / `chat {model}` / `embeddings`。
- **核心 metric**：`gen_ai.client.token.usage` (histogram by direction) / `gen_ai.client.operation.duration`。
- **2026 狀態**：spec experimental，multi-agent convention 在 CNCF SIG 發展中。
- **已實作**：Datadog LLM Observability / Uptrace / OpenLLMetry SDK / Grafana Tempo / Honeycomb。

**5 分鐘上手**（Python）：
```bash
pip install opentelemetry-instrumentation-anthropic
```
```python
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()
# agent code 跑下去、span 自動 export 到 OTel collector
```

[Ch 15 §5a 完整講解 →](../chapters/ch15_deploy_audit_replay/#5a-opentelemetry-genai--業界標準-observability)

---

## 何時該做哪個？決策樹

```
你在做的 agent 是？
├─ 內部 demo / POC → 都不用做，先把 functional 跑起來
├─ 賣給 EU 客戶 / 公部門 RFP → ISO 42001 認證準備
├─ 賣給美國 federal / 銀行 → NIST AI RMF 流程文件
├─ 涉 8 high-risk domain → EU AI Act 強制 audit + EU 註冊
└─ 任何 production agent → OpenTelemetry GenAI (observability 基本盤)
```

---

## 完整講解

- **3 大標準對 V3 / agentz_mini 影響** → [Ch 15 §5b 合規對照](../chapters/ch15_deploy_audit_replay/#5b-合規--iso-42001--nist-ai-rmf--eu-ai-act) — V3 audit / replay / cost cap / intervention 4 pillar 怎麼對映 ISO/NIST/EU AI Act
- **OpenTelemetry GenAI 5 分鐘上手** → [Ch 15 §5a](../chapters/ch15_deploy_audit_replay/#5a-opentelemetry-genai--業界標準-observability) + [Ch 8 §3](../chapters/ch08_cost_observability/)
- **Multi-agent 新興安全** → [Ch 14 §8c](../chapters/ch14_multi_agent/#8c-2026-multi-agent-新興安全議題) — ICE / Consensus Trap / Slopsquatting 在 multi-agent 場景下的防禦（合規 audit 要看的 risk）
- **詞條深入** → [名詞表 · Production](../glossary/production)（4 個合規詞 4 欄解釋）+ [名詞表 · Agent §5](../glossary/agent#_5-multi-agent-verification--安全2026-新加)（3 個 multi-agent 安全詞）
- **EU AI Act 倒數** → 2026-08-02 deadline，[Ch 15 §3](../chapters/ch15_deploy_audit_replay/)

> ⚠️ **不是法律建議**。production 導入合規前找律師 / 顧問。台灣國科會 AI 基本法草案 2025-11 已公布、跟 EU AI Act 對齊（[Ch 15 §5b.3](../chapters/ch15_deploy_audit_replay/#5b-3-注意)）。

---

**下一頁** → [CLI / Git](./cli) · [SDK](./sdk) · [Pricing](./pricing) · [Patterns](./patterns) · [MCP / Skills](./mcp) · [Governance](./governance)
