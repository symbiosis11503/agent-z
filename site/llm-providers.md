# 熱門 LLM 模型 / API 申請 / 使用方法

這頁把目前 AI Agent 圈最常用的 LLM 列出來、教你怎麼申請 API key、怎麼用最簡單的 `curl` 或 Python 跑第一支呼叫，最後給粗略費用比較跟 AgentZ 哪一章會用到。

> **不要把 key 貼到任何公開地方（GitHub、Discord、截圖）**。Key 等同信用卡，外洩就被刷光。AgentZ Ch 8 / Ch 15 有講 cost cap + 環境變數隔離。

[[toc]]

---

## 一張表先看完

| 模型家族 | 廠商 | 強項 | 起手價（粗估） | 是否要信用卡 | AgentZ 章節 |
|---|---|---|---|---|---|
| **Claude** (Sonnet / Opus / Haiku) | Anthropic | 長 context (1M) / coding / agent loop 穩 | 約 $3-15 / 1M input tokens | 是 | Ch 1, 4, 9, 15 |
| **GPT** (4o / o1 / o3) | OpenAI | 通用最強、生態最廣 | $2.5-30 / 1M | 是 | Ch 11 對照 |
| **Gemini** (1.5 Pro / 2.0 Flash) | Google | 超長 context (2M) / 影像強 | $0.075-7 / 1M（**有免費額度**） | 否（免費層）/ 是（付費） | Ch 11 對照 |
| **Llama / Llama 3.x** | Meta | 開源、可本地跑 | 自架免費 / cloud $0.2-1 / 1M | 看 cloud provider | Ch 17 |
| **Mistral / Mixtral** | Mistral AI (法國) | 開源 + cloud、歐盟資料合規 | $0.25-8 / 1M | 是 | — |
| **DeepSeek (R1 / V3)** | DeepSeek (中國) | 推理強、便宜 | $0.14-2.19 / 1M | 是 | — |
| **Grok** | xAI | Twitter / X 整合 | 訂閱制 + API | 是 | — |
| **Groq**（注意拼法） | Groq (硬體公司) | 推論超快（~500 tok/s） | 免費層慷慨 + 付費 $0.05-0.79 / 1M | 否（免費） | — |
| **OpenRouter** | 聚合器 | 一個 key 打 100+ 模型 | 各家 list price + 5.5% 手續費 | 是 | Ch 11 |
| **TAIDE** | 國科會 + 工研院 | 台灣主權繁中模型 | 自架免費（**沒有官方雲端 API**） | — | Ch 13 / Ch 17 |
| **Qwen / Yi / 智譜 GLM** | 阿里 / 零一萬物 / 智譜 | 開源中文強 | 自架免費 / cloud 各家 | 看 cloud | — |

---

## 1. Anthropic Claude（**AgentZ 主推**）

### 介紹
Anthropic 的 Claude 系列，是 AgentZ 預設用的模型。三檔位：
- **Haiku 4.5**：快、便宜、適合大量 ReAct loop / 工具呼叫
- **Sonnet 4.6**：平衡，日常 agent 用這顆
- **Opus 4.7**：最強推理，1M context，適合 coding / 深度規劃

特色：
- 1M token context window（Opus 4.7）
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
- Opus 4.7：input $15 / 1M、output $75 / 1M

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

## 怎麼選？— AgentZ 建議

| 你的目的 | 建議 |
|---|---|
| **完全新手、想免費玩** | Groq（免費快） + Gemini（免費 2M context） |
| **跟著 AgentZ 學** | Anthropic Claude Haiku（充 $5 試 Ch 1-15） |
| **比較多家** | OpenRouter（一個 key 打全部） |
| **公司用、要 EU 合規** | Mistral AI |
| **重度推理、想省錢** | DeepSeek R1（$0.55 / 1M） |
| **隱私敏感、零成本** | Ollama + Llama 3.x 本地 |
| **台灣公部門 / 主權 LLM** | TAIDE 自架 |
| **建 production agent** | Claude（Anthropic 直連）+ V3 governance（Ch 15） |

---

## 安全 + 預算守則（**先看再開帳號**）

1. **每個 provider 都先設 monthly limit**（$10-50 起跳）
2. **Key 用環境變數**：`export ANTHROPIC_API_KEY="..."`，不要寫進 code
3. **`.env` 加 `.gitignore`**，不要 commit
4. **AgentZ Ch 8 教 cost observability**，Ch 15 教 cost cap — 上 production 前必看
5. **共用機器**：別用 `~/.bashrc` 存 key，用 1Password / pass / macOS Keychain
6. **不放 GitHub**：trufflehog scan 你的 repo，外洩立刻 rotate
7. **AgentZ V3 案例**：內建 `ProviderKeyVault` + cost cap + audit trail — Ch 15 starter code 直接 copy

---

## 相關章節

- [Ch 0 把工具裝好](./chapters/ch00_setup/) — 環境變數 / API key 設定
- [Ch 1 LLM 是什麼](./chapters/ch01_llm_basics/) — 模型運作原理
- [Ch 4 CLI Agent 入門](./chapters/ch04_cli_agents/) — Claude Code 上手
- [Ch 8 Cost 觀測 / 介入](./chapters/ch08_cost_observability/) — 觀測花費
- [Ch 11 框架比較](./chapters/ch11_frameworks/) — 多模型 / 多框架對照
- [Ch 13 Memory & RAG](./chapters/ch13_memory_rag/) — TAIDE / Ollama 整合
- [Ch 15 Deploy + audit + replay + cost cap](./chapters/ch15_deploy_audit_replay/) — V3 governance
- [名詞表](./glossary) — 專業詞彙速查

---

> **價格更新提醒**：本頁價格參考各家 2026-05 公告。各家會隨時調整，正式採購前請去 official pricing 頁面確認最新數字。
