---
title: Ch 3 — 什麼是 Agent
description: Tool use 怎麼運作 / ReAct (Reason + Act) 循環 / Agent vs LLM vs ChatGPT 關鍵差別 / 為什麼需要 agent harness。
---

# Ch 3 — 什麼是 Agent（工具呼叫 / ReAct / 為何需要）

> **45-60 分鐘**。讀完你會懂：tool use 機制、ReAct 循環、為何需要 agent、什麼時候**不**該用 agent。
>
> 動手練習：手寫追蹤一個 agent loop、讀真實 agent JSON trace、判斷 decision point。
>
> 前置：完成 [Ch 2](../ch02_prompt/) — 已經會寫 system prompt + 結構化輸出。

---

## 1. Agent = LLM + 工具 + 循環

回到 [Ch-1](../ch-1_zero_basics/) 的定義：

```
LLM = 給文字、預測下一個 token
Agent = LLM + 工具 + 「下一步做什麼」的循環
```

光是 LLM 能做：寫詩、聊天、翻譯、解題。
**不能做**：查最新天氣、訂機票、改你電腦的檔案。

為什麼不能？因為 LLM 只是文字機器——它不能伸手「打開瀏覽器」、「跑指令」、「寄信」。

**Agent 加了三樣東西**：
1. **工具**（一組外部函式：搜尋 / 計算 / 寄信 / 改檔案 / 呼叫 API）
2. **工具呼叫機制**（讓 LLM 能「請求」呼叫某個工具）
3. **循環**（LLM 呼叫工具 → 看結果 → 決定下一步 → 再呼叫 / 結束）

---

## 2. Tool Use：LLM 怎麼呼叫工具？

關鍵動作：LLM **不會真的執行**工具。它**生成一段「我想呼叫這個工具」的 JSON**，由外部程式（agent harness）真的執行，把結果塞回去給 LLM。

### 概念流程

```
1. 你（user）告訴 agent：「查台北現在天氣」
2. Agent 把工具清單（例如 search / get_weather）連同 user 訊息一起送給 LLM
3. LLM 回：「我要呼叫 get_weather(city='Taipei')」（這是 JSON，不是真的執行）
4. Agent harness 看到 LLM 想呼叫工具，真的去打 weather API
5. Agent harness 把結果 {"temp": 26, "desc": "晴"} 塞回給 LLM
6. LLM 看到結果，回給你：「台北現在 26 度、晴天」
```

第 3 步生成的 JSON 在 API 裡叫 **tool_use block**。

### Anthropic 真實格式

`client.messages.create(...)` 的 response：

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "我來查一下天氣。"
    },
    {
      "type": "tool_use",
      "id": "toolu_01ABC",
      "name": "get_weather",
      "input": {"city": "Taipei"}
    }
  ],
  "stop_reason": "tool_use"
}
```

注意 `stop_reason: tool_use`——告訴你 LLM 暫停了、要你執行工具再回來。

你的程式收到後：
1. 看到 `tool_use` block
2. 真的執行 `get_weather(city="Taipei")` → 拿到 `{"temp": 26, ...}`
3. 把結果包成 `tool_result` 訊息塞回去：
   ```python
   messages.append({
       "role": "user",
       "content": [{
           "type": "tool_result",
           "tool_use_id": "toolu_01ABC",
           "content": '{"temp": 26, "desc": "晴"}'
       }]
   })
   ```
4. 再 call `messages.create(...)`，LLM 看到結果就會回最終答案。

---

## 3. ReAct：Reason + Act 循環

2022 年 Yao et al. 的論文 [ReAct](https://arxiv.org/abs/2210.03629) 把 agent 的循環抽象成兩個動作：

```
Reason  → LLM 想：「為了完成目標，我下一步該做什麼？」
Act     → LLM 呼叫一個工具
Observe → 工具回傳結果
Reason  → LLM 想：「結果讓我前進了嗎？還需要做什麼？」
Act     → 再呼叫工具 / 給最終答案
...
```

### 視覺化

```
┌─────────────────────────────────────────┐
│  Agent Loop                              │
│                                          │
│   User goal                              │
│      │                                   │
│      ▼                                   │
│   ┌─────────────┐                       │
│   │  Reason     │ ← LLM 想下一步         │
│   └──────┬──────┘                       │
│          │                              │
│          ▼                              │
│   ┌─────────────┐                       │
│   │  Act        │ ← 呼叫工具            │
│   └──────┬──────┘                       │
│          │                              │
│          ▼                              │
│   ┌─────────────┐                       │
│   │  Observe    │ ← 看結果              │
│   └──────┬──────┘                       │
│          │                              │
│       夠了嗎？                          │
│      ┌───┴───┐                          │
│      │       │                          │
│     是        否 → 回 Reason             │
│      │                                  │
│      ▼                                  │
│   Final answer                          │
└─────────────────────────────────────────┘
```

### 為什麼叫 Reason + Act？

論文發現：**讓 LLM 明確「先想再做」比「直接做」效果好很多**。Reason 步驟讓 LLM 內化「為什麼」，避免亂呼叫工具。

現代 agent harness（Claude Code / Codex / OpenCode）都是 ReAct 的變體，再加上：
- **多工具並行**
- **工具回傳後再次 reason**（不是固定模板）
- **stop condition**（什麼時候 LLM 決定「夠了，給答案」）

---

## 4. 為什麼需要 Agent？什麼時候**不**該用？

### 需要 Agent 的情境

1. **需要最新資訊**（LLM 訓練資料截止後的事 → 用 search tool）
2. **需要存取私人資料**（你 Notion / 電腦 / 公司 DB → 用 MCP server）
3. **需要執行動作**（寄信 / 改檔案 / 跑 SQL → 用對應工具）
4. **多步驟流程**（複雜任務需要好幾步推理 + 工具呼叫）
5. **長時間任務**（agent 自己跑、你不在旁邊監督）

### **不**該用 Agent 的情境

⚠️ 這節很重要，多數新手會 over-agent。

1. **單純 Q&A** — 如果 ChatGPT 一句話能答，**別用 agent**。多工具 + 多輪呼叫 = 多 token = 多錢 + 多慢。
2. **固定 workflow** — 如果流程確定不變（「先翻譯，再加標題」），寫死 pipeline 比 agent 可靠。
3. **延遲敏感** — agent 動輒 5-30 秒（多輪 LLM call）。即時聊天場景不適合。
4. **成本敏感 + 可預測** — 一個固定的 LLM call 你能算成本，agent 一輪你不知道會 call 幾次 LLM。
5. **安全敏感** — agent 可能呼叫不該呼叫的工具。固定 pipeline + 嚴格 input validation 更安全。

> 💡 **箴言**（[Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)）：
> 「能用 workflow 解的問題，不要用 agent。能用單一 LLM call 解的問題，不要用 workflow。」

---

## 5. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 3 — Tools & Environments**：tools / environments / sandboxing
- **Section 7 — Work Modes**：human-in-the-loop / AFK execution

---

## 6. 動手練習

### 練習 3.1：手寫追蹤一個 agent loop

不用打開電腦。在紙上或備忘錄裡，**手寫**一個 agent 處理下列任務的步驟：

**任務**：「找出 2026 年 5 月台北最便宜的飛東京機票」

請畫出 agent 會呼叫哪些工具、每步 reason 是什麼、observe 看到什麼、什麼時候停。

格式範例：
```
Round 1:
  Reason: 我需要查機票，要用 search 工具
  Act: search("台北 東京 機票 2026 5 月")
  Observe: [搜尋結果摘要]

Round 2:
  Reason: 我有 3 個網站，要選便宜的、進去看細節
  Act: open_url("...")
  Observe: ...

...

Round N:
  Reason: 我比較完了，回給使用者
  Act: 直接回答（不呼叫工具）
```

**成功標準**：你能畫出 4 個以上 round，每個 round 有清楚的 Reason / Act / Observe。

### 練習 3.2：讀真實 Agent JSON trace

複製這段 Python 跑一次，**仔細讀 print 出的訊息陣列**：

```python
import os, json
import anthropic

client = anthropic.Anthropic()

tools = [{
    "name": "calc",
    "description": "Calculate a math expression. Input: {expr: '3*4'}",
    "input_schema": {
        "type": "object",
        "properties": {"expr": {"type": "string"}},
        "required": ["expr"]
    }
}]

messages = [{"role": "user", "content": "幫我算 (17*23)+(89*7)。用 calc 工具。"}]

while True:
    r = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        tools=tools,
        messages=messages,
    )
    print(f"--- assistant ---\n{json.dumps([c.model_dump() for c in r.content], ensure_ascii=False, indent=2)}\n")
    messages.append({"role": "assistant", "content": r.content})

    if r.stop_reason != "tool_use":
        break

    # 找 tool_use 並執行
    tool_results = []
    for block in r.content:
        if block.type == "tool_use" and block.name == "calc":
            try:
                result = eval(block.input["expr"])  # 教學範例用 eval；產品請用 ast.literal_eval
            except Exception as e:
                result = f"ERROR: {e}"
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
            })
            print(f"--- tool result (id={block.id}): {result} ---\n")
    messages.append({"role": "user", "content": tool_results})

print(f"=== Final answer ===\n{r.content[0].text if r.content else '(empty)'}")
```

**任務**：讀完 trace 後，回答：
1. LLM 一共 call 了幾次 `calc` 工具？
2. 每一次的 `expr` 是什麼？
3. LLM 為什麼最後選擇停？

**成功標準**：3 題都答對。

### 練習 3.3：決定要不要用 agent

下列 5 個任務，判斷「該用 agent」還是「不該用」，並寫一句理由：

1. 「翻譯這段英文成繁中」
2. 「找出我 Notion 裡所有跟『會議』相關的頁面，整理成表」
3. 「每天早上 8 點查一次股票價格、超過 X 元就寄信給我」
4. 「寫一首中秋節的詩」
5. 「分析我這個月信用卡帳單，找出最大 3 筆異常支出」

**成功標準**：判斷正確 + 理由講得清楚（哪些工具 / 為什麼不需要）。

> 參考答案在下一節（先自己想）：
> 1. 不該（單純翻譯，一個 LLM call 解）
> 2. 該（需要 Notion 工具 + 多筆查詢 + 整理）
> 3. 該（多步驟 + 跨服務工具 + 條件判斷）
> 4. 不該（純創作，一個 LLM call 解）
> 5. 該（需要工具讀帳單 + 計算統計 + 異常判斷）

---

## 7. 你做完這一章後 ✅

- [ ] 知道 Agent = LLM + 工具 + 循環
- [ ] 看到 tool_use JSON 不會嚇到
- [ ] 知道 ReAct 是什麼、為什麼有用
- [ ] 知道 5 個「不該用 agent」的情境
- [ ] 跑完練習 3.1 / 3.2 / 3.3
- [ ] 看完練習 3.2 的 trace，**能跟人解釋它在做什麼**

打勾 5 個以上，恭喜——你完成了 **Watcher 階段**！下一章進 **Operator** 階段，開始裝 CLI agent。

---

## 7a. 常見地雷（agent 概念誤區）

| 地雷 | 真相 |
|---|---|
| **Agent 完全自主** | 應該人類 in-the-loop, 關鍵決策 (付錢/寄信/改 prod) 必確認 |
| **Agent = AGI** | 不是。Agent 只是 LLM + 工具 + 循環, 沒意識也不主動 |
| **越多 agent 越好** | 多 agent 引入 coordination overhead。簡單任務單 agent |
| **agent 不會錯** | hallucinate / cost 失控 / loop 不停 / reward hacking 都會 |
| **ReAct 是唯一範式** | 還有 Plan-and-Solve / Reflection / CodeAct / Multi-agent ([Ch 10](../ch10_react_paradigms/) / [Ch 14](../ch14_multi_agent/)) |
| **所有 task 都該 agentize** | task 結構化、可重複、用 script 解就好。Agent 適合「需要判斷 + 工具切換」的 |
| **沒 governance 也能 ship** | Production agent 必有 cost cap / audit / replay ([Ch 8](../ch08_cost_observability/) / [Ch 15](../ch15_deploy_audit_replay/)) |
| **越大 model 越好** | 簡單 routing 用 Haiku、複雜推理才 Opus |

---

## 7b. 在這頁直接看 LLM 怎麼描述自己會做的事

LLM 雖然不會真的 call 工具（這頁沒接 tool），但你可以叫它**模擬**一次 agent 思路。

<LLMTryout
  title="Ch 3 in-page tryout — 模擬 ReAct 思路"
  defaultSystem="你是 agent ReAct simulator。看任務，模擬出 Reason / Act / Observe 循環。每輪 4-6 句，最多 5 輪。Act 寫成偽工具呼叫（不真的執行）。"
  defaultPrompt="任務：找出台北現在的天氣 + 推薦穿什麼出門。" />

## 8. 補充閱讀

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — 必讀；什麼時候用 agent、什麼時候不用
- [ReAct paper（原文）](https://arxiv.org/abs/2210.03629)
- ai-dict Tools & Environments 段：https://ai-dict.gh.miniasp.com/
- 後面 Ch 10 會手把手帶你寫一次 ReAct loop，現在只要理解概念

---

## Watcher 階段（Ch 1-3）回顧

你現在會什麼：
- LLM 是「下一個 token 預測器」
- 知道 token / context / role / temperature / pricing
- 寫 system prompt 有 4 欄位框架
- 知道 Agent = LLM + 工具 + 循環
- 看到 tool_use JSON / agent trace 看得懂

下一階段（Operator）：實際用 CLI agent 把日常工作做完。從 [Ch 4 — CLI Agent 入門](../ch04_cli_agents/) 開始。
