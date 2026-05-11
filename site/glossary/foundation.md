---
title: 名詞表 — 基礎概念
description: LLM / Token / Context Window / Role / Temperature / Embedding / Fine-tuning / Hallucination + Prompt / System Prompt / Few-shot / CoT / Structured Output / Compaction / Prompt Cache
---

# 名詞表 · 基礎概念

[← 回名詞表總覽](../glossary)

## 1. LLM 基礎

### 大型語言模型 / LLM (Large Language Model)
- **專業**：用 transformer 架構訓練的神經網路，目標是預測下一個 token 的條件機率分佈 $P(x_{t+1} | x_1, ..., x_t)$。參數量通常從數十億到上兆。
- **白話**：吃進文字、輸出最可能下一個字的機率機器。它不是「在思考」，是統計學意義上猜下一個字。
- **範例**：Claude / GPT-4 / Gemini / Llama 都是 LLM。當你問 ChatGPT「今天天氣」、它回答的本質是「人類在這種情境下會說什麼字最有可能」。
- **章節**：[Ch 1](../chapters/ch01_llm_basics/)

### Token / Token
- **專業**：LLM 的最小輸入單位，由 tokenizer 把字串切成的 sub-word 片段。中文約 1-2 字一個 token，英文約 4 字元一個。
- **白話**：LLM「看世界」的單位、也是收錢的單位。
- **範例**：「Hello world」= 3 token（`Hello`, ` world`, `!`）。「今天天氣真好」= 4-7 token。Anthropic Haiku 4.5 輸入 $0.80 / 百萬 token。
- **章節**：[Ch 1 §2](../chapters/ch01_llm_basics/#2-token-是什麼)

### 上下文視窗 / Context Window
- **專業**：LLM 一次推論能容納的最大 token 數。受 model 架構（attention pattern）跟 GPU 記憶體限制。
- **白話**：LLM 一次能讀的「最多多少字」。讀太多塞不下。
- **範例**：Claude 4.x 200K-1M token、GPT-4o 128K、Gemini 2.0 Flash 1M。200K token ≈ 一本中等小說。
- **章節**：[Ch 1 §3](../chapters/ch01_llm_basics/#3-context-window-llm-的-記憶-上限)

### 角色 / Role
- **專業**：API messages 陣列每則訊息的發話者標記：`system` / `user` / `assistant`（部分 model 多 `tool` / `function`）。
- **白話**：「這段話是誰講的？」系統 / 使用者 / LLM。
- **範例**：`[{role: "system", content: "你只回繁中"}, {role: "user", content: "Translate Hello"}, {role: "assistant", content: "你好"}]`。
- **章節**：[Ch 1 §4](../chapters/ch01_llm_basics/#4-role-system--user--assistant)

### 溫度 / Temperature
- **專業**：softmax 採樣機率分佈的溫度參數。溫度 0 = greedy（取最高機率）、溫度 > 1 = 越平坦（隨機）。
- **白話**：「LLM 答得有多隨興」的旋鈕。0 = 死板穩定、1 = 有創意。
- **範例**：寫合約 → 溫度 0；寫詩 → 溫度 0.8。agent 工具呼叫一定 0 或 0.1，要穩定。
- **章節**：[Ch 1 §5](../chapters/ch01_llm_basics/#5-temperature-隨機性旋鈕)

### 嵌入 / Embedding
- **專業**：把文字（or 圖 / 音）映射到固定維度的 dense vector（通常 384-3072 維），讓語意相近的東西在向量空間距離近。
- **白話**：把一段文字變成一串數字，讓電腦能算「兩段意思像不像」。
- **範例**：「貓」跟「狗」的 embedding 距離近、跟「火箭」的距離遠。RAG 全靠這個做 similarity search。
- **章節**：[Ch 13](../chapters/ch13_memory_rag/)

### 微調 / Fine-tuning
- **專業**：用 supervised / RL 訊號繼續訓練 base model 的部分或全部參數，讓它更適配特定 task / domain / 風格。
- **白話**：把現成 LLM 拿過來、餵它你自己的資料、讓它變成「你公司專用版」。
- **範例**：把 Llama-3 fine-tune 成法律 advisor、客服機器人、code reviewer。
- **章節**：[Ch 17](../chapters/ch17_builder_advanced/)

### 幻覺 / Hallucination
- **專業**：LLM 生成 plausible 但事實錯誤、無依據的內容。常見原因：訓練資料缺少、context 引導不足、temperature 高。
- **白話**：LLM 一本正經地胡說八道。
- **範例**：問「2026 年 5 月某某 paper 的作者」、它掰一個不存在的 paper 跟假作者，還給你假 DOI。Ch 16 §4 anti-hallucination 5 條規則就是治這個。
- **章節**：[Ch 16](../chapters/ch16_researcher/)

---

## 2. Prompt / Context 管理

### 提示 / Prompt
- **專業**：使用者 / 系統送給 LLM 的完整輸入文字（含 system / user / assistant 訊息 + tool 定義 + few-shot 範例）。
- **白話**：你跟 LLM 說的話。**不是 chat，是 specification**——你不寫清楚它就自己腦補。
- **範例**：「翻譯這段」=爛 prompt；「你是繁中翻譯助理。只翻譯不解釋。範例：Hello → 你好。請翻譯：Good morning」= 好 prompt。
- **章節**：[Ch 2](../chapters/ch02_prompt/)

### 系統提示 / System Prompt
- **專業**：放在 messages 陣列開頭的 `role: system` 訊息，定義 LLM 角色 / 約束 / 輸出格式。
- **白話**：給 LLM 的「使用說明書 + 性格設定」。每次對話開始它先讀。
- **範例**：`"你是繁中技術文件翻譯助理。只回繁中。不解釋技術名詞除非問你。輸出 markdown 格式。"`
- **章節**：[Ch 2 §2](../chapters/ch02_prompt/#2-system-prompt-的-4-個欄位)

### 少量範例 / Few-shot
- **專業**：在 prompt 中提供 1-N 個 input/output pair 示範，讓 LLM 從範例 in-context learn pattern。
- **白話**：給 LLM 看「我要的答案長這樣」的範本，比抽象描述有效 10x。
- **範例**：「分類情緒：『今天好開心』→ 正面 / 『下雨真煩』→ 負面 / 『等公車中』→ 中性 / 『加薪了！』→ ?」 LLM 看到範例知道輸出格式 + 標籤集合。
- **章節**：[Ch 2 §3](../chapters/ch02_prompt/#3-few-shot-vs-zero-shot)

### 思考鏈 / Chain-of-Thought (CoT)
- **專業**：透過 prompt 引導 LLM 在最終答案前先生成中間推理步驟。可顯式（`<thinking>`）或隱式（`Let's think step by step`）觸發。
- **白話**：要 LLM「先想再答」、想的過程印出來。算數 / 邏輯題效果顯著。
- **範例**：問「17 × 23」、加 "Let's think step by step" 前後答對率差 30%+。現代 reasoning model（o1 / R1 / Claude Sonnet）內建 CoT 不用你加。
- **章節**：[Ch 2 §4](../chapters/ch02_prompt/#4-chain-of-thought-cot)

### 結構化輸出 / Structured Output
- **專業**：透過 JSON mode / tool use schema / Pydantic AI 等機制，強制 LLM 輸出對齊指定 schema 的合法 JSON。
- **白話**：要 LLM 回答**只能是固定格式**，不能加廢話。下游程式好 parse。
- **範例**：要 LLM 翻譯回 `{"translated": "...", "confidence": 0.95}`、不要回「Sure, here's your translation: ...」。
- **章節**：[Ch 2 §5](../chapters/ch02_prompt/#5-結構化輸出要-json-就要對)

### 壓縮 / Compaction
- **專業**：長對話超過 context window 前，把舊 messages 摘要成短 summary 取代原文。trade off：壓縮失去細節 vs 不壓爆 context。
- **白話**：對話太長、把老的對話濃縮成「老闆說過喜歡咖啡，討論過 3 個方案」這種大綱。
- **範例**：Claude Code 內建 `/compact` 指令；自己寫 agent 在 messages.length > 20 時觸發 LLM 摘要 messages[:10]。
- **章節**：[Ch 13 §3](../chapters/ch13_memory_rag/#3-session-memory-累積--摘要)

### 提示快取 / Prompt Cache
- **專業**：在 messages / system / tools 上標 `cache_control: {type:"ephemeral"}`，相同 prefix 後續呼叫時 input cost 降至 1/10，cache TTL 1 小時（Anthropic）。
- **白話**：「同一段長 system prompt 不要每次都收滿費」。LLM 把它快取住、第二次起便宜 90%。
- **範例**：5K-token system prompt + 多輪對話：第一次寫入 1.25x cost、第二次起 0.1x cost。Ch 8 cost cap 配 cache 兩件事一起做。
- **章節**：[Ch 8 §4](../chapters/ch08_cost_observability/) + [速查卡 SDK](../cheatsheet/sdk#prompt-cache-省-90-cost)

---

**其他類別** → [基礎](./foundation) · [Agent / CLI](./agent) · [實務](./practice) · [Production](./production) · [台灣/混淆 pair](./taiwan-misc)
