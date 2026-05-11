# Ch 8 — Cost Tracker starter

對應 [AgentZ Ch 8](../../chapters/ch08_cost_observability/) 練習 8.1 / 8.2 / 8.3。

把 Anthropic SDK 包一層、每 call 自動 log 到 SQLite + 超 daily cap 直接 raise CostCapExceeded。

## 跑

```bash
cd starter-code/ch08_cost_observability
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."

uv run cost_tracker.py "用繁中介紹 LLM Token"
```

看到 demo 跑 2 個 LLM call（Haiku + Sonnet）、每個 call 印 `[cost]` 行、最後印 by_model / by_run report。

查 SQLite：

```bash
sqlite3 costs.db "SELECT date(ts), model, COUNT(*), SUM(cost_usd) FROM calls GROUP BY date(ts), model;"
```

## 在學什麼

| 觀念 | 程式碼在哪 |
|---|---|
| **Pricing snapshot** | `PRICING` dict — 2026-05 USD/1M token。**會過期，請 update** |
| **Pre-flight cap check** | `messages_create()` 先 `today_total()` 比 cap |
| **Fail-closed** | 超 cap raise `CostCapExceeded`，agent 應該停 |
| **SQLite log** | `calls` table — call_id / ts / model / tokens / cost / run_id |
| **run_id grouping** | 一個 agent run 內多 call 串同 run_id，可以看「這個 run 燒多少」 |
| **By model / by run** | 後台 query — 看哪個 model / run 燒最多 |
| **Wrap pattern** | `CostTracker.messages_create(**kwargs)` 介面 = `client.messages.create(**kwargs)`，drop-in |

## 練習

- **8.1**: 把這個 cost tracker 加進 `ch12_mini_framework` 的 agent loop，看 ReAct 跑一個 task 燒多少
- **8.2**: 加 `weekly_cap_usd` 防 daily cap 還是月底炸（cron 每天 reset 不夠）
- **8.3**: 加 trip wire on `output_tokens > 8000` — agent 失控狂寫 output 也擋掉
- **8.4 (bonus)**: 改用 PostgreSQL（多人共用 dashboard）

## 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **PRICING 過期** | log 的 cost 跟帳單對不起來 | 每月對 [Anthropic pricing](https://www.anthropic.com/pricing) update |
| **多 process 同時寫** | SQLite locked | 改 PostgreSQL or 用 WAL mode |
| **token 算錯模型** | 不在 PRICING 裡的 model cost=0 | 加 unknown model warning + fallback 估值 |
| **過 cap 後重試** | 整 agent loop 炸 | catch `CostCapExceeded` 後優雅退出 + 通知 |
| **prompt cache 沒折扣** | 大 prompt 重複 call 沒省到 | 用 cache_control beta + 估算 cache hit cost |
| **timezone 不一致** | daily_total 跨日異常 | 用 UTC 或統一 timezone |
| **沒 retry budget** | 一次 429 浪費 retry quota | retry 也算 cost、retry policy 寫進 budget |

## 進階：production 升級路線

```
        你現在這層 (mini cost tracker)
              ▼
        +daily/weekly/monthly cap
              ▼
        +per-team cost allocation
              ▼
        +SSO / RBAC dashboard
              ▼
        Helix V3 governance stack (Ch 15)
```

[Ch 15](../../chapters/ch15_deploy_audit_replay/) 介紹 V3 的 production cost cap 是什麼樣（每 endpoint pre-flight estimate + post-flight log + Grafana dashboard）。

## 補充閱讀

- [Anthropic pricing](https://www.anthropic.com/pricing)
- AgentZ [Ch 8 章節](../../chapters/ch08_cost_observability/)
- AgentZ [Ch 15 V3 case study](../../chapters/ch15_deploy_audit_replay/)
- [OpenAI usage API](https://platform.openai.com/docs/api-reference/usage) — 對應的 cost lookup
- [LiteLLM cost tracking](https://docs.litellm.ai/docs/observability/cost_tracking) — 跨 vendor 通用方案
