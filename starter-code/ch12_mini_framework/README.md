# Ch 12 — Mini Framework starter

對應 [AgentZ Ch 12](../../chapters/ch12_mini_framework/) 練習 12.1 / 12.2 / 12.3。

## 怎麼跑

```bash
cd starter-code/ch12_mini_framework
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."
uv run run_agent.py
```

## 練習

- **12.1**: 補齊 `agentz_mini.py` 的 `Agent.run()` (skeleton 已 in place)
- **12.2**: 加 `Agent.run_with_reflection(task, target_score=8)` wrapper
- **12.3**: `replay.py` 讀 step trace JSON 並逐步 print（已有範例）

## 跟書中差異

書中 Ch 12 §3 給的是 reference 完整實作（150 行）。這邊 starter 故意留 NotImplementedError 讓你動手寫，建議：
1. 先看 Ch 12 完整實作對照
2. 自己重寫一遍（不要直接 copy-paste）
3. 用 `run_agent.py` 驗證跑得起來

## 成功標準

`uv run run_agent.py` 印出 Claude 的回答 + step trace + cost。
