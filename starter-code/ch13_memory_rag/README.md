# Ch 13 — Memory & RAG starter

對應 [AgentZ Ch 13](../../chapters/ch13_memory_rag/) 練習 13.1 / 13.2 / 13.3。

## 跑

```bash
cd starter-code/ch13_memory_rag
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."   # chroma embedding 用 OpenAI
uv run session_memory.py
uv run rag_demo.py
```

## 練習

- **13.1**: 完成 `session_memory.py` 的 summarize 壓縮（30 輪對話 context 始終 < 50K token）
- **13.2**: 完成 `rag_demo.py`——切 chunk + embed + Chroma + query
- **13.3**: 加 contextual retrieval（每 chunk 加 50 字 context）對比有/無 contextualize 的召回率

## 成功標準

- 13.1: 跑 30 輪對話，每輪 `/usage` 顯示 input token 始終 < 50K
- 13.2: 從你的 5-10 個 .md 檔答出來的問題
- 13.3: 5 個問題的有/無 contextualize 對比表填齊
