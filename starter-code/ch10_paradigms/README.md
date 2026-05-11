# Ch 10 — ReAct / Plan-and-Solve / Reflection starter

對應 [AgentZ Ch 10](../../chapters/ch10_react_paradigms/) 練習 10.1 / 10.2 / 10.3。

## 跑

```bash
cd starter-code/ch10_paradigms
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."

uv run react_agent.py        # 純 ReAct
uv run plan_and_solve.py     # plan 階段 + execute 階段
uv run reflection.py         # act → critique → redo
```

## 練習

- **10.1**: 看書 §3 完整實作對照、自己寫 `plan_and_solve.py` 的 plan 階段
- **10.2**: 寫 `reflection.py` 的 critique loop（parse_score / parse_feedback）
- **10.3**: 寫 `hybrid_agent.py` 串 Plan → ReAct → 一次 Reflection

## 成功標準

`uv run plan_and_solve.py` 跑「研究 3 個 OSS agent framework 並寫比較表」、看 plan 階段印出計畫、execute 階段照 plan 走。
