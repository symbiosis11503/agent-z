"""Ch 15 Audit + Replay agent starter — 練習 15.1。

完成後跑：
    uv run agent_with_audit.py "用繁中介紹 AI Agent"
    sqlite3 audit.db "SELECT * FROM audit_events"
    sqlite3 replay.db "SELECT * FROM replay_records"
"""
from __future__ import annotations

import datetime
import json
import os
import sqlite3
import sys
import uuid

import anthropic


class AuditSink:
    def __init__(self, db_path: str = "audit.db"):
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
        self.conn.commit()

    def emit(self, category: str, run_id: str, payload: dict) -> str:
        event_id = "aud_" + uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO audit_events VALUES (?, ?, ?, ?, ?)",
            (event_id, datetime.datetime.utcnow().isoformat(), category, run_id, json.dumps(payload, ensure_ascii=False)),
        )
        self.conn.commit()
        return event_id


class ReplayStore:
    def __init__(self, db_path: str = "replay.db"):
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
        self.conn.commit()

    def record(self, run_id: str, step_idx: int, kind: str, input_data: dict, output_data: dict, cost: float) -> str:
        rid = "rep_" + uuid.uuid4().hex[:12]
        self.conn.execute(
            "INSERT INTO replay_records VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rid, run_id, step_idx, kind,
             json.dumps(input_data, ensure_ascii=False, default=str),
             json.dumps(output_data, ensure_ascii=False, default=str),
             cost),
        )
        self.conn.commit()
        return rid


def run_agent(user_message: str, cost_cap_usd: float = 0.10) -> dict:
    """完成這個 — 練習 15.1。

    應該：
    1. 開新 run_id (rta_xxx)
    2. AuditSink.emit('run_started', run_id, {message: ...})
    3. ReAct loop:
       a. call LLM, ReplayStore.record('llm_call', ...)
       b. AuditSink.emit('llm_call', ...)
       c. 累積 cost；超 cap → emit('cost_exceeded') + return
    4. final: emit('run_completed')
    """
    audit = AuditSink()
    replay = ReplayStore()
    run_id = "rta_" + uuid.uuid4().hex[:12]
    audit.emit("run_started", run_id, {"message": user_message})

    # TODO 15.1: 完成 ReAct loop with audit + replay recording
    raise NotImplementedError("Complete run_agent for exercise 15.1")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    msg = " ".join(sys.argv[1:]) or "用繁中介紹 AI Agent。"
    result = run_agent(msg)
    print(json.dumps(result, ensure_ascii=False, indent=2))
