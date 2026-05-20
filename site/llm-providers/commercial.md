---
title: LLM 申請 — 商業 API（Claude / GPT / Gemini）
description: Anthropic Claude、OpenAI GPT、Google Gemini 三家美國商業 LLM 申請流程、curl + Python 範例、費用速算
---

# 熱門 LLM · 商業 API（Claude / GPT / Gemini）

[← 回 LLM / API 申請總覽](../llm-providers)

美國三家主流商業 LLM，付費為主、能力最強，AgentZ 多數章節用這幾家做範例。

[[toc]]

## 1. Anthropic Claude（**AgentZ 主推**）

### 介紹
Anthropic 的 Claude 系列，是 AgentZ 預設用的模型。三檔位：
- **Haiku 4.5**：快、便宜、適合大量 ReAct loop / 工具呼叫
- **Sonnet 4.6**：平衡，日常 agent 用這顆
- **Opus 4.6**：最強推理，1M context，適合 coding / 深度規劃

特色：
- 1M token context window（Opus 4.6）
- 內建 tool use（function calling）
- Claude Code CLI 直接綁這顆
- API 行為相對「穩」，agent loop 不易突然亂跑

### 申請 API key
1. 開 https://console.anthropic.com/ → Sign up（用 Google / GitHub / Email 都可以）
2. 驗證 phone 號（必填）
3. Billing → Add payment method（信用卡）
4. 預存 credit（最低 $5）— **重要：先設 monthly limit $10-20 避免炸**
5. API Keys → Create Key → 複製 `sk-ant-api03-...`

> AgentZ Ch 8 / Ch 15 教你怎麼設 cost cap 在程式層把 over-spend 擋掉。

### 第一支呼叫（curl）
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."

curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-haiku-4-5",
    "max_tokens": 200,
    "messages": [{"role": "user", "content": "用繁中介紹 AI Agent。"}]
  }'
```

### 第一支呼叫（Python）
```python
# pip install anthropic
import anthropic

client = anthropic.Anthropic()  # 自動讀 ANTHROPIC_API_KEY env
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}]
)
print(resp.content[0].text)
```

### 費用速算
- Haiku 4.5：input $1 / 1M、output $5 / 1M
- Sonnet 4.6：input $3 / 1M、output $15 / 1M
- Opus 4.6：input $15 / 1M、output $75 / 1M

一次 agent run 大約 5-50K tokens，Haiku 一次跑 < $0.05，Sonnet < $0.20。

---

## 2. OpenAI GPT

### 介紹
業界最廣的模型，Function calling / Assistants API / Realtime API 都最早出。AgentZ Ch 11 會把它跟 Claude 做對照。

### 申請
1. https://platform.openai.com/ → Sign up
2. Billing → Add card → 預存 credit
3. **重要**：新帳號要等 24-48hr 才能用某些 model；先設 usage limit
4. API keys → Create new secret key → `sk-proj-...`

### 範例（curl）
```bash
export OPENAI_API_KEY="sk-proj-..."

curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "用繁中介紹 AI Agent。"}]
  }'
```

### Python
```python
# pip install openai
from openai import OpenAI

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
print(resp.choices[0].message.content)
```

### 費用
- gpt-4o-mini：input $0.15、output $0.60 / 1M（便宜）
- gpt-4o：input $2.5、output $10 / 1M
- o1 / o3（推理）：較貴，input $15-60 / 1M

---

## 3. Google Gemini（**有免費層**）

### 介紹
- 2M token context window（業界最長）
- 影像、影片、PDF 多模態強
- **免費層慷慨**：Flash 系列每分鐘 15 次、每天 1500 次免費

### 申請
1. https://aistudio.google.com/ → 用 Google 帳號登入（不用信用卡）
2. Get API key → Create API key → `AIza...`
3. 想用付費層：到 Google Cloud Console 開 Billing

### Python
```python
# pip install google-generativeai
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-exp")
resp = model.generate_content("用繁中介紹 AI Agent。")
print(resp.text)
```

### 費用
- Flash：免費層 / 付費 input $0.075、output $0.30 / 1M
- Pro：input $1.25、output $5 / 1M
- 2M context 模式價錢翻倍

---


---

**其他類別** → [開源/聚合](./opensource-aggregator) · [本地/主權](./local-sovereign) · [全本一頁](./all)
