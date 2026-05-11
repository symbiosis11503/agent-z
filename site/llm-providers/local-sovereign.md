---
title: LLM 申請 — 本地推論 / 台灣主權 / 中文圈（Ollama / TAIDE / Qwen-GLM-Yi）
description: Ollama 本地推論、TAIDE 台灣主權模型自架、Qwen/GLM/Yi 中文圈三家 — 不要 cloud API 的選項
---

# 熱門 LLM · 本地推論 / 台灣主權 / 中文圈

[← 回 LLM / API 申請總覽](../llm-providers)

不想申請 cloud API key、不想付費、想自己掌握資料？這頁列 3 種選擇：本地推論、台灣主權、中文圈三家。

[[toc]]

## 9. 本地跑（Ollama / LM Studio）— **不用 API key**

### 介紹
完全離線、零成本、隱私 100% — 缺點是要你自己有 GPU（或 Apple Silicon M-series）。

### Ollama（CLI 推薦）
```bash
# Mac
brew install ollama
ollama serve  # 背景跑

# 拉模型（4GB 起跳）
ollama pull llama3.2:3b
ollama pull qwen2.5:14b
ollama pull deepseek-r1:7b

# 跑
ollama run llama3.2:3b "用繁中介紹 AI Agent。"
```

### Python（OpenAI 相容）
```python
client = OpenAI(
    api_key="ollama",  # 隨便填
    base_url="http://localhost:11434/v1",
)
resp = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
```

### 硬體建議
| 設備 | 能跑 |
|---|---|
| MacBook Air M2 8GB | 3B 模型勉強 |
| MacBook Pro M3 16GB | 7B 流暢、13B 慢 |
| Mac Studio M3 Ultra 128GB | 70B 流暢、235B 可跑 |
| 4090 24GB | 13B 流暢、Q4 量化 30B |
| 雙 4090 / A100 | 70B+ |

---

## 10. TAIDE（**台灣主權繁中模型**）

### 介紹
- 國科會（NSTC）+ 工研院（ITRI）主導
- 基於 Llama 3 訓練，加大量繁中語料
- 目標：台灣公部門、企業有「不依賴境外 API」的選擇
- **沒有官方雲端 API**，只能自架（HuggingFace 下載 weights）

### 申請使用
1. https://taide.tw/ → 註冊 → 填用途
2. 通過審核後可下載 weights（HuggingFace 連結）
3. 自架（建議用 vllm / Ollama / llama.cpp）

### 自架（Ollama 範例）
```bash
# 從 HuggingFace 下載 GGUF 格式
huggingface-cli download taide/Llama-3.1-TAIDE-LX-8B-Chat \
    --local-dir ./taide-8b

# 寫 Modelfile
cat > Modelfile <<EOF
FROM ./taide-8b/Llama-3.1-TAIDE-LX-8B-Chat.Q4_K_M.gguf
PARAMETER temperature 0.7
EOF

# 載入
ollama create taide-8b -f Modelfile
ollama run taide-8b "用繁中介紹 AI Agent。"
```

### AgentZ 整合
- Ch 13（Memory / RAG）：用 TAIDE 當生成模型 + OpenAI embedding 做 RAG
- Ch 17（Builder 進階）：用 TAIDE 做 Agentic-RL 本地訓練

---

## 11. Qwen / 智譜 GLM / 零一萬物 Yi

中文圈三家強模型，都可以從 HuggingFace 抓 weights 自架，或用各家雲端 API（不一定有境外可用版本）。

- **Qwen2.5**（阿里）：14B / 32B / 72B 開源，繁中表現好
- **GLM-4**（智譜）：6B / 9B 開源
- **Yi-1.5**（零一萬物，李開復）：6B / 34B 開源

自架方式同 TAIDE：用 Ollama 或 vllm。

---


---

**其他類別** → [商業 API](./commercial) · [開源/聚合](./opensource-aggregator) · [全本一頁](./all)
