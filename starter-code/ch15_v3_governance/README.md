# Ch 15 — V3 Governance starter

對應 [AgentZ Ch 15](../../chapters/ch15_deploy_audit_replay/) 練習 15.1 + 15.2。

## 跑

```bash
cd starter-code/ch15_v3_governance
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."

# 15.1: 寫一個 agent + audit + replay 都進 SQLite
uv run agent_with_audit.py

# 15.2: 包成 FastAPI HTTP API
uv run uvicorn server:app --reload --host 0.0.0.0 --port 8000
# 另一個 terminal:
curl -X POST http://localhost:8000/v1/run -H 'Content-Type: application/json' \
  -d '{"message": "你好，用繁中介紹自己"}'
```

## 練習

- **15.1**: 完成 `agent_with_audit.py` — Ch 12 mini framework + AuditSink + ReplayStore SQLite
- **15.2**: 寫 `server.py` FastAPI wrap，提供 POST /v1/run + POST /v1/runs/{id}/abort + GET /v1/runs/{id}/audit
- **15.3**: 跑一個會超 cost cap 的 run，觀察 audit 有 `cost_exceeded` 事件

## 成功標準

- 跑完 run、`sqlite3 audit.db "SELECT * FROM audit_events"` 看到完整時序
- curl abort 真的中止 + audit 有 `run_aborted` 事件
