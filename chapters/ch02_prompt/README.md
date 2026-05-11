# Ch 2 — Prompt 設計

> **45-60 分鐘**。讀完你會懂：system prompt 怎麼寫 / few-shot / Chain-of-Thought / 結構化輸出 / 5 個 prompt 通病怎麼修。
>
> 動手練習：把一個爛 prompt 改成好 prompt，量化答案品質提升。
>
> 前置：完成 [Ch 1](../ch01_llm_basics/) — 已經會 system/user/assistant role。

---

## 1. Prompt 是 LLM 的 specification（不是請求）

新手最常見的錯誤：把 prompt 當「跟人講話」。

**LLM 不是人**——它是「下一個 token 預測器」。你給它的 prompt 是**完整 specification**，包含：
- **背景**（你是誰、要做什麼）
- **角色**（LLM 扮演什麼）
- **約束**（什麼能做、什麼不能）
- **輸出格式**（要 markdown、JSON、純文字、條列）
- **範例**（理想答案長什麼樣）

少任何一塊，LLM 就會「自己腦補」——然後你拿到不想要的答案。

---

## 2. System prompt 的 4 個欄位

寫 system prompt 時，**心裡固定跑這 4 個欄位**：

### 2.1 角色（Role）

```
你是一個專業的繁中技術文件翻譯助理。
```

不寫角色 → LLM 會用 default「helpful assistant」聲音，常常太籠統或太禮貌。

### 2.2 約束（Constraints）

```
- 只回繁中。如果使用者用其他語言問你，回「請用繁中問」並停止。
- 不解釋技術名詞，除非使用者明問。
- 翻譯時保留原文的程式碼區塊不動。
```

不寫約束 → LLM 會自由發揮、加很多它覺得「貼心」的東西。

### 2.3 輸出格式（Output format）

```
回答時用以下格式：
1. 直接翻譯結果（繁中）
2. 如果有意譯，列出原文跟翻譯的對照
```

不寫格式 → 每次答案結構都不同，下游程式接不住。

### 2.4 範例（Examples，可選）

```
範例：
使用者：Translate: API key
你：API 金鑰
```

不舉例 → LLM 對「你想要的長相」靠猜。給 1-3 個範例（**few-shot**）通常品質大幅提升。

---

## 3. Few-shot vs Zero-shot

- **Zero-shot**：完全沒範例，只下指令。
- **Few-shot**：在 prompt 裡塞 1-N 個示範。

什麼時候用？

| 任務類型 | 推薦 |
|---|---|
| 翻譯 / 結構化輸出 / 分類 | few-shot（1-3 個範例就大幅變好） |
| 開放性問題（寫作 / 諮詢 / 解釋） | zero-shot 通常夠 |
| 你不確定 LLM 會不會做的事 | 一定要 few-shot 先測一次 |

> 💡 **few-shot 不一定要塞在 system prompt**。也可以塞在 user 訊息頭部，或用 `assistant` 訊息真實演示前一輪互動。

---

## 4. Chain-of-Thought（CoT）

要 LLM **先想再答**，答案品質常常飆升——尤其是要算數、邏輯推理、多步驟分析的任務。

兩個寫法：

### 寫法 A：明示要求「先想」

```
解答時，請先用 <thinking> 標籤把思路寫出來，再用 <answer> 標籤給答案。

範例：
使用者：13 * 27 = ?
你：
<thinking>
13 * 27 = 13 * (25 + 2) = 13*25 + 13*2 = 325 + 26 = 351
</thinking>
<answer>351</answer>
```

### 寫法 B：用「let's think step by step」魔法句

這句話 2022 年發現的，把它加在 prompt 結尾，LLM 答案就會變好。原因是訓練資料裡這句話後面常接「step 1...step 2...」的推理。

```python
messages=[
    {"role": "user", "content": f"{question}\n\nLet's think step by step. 用繁中思考。"}
]
```

> 💡 **現代 reasoning model**（Claude / GPT-4o / Gemini thinking 系列、DeepSeek-R1）有內建 thinking，不用你手動加 CoT。但對 Haiku / Mini 等小 model 仍然有效。

---

## 5. 結構化輸出：要 JSON 就要對

> 如果你下游程式要 parse LLM 的答案（不是給人看），絕對不要靠運氣

### 三個層次

**A. Prompt 裡要求 JSON（最弱）**
```
回答時只回 JSON，格式 {"answer": str, "confidence": float}
```
LLM 會「常常」回對的 JSON，但偶爾會多一段「Here's your JSON:」前綴——下游 parse 死。

**B. 用 JSON mode（中等）**
OpenAI / Anthropic 都有 `response_format="json_object"` 的 flag，**強制** LLM 只能輸出合法 JSON。

```python
client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[...]
)
```

**C. 用 tool use 的 input schema（最強）**
Anthropic / OpenAI 都支援用 JSON Schema 定義 tool 的 input。當你只是要結構化輸出時，**用一個假 tool 強制 LLM 填**：

```python
# 用 Anthropic tools 做結構化輸出
tools=[{
    "name": "report_translation",
    "description": "Report the translation result.",
    "input_schema": {
        "type": "object",
        "properties": {
            "translated": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["translated", "confidence"]
    }
}]
```

LLM 會自動回一個 tool_use block，input 100% 對齊 schema——這是**目前最可靠的結構化輸出方式**。

---

## 6. 5 個 prompt 通病

### 病 1：太籠統
❌ 「幫我寫一個 API」
✅ 「用 FastAPI 寫一個 `/v1/users` GET endpoint，回 JSON list of {id, name, email}。不要寫 auth。直接給 code，不解釋。」

### 病 2：自相矛盾
❌ 「簡短回答，但要詳細解釋每個步驟」（你到底要短還要長？）
✅ 「最多 100 字。如果使用者要更多細節，請他追問。」

### 病 3：沒講想要的格式
❌ 「告訴我 Python 跟 JS 的差別」
✅ 「用 markdown 表格列出 Python 跟 JS 在這 5 個維度的差別：型別系統 / 並發模型 / 包管理 / 部署 / 生態系」

### 病 4：用否定句
LLM 對「不要做 X」比「要做 Y」差。
❌ 「不要解釋」
✅ 「直接給結論，省略推理過程」

### 病 5：把工作丟給 LLM 想
❌ 「請給我最好的建議」
✅ 「請從下列 3 個選項挑 1 個，用 100 字說明選擇理由：A. ... B. ... C. ...」

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 2 — Sessions, Context Windows & Turns**：context window / turns / message roles
- **Section 1 — Models**：tokens / parameters

---

## 8. 動手練習

### 練習 2.1：把爛 prompt 改成好 prompt

下面這個 prompt 至少有 4 個通病，請改寫：

```
告訴我 Python 怎麼學，要詳細但簡短，最好不要太多範例但要有範例，給我點建議。
```

**成功標準**：你的新版必須
1. 明確角色
2. 明確約束（學什麼程度？花多久？）
3. 明確輸出格式（步驟？表格？對話？）
4. 沒有自相矛盾
5. 用同樣的 model 跑舊版跟新版，比較答案品質

### 練習 2.2：強制 JSON 結構化輸出

寫一個 prompt 讓 Claude **每次都**回這個結構，零容錯：

```json
{
  "language": "zh-TW" | "en" | "ja",
  "translated": "string",
  "confidence": 0.0 - 1.0,
  "ambiguities": ["string", ...]
}
```

用上 §5 的方法 C（tool use schema）。連跑 10 次，**每次都要合法 JSON**。

**成功標準**：10/10 valid JSON parse 成功。

### 練習 2.3：CoT 對比

問同一個邏輯題（自選，例如「一個房間有 3 個開關控制 3 顆燈泡，你只能進房間一次，怎麼判斷哪個開關對哪顆燈？」）給 Claude Haiku：
1. 不加 CoT：直接問
2. 加 "Let's think step by step. 用繁中思考。" 結尾

比較兩個答案。**多數情況下，加 CoT 的答案會明顯較對**。

**成功標準**：你能說出兩個答案的差別在哪。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 prompt 是 specification 不是請求
- [ ] 寫 system prompt 會自動跑「角色 / 約束 / 格式 / 範例」4 欄位
- [ ] 知道什麼時候用 few-shot
- [ ] 會用 CoT
- [ ] 知道 3 層結構化輸出（prompt / JSON mode / tool schema）哪個最可靠
- [ ] 看到 prompt 能抓出 5 個通病
- [ ] 跑完練習 2.1 / 2.2 / 2.3

打勾 5 個以上，進 [Ch 3 — 什麼是 Agent](../ch03_what_is_agent/)。

---

## 9a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **system / user 用混** | LLM 不分指示跟內容 | system = 角色 + 規則 / user = 具體請求 + 資料 |
| **prompt 太籠統** | 答案飄忽不一致 | 明確「輸出格式 / 字數限制 / 語氣 / 邊界」 |
| **沒給 example** | 結構出不來 | few-shot 1-3 個範例，遠勝 100 字解釋 |
| **negative instruction 不寫 positive** | LLM 還是做了 | 寫「請做 X」比「不要做 Y」有效 |
| **指令矛盾** | LLM 隨意挑一個 | 同 prompt 內規則 audit、矛盾的拆兩段 |
| **CoT 卻禁推理** | 「直接回答不解釋」+「step by step」同時 | 想要推理就允許輸出 thought、要簡潔就 final-only |
| **不留 escape hatch** | LLM 編答案 | 加「不知道請說『無法判斷』」 |
| **prompt 撞 200K** | LLM 「忘」前面 | summarize 歷史；用滑動窗口；structured prompt |
| **每次 prompt 重寫** | 同 task 結果飄 | 寫成 SKILL 或 prompt template 鎖版 |
| **prompt injection** | user 輸入「忽略上面」LLM 真就忽略 | system 強調權限、user 輸入用 `<user_input>` 包起來 |

---

## 9b. 在這頁直接練 prompt

改 system prompt + user prompt、按送出看結果。多試幾次你會學到 prompt 寫法。

<LLMTryout
  title="Ch 2 in-page tryout — 改 system prompt 看差別"
  defaultSystem="你是繁中翻譯助理。只翻譯，不解釋。如果使用者用非英文發訊息，請回「請給英文」並停止。"
  defaultPrompt="Translate: API key" />

## 10. 補充閱讀

- [Anthropic — Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [OpenAI — Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering)
- `anthropics/prompt-eng-interactive-tutorial`（GitHub，35K⭐）— Anthropic 互動式 tutorial
- ai-dict 繁中：https://ai-dict.gh.miniasp.com/
