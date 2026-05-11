# AgentZ 動手練習 starter code

每個 `ch*` 子目錄對應書中那一章的動手練習 starter code。

## 怎麼用

```bash
# clone 整本書 repo
git clone https://github.com/symbiosis11503/agent-z
cd agent-z/starter-code/<chapter>

# 看該章 starter 怎麼跑
cat README.md

# 用 uv 裝依賴 + 跑
uv sync
uv run starter.py
```

## 章節對應

- [`ch09_weather_agent/`](./ch09_weather_agent/) — 練習 9.1 Weather Agent + 9.2 Parallel + 9.3 Error Recovery
- [`ch10_paradigms/`](./ch10_paradigms/) — 練習 10.1 ReAct vs Plan-and-Solve + 10.2 Reflection
- [`ch12_mini_framework/`](./ch12_mini_framework/) — 練習 12.1 完整 mini framework skeleton
- [`ch13_memory_rag/`](./ch13_memory_rag/) — 練習 13.1 session memory + 13.2 Chroma RAG
- [`ch15_v3_governance/`](./ch15_v3_governance/) — 練習 15.1 audit + replay SQLite + 15.2 FastAPI wrap

## 前置

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- 至少一個 LLM API key（環境變數 `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GROQ_API_KEY`）

詳見 Ch 0 §4-5。
