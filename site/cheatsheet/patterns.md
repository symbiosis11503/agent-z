---
title: 速查卡 — Agent 範式 + Cost cap pattern
description: ReAct / Plan-and-Solve / Reflection 三範式 + Cost cap fail-closed pattern (SQLite-backed)。
---

# 速查卡 · Patterns

[← 回速查卡總覽](../cheatsheet)

## ReAct loop 範式

```python
def react_loop(goal, max_steps=5):
    history = []
    for _ in range(max_steps):
        thought = llm(prompt=f"Goal: {goal}\nHistory: {history}\nNext?")
        if "FINAL_ANSWER:" in thought:
            return thought.split("FINAL_ANSWER:")[-1]
        # parse: tool_name, args = parse_tool(thought)
        # result = run_tool(tool_name, args)
        history.append({"thought": thought, "result": result})
    return "max steps reached"
```

## Plan-and-Solve 範式

```python
plan = llm("給定 task X，列 5 步驟 plan")
for step in plan:
    result = react_loop(step, max_steps=3)
    if not ok(result):
        plan = revise(plan, result)  # 中途 revise
final = llm("整合 results 寫 answer")
```

## Reflection wrap

```python
draft = base_agent(task)
for _ in range(max_reflect_iters := 3):
    critique = critic_agent(draft)
    if critique.verdict == "pass":
        break
    draft = base_agent(task, critique=critique)
```

---

## Cost cap pattern

```python
import sqlite3, datetime
conn = sqlite3.connect("costs.db")
conn.execute("""CREATE TABLE IF NOT EXISTS calls (
    call_id TEXT, ts TEXT, model TEXT,
    input_tokens INT, output_tokens INT, cost_usd REAL
)""")

DAILY_CAP = 0.10  # USD

def safe_call(**kwargs):
    today_total = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) FROM calls WHERE date(ts)=?",
        (datetime.date.today().isoformat(),)
    ).fetchone()[0]
    if today_total >= DAILY_CAP:
        raise CostCapExceeded(f"${today_total} >= ${DAILY_CAP}")
    resp = client.messages.create(**kwargs)
    # log usage
    conn.execute("INSERT INTO calls VALUES (?, ?, ?, ?, ?, ?)", ...)
    conn.commit()
    return resp
```

[完整 Ch 8 starter →](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch08_cost_observability)

---

**下一頁** → [MCP / Skills](./mcp) · [Governance](./governance) · [CLI / Git](./cli) · [SDK](./sdk) · [Pricing](./pricing)
