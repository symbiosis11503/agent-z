# Ch 15 — Deploy + Audit + Replay + Cost Cap：Helix V3 完整 Case Study

> **90-120 分鐘**。Builder 階段壓軸。讀完你會懂：production-grade agent 必備的 4 個 governance pillar（audit / replay / cost cap / observability），跟 Helix V3 怎麼做的。
>
> 動手練習：把你 Ch 12 的 mini framework 升級到 V3 級 governance、deploy 上線一個 HTTP API。
>
> 前置：完成 [Ch 14](../ch14_multi_agent/) — multi-agent 寫得出來。
>
> 🛠 **Starter code**: [`starter-code/ch15_v3_governance/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch15_v3_governance) — AuditSink + ReplayStore + agent_with_audit.py SQLite governance scaffold (練習 15.1) + FastAPI server (練習 15.2)。

---

## 1. 從 toy 到 production 的 gap

Ch 12 你寫了 `agentz_mini.py` ~200 行。能跑、能 demo、能 hackathon。但拿去**真實上線給用戶用**，立刻撞牆：

| 問題 | toy script | production 需要 |
|---|---|---|
| 學員不小心無限 loop 燒 $500 | 沒擋 | **cost cap**（per-run / per-day / per-user） |
| 出問題沒 trace 看 | 沒紀錄 | **audit log** + 結構化儲存 |
| 客戶說「我那次的答案怪怪的能再來一次嗎」 | 沒辦法 | **replay**（重現整次 run） |
| 用戶問「我這個月花多少？」 | 看你心情 | **per-user cost analytics** |
| Anthropic 掛了 | 整個服務掛 | **multi-provider fallback** |
| 跑長 task 想中止 | Ctrl+C 自己 | **abort endpoint + audit** |
| 多人共用要分 key | 一個全域 env | **vault + 加密** |

這就是 [Helix V3](https://github.com/symbiosis11503/helix-framework) 幹的事。本章用 V3 當完整 case study。

---

## 2. Helix V3 是什麼

V3 是 Symbiosis (SBS) 開源的 **agentic platform**，把上面 7 個 production gap 全包：

- **Multi-provider catalog**（9 家：Claude / OpenAI / Gemini / Groq / Mistral / OpenRouter / DeepSeek / oauth-gpt / mock）
- **ProviderKeyVault**（Fernet 加密 + 「先驗證」pre-flight ping）
- **Cost cap**（per-run / per-day / per-user，超過 fail-closed）
- **Audit log**（每個 LLM call / tool call / abort / cost 事件都有 audit_event_id）
- **Replay**（每個 run 存完整 step trace JSONB，可重放）
- **Run abort registry**（中止跑到一半的 agent + audit 事件）
- **MCP server expose**（V3 變 MCP server 給其他 agent 接）
- **Command Center UI**（「組織操作台」— 建/派/看進度/看風險/看結果/介入 六動詞）

GitHub: https://github.com/symbiosis11503/helix-framework
線上 demo: https://helix.symbiosis.tw (路由還在 fix 中)

---

## 3. 四大 governance pillar 拆解

### 3.1 Audit Log

**規範**：每個 agent run 內部發生的事都要紀錄。

V3 audit_event 結構：
```python
{
    "audit_event_id": "aud_a1b2c3d4e5f6",  # UUID
    "ts": "2026-05-11T13:45:00Z",
    "category": "llm_call" | "tool_call" | "run_aborted" | "cost_exceeded" | ...,
    "run_id": "rta_...",
    "session_id": "ses_...",
    "user_id": "wei",
    "payload": { ... },
}
```

寫進 PostgreSQL JSONB 欄位。查詢：
```sql
-- 查某 run 的所有事件
SELECT * FROM audit_events WHERE run_id = 'rta_...' ORDER BY ts;

-- 查最近 1 小時所有失敗的 run
SELECT * FROM audit_events
WHERE category = 'cost_exceeded'
  AND ts > NOW() - INTERVAL '1 hour';
```

UI 上每個 run / agent / session card 都有「→ 查 audit」深連結。

### 3.2 Replay

**規範**：每次 LLM call + tool call 的完整 input / output 要存。

V3 `replay_record` 表：
```python
{
    "replay_record_id": "rep_x9y8z7",
    "run_id": "rta_...",
    "step_index": 0,
    "kind": "llm_call",
    "input": {"model": "...", "messages": [...]},
    "output": {"content": [...], "usage": {...}},
    "cost_estimate_usd": 0.0023,
    "cost_observed_usd": 0.0021,
    "cost_catalog_version": "v3-2026-05",
}
```

Replay UI：
- 列出 run 的所有 step
- 點某 step 看 raw input/output
- 從某 step 開始 fork 一個新 run（改 prompt 試）

### 3.3 Cost Cap

V3 三層：
- `costBudgetUSDPerRun` — 一次 agent run 最多多少
- `costBudgetUSDPerDay` — 帳號一天最多多少
- `cost_intent: "free" | "paid"` — agent template 標記（mock-trial 免費 / claude-paid）

實作（簡化）：
```python
def maybe_estimate(model, prompt_tokens, expected_out):
    p_in, p_out = catalog_lookup(model)
    return (prompt_tokens * p_in + expected_out * p_out) / 1_000_000

def call_llm_with_cap(model, messages, run_state):
    est = maybe_estimate(model, count_tokens(messages), 1000)
    if run_state.cumulative_cost + est > run_state.cap_per_run:
        emit_audit("cost_exceeded", {"est": est, "cumulative": run_state.cumulative_cost, "cap": run_state.cap_per_run})
        raise CostBudgetExceededError(...)
    resp = client.messages.create(model=model, messages=messages)
    real = (resp.usage.input_tokens * p_in + resp.usage.output_tokens * p_out) / 1_000_000
    run_state.cumulative_cost += real
    return resp
```

**重點**：**估算 + 真實**雙軌記錄。估算用來 pre-flight 擋過 cap 的 call、真實用來算錢。

### 3.4 Run Abort + Intervention

V3 W4 Lane F 做的事：

- `RunAbortRegistry`（in-memory + audit log）每個 run 註冊 run_id + session_id
- POST `/v3/agentic/runs/{run_id}/abort?reason=operator_abort` 標記 aborted
- agent loop 每個 LLM call / tool call **之間**檢查 abort flag，被標記就 raise 結束
- SSE streaming 在 between-token / post-token 兩個檢查點
- abort 事件寫 audit（`category=run_aborted`）

UI：每個 running session card 有「介入」chip → 開 modal → 寫原因 → POST abort。

---

## 4. V3 Multi-provider Catalog（iter 149-150）

V3 不綁單家 LLM vendor。`/v3/agentic/providers` 列出 9 個：

```json
{
  "providers": [
    {"provider": "mock", "auth_mode": "api_key", "default_model": "mock-echo"},
    {"provider": "openai", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "anthropic", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "gemini", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "groq", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "mistral", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "openrouter", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "deepseek", "auth_mode": "api_key", "endpoint": "..."},
    {"provider": "oauth-gpt", "auth_mode": "oauth_bridge", "endpoint": "..."}
  ]
}
```

**ProviderKeyVault**（V3 W3 iter 146-148）：
- 用 Fernet 對稱加密把 key 存本機檔
- 「先驗證」按鈕 POST `/providers/{provider}/ping`、真的打 vendor `/models` endpoint 確認 key 可用
- 缺 key fail-closed（不會 fallback mock）

---

## 5. V3 部署架構

```
                ┌──────────────────────────────────┐
User browser →  │ Cloudflare Tunnel                │
                │ helix.symbiosis.tw → VPS-Helix   │
                └──────────────┬───────────────────┘
                               │
                               ▼
                ┌──────────────────────────────────┐
                │ VPS-Helix (FastAPI :8442)        │
                │  /v3/ui/* — Command Center       │
                │  /v3/agentic/* — REST API        │
                │  /v3/mcp/* — MCP server expose   │
                └──────────────┬───────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                              ▼
       ┌─────────────────┐         ┌─────────────────┐
       │ PostgreSQL      │         │ Anthropic /     │
       │ - audit_events  │         │ OpenAI /        │
       │ - replay_records│         │ Gemini / Groq...│
       │ - sessions      │         └─────────────────┘
       └─────────────────┘
```

- Runtime: Python 3.12 + FastAPI + uvicorn + asyncio
- DB: PostgreSQL JSONB 為主 + pgvector 為 RAG memory
- Frontend: Vanilla JS Command Center（v0.1 沒上 framework）

---

## 6. 自己升級你的 agentz_mini → production

### 6.1 加 audit log

```python
import sqlite3, uuid, datetime, json

class AuditSink:
    def __init__(self, db_path="audit.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                ts TEXT,
                category TEXT,
                run_id TEXT,
                payload TEXT
            )
        """)

    def emit(self, category, run_id, payload):
        event_id = "aud_" + uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO audit_events VALUES (?, ?, ?, ?, ?)",
            (event_id, datetime.datetime.utcnow().isoformat(), category, run_id, json.dumps(payload)),
        )
        self.conn.commit()
        return event_id
```

`Agent.run()` 裡每個 LLM call / tool call 都 `audit.emit(...)`。

### 6.2 加 replay store

```python
class ReplayStore:
    def __init__(self, db_path="replay.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS replay_records (
                record_id TEXT PRIMARY KEY,
                run_id TEXT,
                step_index INTEGER,
                kind TEXT,
                input TEXT,
                output TEXT,
                cost_observed REAL
            )
        """)

    def record(self, run_id, step_idx, kind, input_data, output_data, cost):
        rid = "rep_" + uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO replay_records VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rid, run_id, step_idx, kind, json.dumps(input_data, default=str), json.dumps(output_data, default=str), cost),
        )
        self.conn.commit()
```

### 6.3 包 FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
agent = Agent(model="claude-haiku-4-5", tools=[...], cost_cap_usd=0.50)

class RunRequest(BaseModel):
    message: str

@app.post("/v1/run")
def run(req: RunRequest):
    try:
        result = agent.run(req.message)
        return {"answer": result.answer, "cost": result.cost, "run_id": result.run_id}
    except CostExceeded as e:
        raise HTTPException(429, str(e))

@app.post("/v1/runs/{run_id}/abort")
def abort(run_id: str):
    AbortRegistry.mark(run_id)
    return {"status": "aborted"}
```

Deploy：`uv run uvicorn main:app --host 0.0.0.0 --port 8000`，或包 Docker → Fly.io / Railway / 自架 VPS。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 4 — Failure Modes**：cost runaway / context decay
- **Section 7 — Work Modes**：observability / human-in-the-loop / abort

---

## 8. 動手練習

### 練習 15.1：升級你的 agentz_mini → 加 audit + replay

擴 `agentz_mini.py` 加 `AuditSink` + `ReplayStore`，每個 step 寫入。
跑一個 run、再寫 `inspect.py` 從 SQLite 撈 run 的所有 audit + replay 印出來。

**成功標準**：你能從 audit.db / replay.db 重建整個 run 的完整時序。

### 練習 15.2：包成 HTTP API

把 agentz_mini 包成 FastAPI，提供 `POST /v1/run` + `POST /v1/runs/{id}/abort`。用 curl 測一個 run、跑到一半 abort。

**成功標準**：abort 真的中止 + audit 有 `run_aborted` 事件。

### 練習 15.3：逛 V3 source code

clone https://github.com/symbiosis11503/helix-framework，讀：
- `src/helix_v3/agent_framework/run_abort.py` — abort registry
- `src/helix_v3/agent_framework/provider_ping.py` — multi-provider ping
- `src/helix_v3/service/main.py` — FastAPI endpoint 全集

**成功標準**：你能畫出 V3 的「user → command center → API → agent loop → audit / replay」資料流。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 production agent 必備的 4 governance pillar
- [ ] 看過 V3 audit_event / replay_record / cost_cap / abort 怎麼存
- [ ] 看過 V3 multi-provider catalog 9 家結構
- [ ] 升級 agentz_mini 加 audit + replay
- [ ] 包成 FastAPI deploy
- [ ] 讀過 V3 source code 至少 3 個檔案
- [ ] **能跟人解釋 production agent 跟 toy agent 差在哪**

打勾 5 個以上，**Builder 階段完工**！

---

## Builder 階段（Ch 9-15）回顧

你現在會什麼：
- 從零寫 tool use loop
- 三種 agentic 範式都實作過
- 4 個主流 framework 比較得出來
- 自己寫一個 mini framework
- agent 有 session / long-term / RAG memory
- 寫過 multi-agent（pipeline / supervisor / handoff）
- production-grade governance（audit / replay / cost / abort）

下一階段（**進階分流**，Ch 16-18）依你的目的選一條走。

---

## 10. 補充閱讀

- [Helix V3 GitHub](https://github.com/symbiosis11503/helix-framework)
- [Helix V3 quickstart](https://github.com/symbiosis11503/helix-framework/blob/main/docs/QUICKSTART_SELF_HOST.md)
- [Anthropic — Production-ready agents](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/best-practices)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- LangSmith / LangFuse / Helicone — agent observability tools
