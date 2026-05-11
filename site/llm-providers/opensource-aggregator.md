---
title: LLM 申請 — 開源 / 聚合 / 速度 / 便宜（Groq / DeepSeek / Mistral / OpenRouter / Grok）
description: Groq、DeepSeek、Mistral、OpenRouter、Grok 5 家「免費/便宜/快速/聚合」型 LLM 申請、範例、費用
---

# 熱門 LLM · 開源 / 聚合 / 速度 / 便宜

[← 回 LLM / API 申請總覽](../llm-providers)

不想全壓在美國三大廠？這 5 家適合：免費試（Groq）、推理便宜（DeepSeek）、歐盟合規（Mistral）、一個 key 打 100+ 家（OpenRouter）、X 社交整合（Grok）。

[[toc]]

## 4. Groq（**最快 + 免費**）

### 介紹
- 不是 Grok（xAI）— **Groq** 是硬體公司，自研 LPU 推論晶片
- 推論速度 ~500 tok/s（一般 GPU 50-100 tok/s）
- 跑 Llama 3.x / Mixtral / Gemma 等開源模型
- 免費層每天幾千 request，做 demo / 學習超夠

### 申請
1. https://console.groq.com/ → Sign up（Email / Google）
2. API Keys → Create API key → `gsk_...`
3. 不需要信用卡（免費層）

### Python（OpenAI 相容介面）
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)
resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
print(resp.choices[0].message.content)
```

### 費用
- 免費層慷慨
- 付費：Llama 3.3 70B input $0.59、output $0.79 / 1M

---

## 5. DeepSeek（**推理強 + 便宜**）

### 介紹
- DeepSeek R1：推理能力接近 o1，價格 1/30
- DeepSeek V3：通用模型，跟 Claude Sonnet 同檔位
- 中國公司，但 API 在境外可直接打

### 申請
1. https://platform.deepseek.com/ → Sign up
2. 充值（最低 $1）— 信用卡 / Stripe
3. API key → `sk-...`

### Python（OpenAI 相容）
```python
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)
resp = client.chat.completions.create(
    model="deepseek-chat",  # or "deepseek-reasoner"
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
```

### 費用
- deepseek-chat (V3)：input $0.14（cache hit）/ $0.27 / 1M
- deepseek-reasoner (R1)：input $0.55 / output $2.19 / 1M

---

## 6. Mistral AI（歐盟、GDPR 友善）

### 介紹
- 法國公司，資料留歐盟
- 開源 model（Mistral 7B, Mixtral 8x7B）也能自架
- 適合需要 EU 合規的場景

### 申請
1. https://console.mistral.ai/ → Sign up
2. Workspace → Billing → Add card
3. API Keys → 建立

### Python
```python
# pip install mistralai
from mistralai import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
resp = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
print(resp.choices[0].message.content)
```

### 費用
- Mistral Large：input $2、output $6 / 1M
- Mistral Small：input $0.2、output $0.6 / 1M

---

## 7. OpenRouter（聚合器，**一個 key 打全部**）

### 介紹
- 一個 API key 可以打 Anthropic / OpenAI / Google / Mistral / Llama 等 100+ 模型
- 每家 list price + 5.5% 手續費
- 適合「想比較多家、不想開 N 個帳號」的學習階段

### 申請
1. https://openrouter.ai/ → Sign up (Google / GitHub)
2. Credits → 充值（最低 $5，支援信用卡 / 加密貨幣）
3. Keys → Create key → `sk-or-v1-...`

### Python（OpenAI 相容）
```python
client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)
resp = client.chat.completions.create(
    model="anthropic/claude-haiku-4.5",  # 也可以 "openai/gpt-4o-mini" 等
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
```

### 費用
- 各家 list price + 5.5%
- 也提供「免費」型號（速率受限）

---

## 8. xAI Grok

### 介紹
- Elon Musk 的 xAI
- 整合 X (Twitter) realtime 資料
- 訂閱 X Premium+ 內含網頁版

### 申請
1. https://console.x.ai/ → Sign up
2. Billing → Add card
3. API Keys → `xai-...`

### Python（OpenAI 相容）
```python
client = OpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)
resp = client.chat.completions.create(
    model="grok-2-latest",
    messages=[{"role": "user", "content": "用繁中介紹 AI Agent。"}],
)
```

---


---

**其他類別** → [商業 API](./commercial) · [本地/主權](./local-sovereign) · [全本一頁](./all)
