"""Ch 8 — Cost tracker: wrap Anthropic SDK + SQLite log + trip wire。

Pattern:
    每個 LLM call 過這層 → 自動拆 input/output token → 換算 USD → 寫 SQLite
    + 每次 check daily total，超 cap 直接 raise CostCapExceeded

跑：
    uv run cost_tracker.py "用繁中介紹 LLM Token"
    sqlite3 costs.db "SELECT date(ts), SUM(cost_usd) FROM calls GROUP BY date(ts);"
"""
from __future__ import annotations

import datetime
import json
import os
import sqlite3
import sys
import uuid
from dataclasses import dataclass

import anthropic


# === 2026-05 snapshot pricing (USD per 1M tokens). 過期請去 Anthropic console 查 ===
PRICING = {
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4-7": {"input": 15.00, "output": 75.00},
}


class CostCapExceeded(Exception):
    """Daily cost 超 cap，agent 應該 fail-closed。"""


@dataclass
class CallRecord:
    call_id: str
    ts: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    run_id: str | None  # 多 call 串一個 run


class CostTracker:
    def __init__(self, db_path: str = "costs.db", daily_cap_usd: float = 1.00):
        self.conn = sqlite3.connect(db_path)
        self.daily_cap_usd = daily_cap_usd
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS calls (
                call_id TEXT PRIMARY KEY,
                ts TEXT,
                model TEXT,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost_usd REAL,
                run_id TEXT
            )
        """)
        self.conn.commit()
        self._client = anthropic.Anthropic()

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """換算 USD（per 1M token pricing）。"""
        p = PRICING.get(model)
        if not p:
            return 0.0  # unknown model 不阻擋但也不算錢（先警告）
        return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000

    def today_total(self) -> float:
        today = datetime.date.today().isoformat()
        row = self.conn.execute(
            "SELECT COALESCE(SUM(cost_usd), 0) FROM calls WHERE date(ts) = ?",
            (today,),
        ).fetchone()
        return row[0]

    def messages_create(self, run_id: str | None = None, **kwargs) -> anthropic.types.Message:
        """Wrap Anthropic SDK call — 自動 log + 阻擋超 cap。

        和 client.messages.create() 介面一樣。
        """
        # Pre-flight: 已經超 cap 直接擋
        today = self.today_total()
        if today >= self.daily_cap_usd:
            raise CostCapExceeded(
                f"daily cost ${today:.4f} >= cap ${self.daily_cap_usd:.2f} — fail-closed"
            )

        # 真 call
        resp = self._client.messages.create(**kwargs)

        # 抽 token usage
        usage = resp.usage
        in_tok = usage.input_tokens
        out_tok = usage.output_tokens
        cost = self.estimate_cost(kwargs.get("model", ""), in_tok, out_tok)

        # Log
        rec = CallRecord(
            call_id="call_" + uuid.uuid4().hex[:12],
            ts=datetime.datetime.utcnow().isoformat(),
            model=kwargs.get("model", "unknown"),
            input_tokens=in_tok,
            output_tokens=out_tok,
            cost_usd=cost,
            run_id=run_id,
        )
        self.conn.execute(
            "INSERT INTO calls VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rec.call_id, rec.ts, rec.model, rec.input_tokens, rec.output_tokens, rec.cost_usd, rec.run_id),
        )
        self.conn.commit()

        print(f"  [cost] model={rec.model} in={in_tok} out={out_tok} cost=${cost:.5f} today=${today + cost:.4f}/{self.daily_cap_usd}")

        return resp

    def by_model(self) -> dict:
        """Group by model — 看哪個 model 燒最多。"""
        rows = self.conn.execute(
            "SELECT model, COUNT(*), SUM(cost_usd) FROM calls GROUP BY model"
        ).fetchall()
        return {r[0]: {"calls": r[1], "cost_usd": r[2]} for r in rows}

    def by_run(self) -> dict:
        """Group by run_id — 看哪 run 最貴。"""
        rows = self.conn.execute(
            "SELECT COALESCE(run_id, '(no run)'), COUNT(*), SUM(cost_usd) FROM calls GROUP BY run_id"
        ).fetchall()
        return {r[0]: {"calls": r[1], "cost_usd": r[2]} for r in rows}


def demo(user_msg: str):
    tracker = CostTracker(daily_cap_usd=0.05)  # 故意設低，超 5 cent 就停
    run_id = "demo_" + uuid.uuid4().hex[:8]

    try:
        # Haiku call
        resp1 = tracker.messages_create(
            run_id=run_id,
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": user_msg}],
        )
        print(f"\nHaiku answer: {resp1.content[0].text[:200]}\n")

        # Sonnet call 同 run_id
        resp2 = tracker.messages_create(
            run_id=run_id,
            model="claude-sonnet-4-6",
            max_tokens=400,
            messages=[
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": resp1.content[0].text},
                {"role": "user", "content": "把上面用 5 句話濃縮"},
            ],
        )
        print(f"\nSonnet refine: {resp2.content[0].text[:200]}\n")

    except CostCapExceeded as e:
        print(f"\n⛔ {e}")

    print(f"\n=== Report ===")
    print(f"Today total: ${tracker.today_total():.5f} / ${tracker.daily_cap_usd}")
    print(f"By model: {json.dumps(tracker.by_model(), indent=2)}")
    print(f"By run: {json.dumps(tracker.by_run(), indent=2)}")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)
    msg = " ".join(sys.argv[1:]) or "用繁中介紹 LLM token 是什麼"
    demo(msg)
