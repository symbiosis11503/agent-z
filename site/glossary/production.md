---
title: 名詞表 — Production Governance + 模型訓練 / Agentic-RL
description: Budget Cap / Intervention / Audit / Replay / Guardrails + SFT / GRPO / Agentic-RL
---

# 名詞表 · Production Governance + 模型訓練 / Agentic-RL

[← 回名詞表總覽](../glossary)

## 8. Production Governance

### 預算上限 / Budget Cap
- **專業**：在 agent run / day / user / org 層級設定累積 token spend 上限。超過 fail-closed（raise exception / stop run）。
- **白話**：「最多花 X 元」的硬規定。超過就停。
- **範例**：V3 三層 cap：`costBudgetUSDPerRun = 0.5` / `costBudgetUSDPerDay = 10`。Anthropic console 也有月帳號 cap 可設。
- **章節**：[Ch 8 §4.1](../chapters/ch08_cost_observability/#41-設-budget-cap)

### 介入 / Intervention / Abort
- **專業**：external signal 中止 in-progress agent run。實作：abort registry 標記 run_id、agent loop 在每個 LLM call / tool call 之間 / SSE 之間檢查 flag、撞到 raise / 結束。
- **白話**：agent 跑到一半你按「停」、它馬上停下。
- **範例**：Claude Code Ctrl+C、V3 POST `/runs/{id}/abort?reason=...`、UI「介入」chip。
- **章節**：[Ch 8 §4.3](../chapters/ch08_cost_observability/#43-強制中止-ctrlc--abort)

### 稽核 / Audit
- **專業**：每個 agent action（LLM call / tool call / state transition / cost event / abort）寫進 append-only event log。每筆 `audit_event_id` + ts + category + run_id + payload。
- **白話**：「agent 做了什麼、何時做的」全紀錄。出問題能查。
- **範例**：V3 PostgreSQL `audit_events` JSONB table、`category` enum (`llm_call` / `tool_call` / `run_aborted` / `cost_exceeded` / ...)。
- **章節**：[Ch 15 §3.1](../chapters/ch15_deploy_audit_replay/#31-audit-log)

### 回放 / Replay
- **專業**：紀錄每次 LLM call / tool call 完整 input + output + cost，事後可重現整個 run 或從某 step 分叉重跑（fork replay）。
- **白話**：「agent 那次跑的所有細節錄影下來、能倒帶看」。
- **範例**：V3 `replay_records` 表存每 step 的 input/output JSONB、cost_estimate / cost_observed。UI 列 trace、點某 step 看 raw、或「從這 step 改 prompt 再跑」。
- **章節**：[Ch 15 §3.2](../chapters/ch15_deploy_audit_replay/#32-replay)

### 護欄 / Guardrails
- **專業**：限制 agent 行為的硬約束。實作層次：filesystem path allow-list / MCP server scope / Hook PreToolUse blocking / model-level safety classifier。
- **白話**：「agent 不准做這些事」的圍欄。
- **範例**：filesystem MCP 只給 `/tmp/agentz` 路徑、Hook 擋住 `rm -rf` 指令、production secret 從不進 prompt。
- **章節**：[Ch 6 §8](../chapters/ch06_mcp/#8-mcp-server-的安全性)

---

## 9. 模型訓練 / Agentic-RL

### 監督式微調 / SFT (Supervised Fine-Tuning)
- **專業**：用人工標註的 `(prompt, ideal_output)` pair 跑 cross-entropy loss、更新 model 參數（全參數 / LoRA / QLoRA）。
- **白話**：「給範本、讓 model 學著像範本回答」。
- **範例**：1K 筆 function-calling 範例 fine-tune Llama-3-8B，得到 BFCL 比 base model 高 10% 的小 model。
- **章節**：[Ch 17 §2](../chapters/ch17_builder_advanced/)

### 群體相對策略優化 / GRPO (Group Relative Policy Optimization)
- **專業**：對同一 prompt sample N 個 output（N=8 常見），給每個算 reward，計算 group_mean reward，每個 output advantage = reward - group_mean，policy gradient 更新。不用 reference model。
- **白話**：「同一題出 8 個版本、看哪個對得分高、學那個方向」。
- **範例**：DeepSeek-R1 用 GRPO + 純 RL 跑出 OpenAI o1 水平的 reasoning model（沒 SFT 暖身、671B model）。
- **章節**：[Ch 17 §5](../chapters/ch17_builder_advanced/#5-grpo-概念)

### 智能體強化學習 / Agentic-RL
- **專業**：用 RL 訓 agent 跑多步 task。Reward 通常 sparse（任務完成 = 1、其他 = 0）、需 trajectory rollout + advantage estimation + policy update。
- **白話**：給 agent「成功就好、過程自由」的訓練——它自己摸索哪些 tool sequence 有效。
- **範例**：訓練「訂機票 agent」、reward 是「最後是否真的訂到 + 票多便宜」。模型自己摸出「先比價再訂」的策略。
- **章節**：[Ch 17](../chapters/ch17_builder_advanced/)

---

**其他類別** → [基礎](./foundation) · [Agent / CLI](./agent) · [實務](./practice) · [Production](./production) · [台灣/混淆 pair](./taiwan-misc)
