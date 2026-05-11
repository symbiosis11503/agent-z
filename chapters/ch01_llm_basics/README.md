# Ch 1 — LLM 是什麼

> **45-60 分鐘**。讀完你會懂：token / context window / role / temperature / 各家 LLM 怎麼選。
>
> 動手練習：跑同一個問題在 3 家 LLM、算 token 成本、選對 model。
>
> 前置：完成 [Ch 0](../ch00_setup/) — 已經跑過 Hello-World。

---

## 1. LLM 不是「在思考」，是「在預測下一個 token」

LLM = Large Language Model = 大型語言模型。

它的核心動作只有一個：**給定一段文字，預測下一個 token 最可能是什麼**。

```
輸入：「今天天氣真_」
LLM 看到後，內部算出機率：
  「好」  → 45%
  「不錯」 → 22%
  「冷」   → 12%
  「熱」   → 9%
  ...其他...

LLM 挑機率最高的「好」，吐出來。
然後把「今天天氣真好」再丟回去，預測下一個 token。
重複，直到它認為這段該停了。
```

就這樣。**沒有理解、沒有意識、沒有思考**——只是統計學意義上的「下一個 token 該是什麼」。

但因為它訓練時看過幾兆 token 的文本，這個「最可能的下一個 token」結果**非常像**人類在思考。這是為什麼 LLM 能聊天、能寫程式、能總結文章——它在模仿訓練資料裡的人類書寫模式。

> 💡 **這個 mental model 很重要**。你後面卡關時（例如「為什麼 LLM 會 hallucinate？」「為什麼它有時答得很好有時很爛？」），答案幾乎都從「它只是在預測下一個 token」推得出來。

---

## 2. Token 是什麼

**Token** = LLM 看世界的最小單位。**不是字元、不是單詞**。

英文：
- `hello` → 1 token
- `Hello, world!` → 4 tokens（`Hello` / `,` / ` world` / `!`）
- `antidisestablishmentarianism` → 6 tokens（被切分）

中文：
- `你好` → 通常 1-2 tokens（看 model）
- `今天天氣真好` → 通常 4-7 tokens
- 平均**一個中文字 ≈ 1.5 token**（粗估）

每家 model 用自己的 **tokenizer** 切，所以同一段文字在 Claude 跟 GPT 算出來的 token 數會略不同。

### 為什麼要在乎 token？

**因為 token = 錢**。API 按 token 計費，分輸入跟輸出兩部分：

| Model（2026 Q1） | 輸入 / 1M token | 輸出 / 1M token |
|---|---|---|
| Claude Haiku 4.5 | $0.80 | $4.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Opus 4.7 | $15.00 | $75.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4o | $2.50 | $10.00 |
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Groq Llama-3.3-70B | 免費（限速） | 免費（限速） |

> 數字會變、請查官方 pricing。重點是**輸出 token 通常比輸入貴 3-5 倍**，所以「讓 LLM 給你短回答」比「讓 LLM 看短輸入」省更多。

### 算成本：粗估 cheatsheet

| 你給的東西 | 大概多少 token |
|---|---|
| 一段中文文章（500 字） | ~750 token |
| 整本書（10 萬字） | ~150,000 token（撐爆多數小 model context） |
| 一張人臉照片 | ~1,000-1,500 token（多模態 model 才算） |
| 1 分鐘音訊轉錄 | ~150 token |

---

## 3. Context Window：LLM 的「記憶」上限

**Context window**（或 context length）= LLM 一次最多能看的 token 數量。

| Model | Context window |
|---|---|
| Claude Haiku 4.5 / Sonnet 4.6 / Opus 4.7 | 200K（部分到 1M） |
| GPT-4o | 128K |
| GPT-4o-mini | 128K |
| Gemini 2.0 Flash | 1M |
| Groq Llama-3.3-70B | 128K |

200K token ≈ 一本中等長度的書。所以你可以把整本書貼進 prompt 讓 Claude 摘要。

### Context 不是「記憶」

⚠️ **常見誤解**：LLM 沒有「記憶」上一通對話的能力。**每次 API call 都是獨立的**——你看到 ChatGPT「記得」剛剛聊過什麼，是因為 ChatGPT 後端把整段歷史對話塞進每次 API call 的 context。

這也是為什麼**長對話會變貴**：每多一輪，前面所有的對話都要重新進 context、重新算錢。

後面 Ch 13 講 memory 系統時會回到這個。

---

## 4. Role：system / user / assistant

LLM API 不只接收一段文字，而是接收一個**訊息陣列**，每則訊息有 **role**：

| Role | 誰寫的 | 例子 |
|---|---|---|
| `system` | 你（給 LLM 的設定/規則） | 「你是個專業的繁中翻譯助理，只回繁中，不解釋」 |
| `user` | 使用者 | 「翻譯這段：Hello world」 |
| `assistant` | LLM 上一輪的回答 | 「你好世界」 |

範例（Python）：

```python
messages=[
    {"role": "system", "content": "你是個繁中翻譯助理。"},
    {"role": "user", "content": "翻譯：Hello world"},
    {"role": "assistant", "content": "你好世界"},
    {"role": "user", "content": "翻譯：Good morning"},
]
```

LLM 看到這串，會接著 `assistant` 角色回應「早安」。

> 💡 **system prompt 是 prompt 設計的核心戰場**。Ch 2 整章在講怎麼設計它。

---

## 5. Temperature：隨機性旋鈕

**Temperature**（0.0 - 1.0+）= LLM 挑下一個 token 時要不要走最高機率。

- **0.0**：永遠挑最高機率。答案最穩定、最 boring，適合**翻譯 / 結構化輸出 / 程式碼**。
- **1.0**：依機率分佈隨機抽。答案最有變化、最有創意，適合**寫作 / brainstorm / 角色扮演**。

實務上：
- 工具呼叫 / agent 決策 → `temperature=0` 或 `0.1`
- 寫文案 / 詩 → `temperature=0.7-1.0`
- 預設 → 多數 SDK default `1.0`（很多人沒意識到，所以結果不穩）

---

## 6. 各家 LLM 怎麼選？

短答案：**沒有「最好」的 model，只有「現在這個任務的對的 model」**。

### 三大 vendor

| 家 | 強項 | 弱項 | 適合 |
|---|---|---|---|
| **Anthropic（Claude）** | 長 context（200K-1M）、寫程式強、講話自然、長文細節保持好 | 比 GPT 慢一點、貴一點 | agent 主力、code 任務、長文 |
| **OpenAI（GPT）** | 生態最完整、tool use 早熟、語音/視覺等多模態深 | hallucination 偶爾較多 | 通用、多模態、speed-critical |
| **Google（Gemini）** | 1M context 最便宜、多模態、搜尋整合 | API 限速嚴、結構輸出有時不穩 | 長文 + 預算敏感 |

### 開源 model 服務商

| 服務 | 提供 model | 特色 |
|---|---|---|
| **Groq** | Llama-3.3-70B / DeepSeek-R1 / Mixtral 等 | 推論超快（>500 token/sec）、有免費 tier |
| **OpenRouter** | 全家 model 一個 API | 一個 key 跨家、cost 透明 |
| **Together AI** | Llama / Mixtral / Qwen 等 | dedicated host、企業用 |
| **DeepSeek** | DeepSeek-V3 / R1 | 中國團隊、便宜、reasoning 強 |

### 本地跑：Ollama / llama.cpp / MLX

如果你有夠強的電腦（Mac M-series unified memory >= 16GB 或 NVIDIA GPU），可以本地跑 model：

- **Ollama** — 最簡單。`ollama pull llama3.3:70b` 就裝好（如果 RAM 夠）
- **llama.cpp** — 最快的 inference 引擎
- **MLX** — Apple Silicon 專用、超快

本地 model 適合「我不想付 API、隱私敏感、或想自己 fine-tune」的情境。後面 Ch 17 會展開。

### 怎麼選的決策樹

```
你的任務是？
├─ 寫程式 / 改 code → Claude Haiku/Sonnet > GPT-4o
├─ 結構化輸出 (JSON) → 任一家、temperature=0
├─ 長文摘要 (>50K token) → Gemini 1M context > Claude 200K
├─ 通用聊天 / RAG → GPT-4o-mini / Claude Haiku（便宜）
├─ Agent 工具呼叫 → Claude Sonnet 4.6 / GPT-4o（成熟）
├─ 多模態（看圖 / 影片） → Gemini > GPT-4o > Claude
└─ 預算 = 0 → Groq 免費 tier / Gemini Flash
```

---

## 7. 動手練習

### 練習 1.1：同一問題、3 家比較

問同一個問題在 Claude / Groq / 一家你自己選的 model，比較：
- 回答風格（誰嚴謹？誰有人情味？誰啰嗦？）
- token 數（看 API response 的 `usage` 欄位）
- 速度（用 `time.time()` 算）

範例 starter（`exercises/1.1_three_providers.py`）：

```python
import os, time
import anthropic
from openai import OpenAI

QUESTION = "用繁中三句話解釋什麼是 AI Agent。"

# Anthropic Claude
t0 = time.time()
claude = anthropic.Anthropic()
r1 = claude.messages.create(
    model="claude-haiku-4-5",
    max_tokens=500,
    messages=[{"role": "user", "content": QUESTION}]
)
print(f"=== Claude Haiku 4.5 ({time.time()-t0:.1f}s, in={r1.usage.input_tokens} out={r1.usage.output_tokens})===")
print(r1.content[0].text)

# Groq Llama-3.3
t0 = time.time()
groq = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
r2 = groq.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": QUESTION}]
)
print(f"=== Groq Llama-3.3 ({time.time()-t0:.1f}s, in={r2.usage.prompt_tokens} out={r2.usage.completion_tokens})===")
print(r2.choices[0].message.content)
```

**成功標準**：三家答案在你 Terminal 並排印出，加上 token 數跟耗時。**儲存截圖**。

### 練習 1.2：算成本

用同一個 prompt（複製練習 1.1）跑 5 次，記錄總 token，**計算 5 次的總成本**。

| Model | 5 次總 in token | 5 次總 out token | 總成本（美金） |
|---|---|---|---|
| Claude Haiku 4.5 | | | |
| GPT-4o-mini | | | |
| Groq Llama-3.3 | | | 0（免費） |

**成功標準**：成本算對到小數點後 4 位（用 §2 表格的 pricing）。

### 練習 1.3：role 實驗

用 system prompt 控制 Claude 角色，**讓它拒絕回非繁中問題**：

```python
messages=[
    {"role": "system", "content": "你只回繁中。如果使用者用其他語言問你，請回「請用繁中問」並不要回答。"},
    {"role": "user", "content": "What is an AI Agent?"}
]
```

**成功標準**：Claude 應該回「請用繁中問」而不是回答原問題。

---

## 8. 你做完這一章後 ✅

- [ ] 知道 LLM 本質是「預測下一個 token」
- [ ] 知道 token / context window / role / temperature 是什麼
- [ ] 看到 pricing 表能粗估一個 task 多少錢
- [ ] 知道哪家 model 適合什麼任務
- [ ] 跑完練習 1.1（三家比較）
- [ ] 跑完練習 1.2（算成本）
- [ ] 跑完練習 1.3（system prompt 控制角色）

打勾 5 個以上，進 [Ch 2 — Prompt 設計](../ch02_prompt/)。

---

## 9. 補充閱讀

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — 什麼時候用 framework / 什麼時候用 raw API
- [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app/) — 線上看你的 prompt 被 tokenize 成什麼樣
- [Hugging Face — Tokenizers explained](https://huggingface.co/docs/tokenizers/en/index)
- 各家 pricing 官方：
  - https://www.anthropic.com/pricing
  - https://openai.com/pricing
  - https://ai.google.dev/gemini-api/docs/pricing
  - https://groq.com/pricing
