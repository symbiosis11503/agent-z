# Ch 9 — Weather Agent starter

對應 [AgentZ Ch 9](../../chapters/ch09_function_calling/) 練習 9.1 / 9.2 / 9.3。

## 怎麼跑

```bash
cd starter-code/ch09_weather_agent
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."
uv run starter.py
```

## 練習

- **9.1**: 完成 `weather_agent.py` 的 `run_agent()` loop（已有骨架）
- **9.2**: 改 `weather_agent.py` 用 `asyncio.gather` 並行執行 tool
- **9.3**: 加 `get_weather` 對「不存在城市」回 `ERROR: ...`、觀察 LLM self-correct

## 成功標準

跑 `uv run weather_agent.py "比較台北跟東京哪個比較熱"`，看到 agent 自動 call 兩次 `get_weather` 並回比較結論。
