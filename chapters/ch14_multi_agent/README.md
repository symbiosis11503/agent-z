# Ch 14 — Multi-Agent 系統

> **75-90 分鐘**。讀完你會懂：multi-agent 三大架構（Pipeline / Supervisor / Blackboard）、handoff 機制、什麼時候用 multi-agent / 什麼時候單 agent 比較好。
>
> 動手練習：用三種架構寫同一個 task（research → write → review），對比。
>
> 前置：完成 [Ch 13](../ch13_memory_rag/) — 你的 agent 有 memory 了。
>
> 🛠 **Starter code**: [`starter-code/ch14_multi_agent/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch14_multi_agent) — Pipeline / Supervisor / Blackboard **三架構同任務對照**（同一 research → write → review task 在 3 種架構下實作）。

---

## 1. 為什麼 multi-agent？

單 agent 能解的問題就**不要**用 multi-agent。但有些場景單 agent 笨：

- **角色分工**：研究 agent 跟寫作 agent 用不同 system prompt，混在一起 prompt 太大
- **權限隔離**：HR agent 看薪資資料 / 客服 agent 不能看薪資 — 工具權限要分
- **效率**：3 個 agent 並行查 3 件事，比 1 個 agent 序列快
- **可重用**：「翻譯 agent」可以被多個高階 agent 引用

陷阱：**多數新手過度用 multi-agent**——把可以 prompt 解的事拆 5 個 agent，debug 變難。

---

## 2. 三大架構

### 2.1 Pipeline（流水線）

最簡單。A 做完 → B 做完 → C 做完。

```
researcher → writer → reviewer → output
```

```python
def pipeline(task):
    research = researcher.run(task)
    draft = writer.run(f"Research:\n{research}\n\nTask: {task}")
    final = reviewer.run(f"Draft:\n{draft}\n\nReview it.")
    return final
```

優點：**簡單、結構清楚**。
缺點：每階段失敗 = 整條流水線失敗、沒辦法 adapt。

### 2.2 Supervisor（主管 + 部屬）

一個 supervisor agent 看任務、決定派給哪個 worker、收結果決定下一步。

```
                ┌──────────────────┐
                │ Supervisor       │
                │ (router LLM)     │
                └─────┬────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  ┌────────┐    ┌────────┐    ┌────────┐
  │Research│    │Writer  │    │Reviewer│
  └────────┘    └────────┘    └────────┘
```

```python
WORKERS = {
    "research": researcher,
    "write": writer,
    "review": reviewer,
}

SUPERVISOR_SYSTEM = """
你是 supervisor。看任務 / 目前狀態，決定下一步派給哪個 worker 或結束。
回傳 JSON: {"next_action": "research|write|review|done", "instruction": "...", "final_answer": "..."}
"""

def supervisor_loop(task, max_iter=10):
    state = {"task": task, "results": {}}
    for _ in range(max_iter):
        decision = supervisor.run_json(state)
        if decision["next_action"] == "done":
            return decision["final_answer"]
        worker = WORKERS[decision["next_action"]]
        result = worker.run(decision["instruction"])
        state["results"][decision["next_action"]] = result
    return "(max iter reached)"
```

優點：**靈活、能 adapt**。
缺點：supervisor 跑很多 LLM call、貴。

### 2.3 Blackboard（黑板）

所有 agent 共讀共寫一個共享 state（黑板），各自看到「目前進度」決定要不要動手。

適合複雜任務有多個獨立面向，例如 RPG 遊戲裡的 NPC、多 agent simulation。

```python
class Blackboard:
    def __init__(self):
        self.state = {}
        self.subscribers = []

    def write(self, key, value):
        self.state[key] = value
        for sub in self.subscribers:
            sub.notify(key, value)
```

實務上少用，除非你做 simulation / 多 agent game。**生產 90% 場景用 Pipeline 或 Supervisor**。

---

## 3. Handoff 機制

當一個 agent 認為「這事我做不來、應該轉給另一個 agent」——這叫 **handoff**。

最乾淨的實作：把 handoff 當成**特殊 tool**。

```python
@tool
def handoff_to_specialist(reason: str, context: str) -> str:
    """Hand off to a specialist agent when current task exceeds your scope."""
    specialist_result = specialist_agent.run(f"Reason: {reason}\nContext: {context}")
    return specialist_result
```

LLM 看到「這超出我能力」就 call `handoff_to_specialist`，整個流程像 ReAct 一樣自然。

---

## 4. 共享 memory

multi-agent 共享資訊有 3 種方式：

### 4.1 透過 message（state passing）
每個 agent 結果寫進 state dict、下個 agent 從 state 讀。最常用。

### 4.2 透過 shared vector store
所有 agent 都連同一個 vector DB 寫讀。複雜對話歷史用這個。

### 4.3 透過 shared SQL / Redis
結構化資料（usage stats / state machine）用 Redis hash。

---

## 5. 何時用 / 何時不用 multi-agent

### 該用 multi-agent
- 不同 agent 用**不同模型**（cheap haiku 跑分類 + opus 跑寫作）
- 角色要**權限隔離**
- 任務有**清晰的階段**（research → write → review）
- 你想**parallel** 跑獨立子任務
- 學術研究 / multi-agent simulation

### 不該用 multi-agent
- 單 agent + system prompt 角色切換能解
- 任務沒清楚階段（每階段都動態）
- 你不想 debug 跨 agent 的 trace
- production 早期（先單 agent 跑起來再考慮拆）

---

## 6. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 5 — Handoffs**：handoff / agent-to-agent transfer / state passing

---

## 7. 動手練習

### 練習 14.1：三種架構同一任務

任務：「研究 OpenAI 跟 Anthropic 最新發表 → 寫一篇 300 字繁中比較 → review 修錯字」。

寫 3 版：
- `pipeline.py`
- `supervisor.py`
- `handoff.py`（單 agent + handoff tool）

對比：
| 架構 | LLM call | latency | token | 答案品質 | debug 難度 |
|---|---|---|---|---|---|
| Pipeline | | | | | |
| Supervisor | | | | | |
| Handoff | | | | | |

**成功標準**：表格填齊、你能說出哪種適合此任務。

### 練習 14.2：權限隔離

寫一個 HR agent（看薪資 DB）+ 一個客服 agent（看客戶資料）。Supervisor 收到「某員工的薪資」要派給 HR agent；「客戶 X 的問題」派給客服。

故意問「客戶 X 的薪資多少」——確認 HR agent 拒絕（沒這資料）/ 客服拒絕（沒權限）。

**成功標準**：跨域問題正確拒絕。

### 練習 14.3：跑 CrewAI / LangGraph multi-agent

用 [Ch 11](../ch11_frameworks/) 學過的 framework 把 14.1 重做一遍。對比 raw multi-agent vs framework 版本。

**成功標準**：跑得起來，能說出 framework 多做了什麼。

---

## 8. 你做完這一章後 ✅

- [ ] 知道 Pipeline / Supervisor / Blackboard 三架構
- [ ] 看過 supervisor 的 router prompt 怎麼寫
- [ ] 知道 handoff 當作 tool 的實作
- [ ] 知道 3 種共享 memory 方式
- [ ] 知道何時用 / 何時不用 multi-agent
- [ ] 跑完練習 14.1 / 14.2 / 14.3

打勾 5 個以上，進 [Ch 15 — Deploy + audit + replay（V3 case study）](../ch15_deploy_audit_replay/)。

---

## 8a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **過度 multi-agent** | 簡單任務拆 5 agent debug 變難 | prompt 能解就別拆；只在「角色 / 權限 / 並行 / 重用」場景才用 |
| **Supervisor 自己做事** | supervisor 直接寫文章不派 worker | system prompt 寫死「不能自己做、只能 delegate」 |
| **Pipeline 無 retry** | stage 失敗整條斷 | 每階段 try/except + retry 1 次再 fail-out |
| **Handoff 訊息太大** | agent A 傳給 B 50K token 含全 history | 抽 summary 而不是傳原文 |
| **deadlock**（blackboard）| agent 互等對方先動 | 設輪流順序或 round-robin、不靠「誰先說話」 |
| **共享 state 競態** | multi-agent 同寫一個 dict | 用 lock 或 single-writer pattern |
| **role 訊息混用** | researcher 收到 writer 的 prompt | 嚴格隔離 system prompt 跟 context, 不要 leak |
| **cost 爆炸** | 4 agent 平行 + Sonnet 燒 $1/run | summarizer 用 Haiku、final 才用 Sonnet/Opus |
| **沒 trace** | 出錯找不到誰漏掉 | 每 agent call 寫 step trace（[Ch 15 audit](../ch15_deploy_audit_replay/)）|
| **JSON 解析失敗** | supervisor 回非 JSON | system prompt 強制 + parse fail fallback to 「ask user」 |

---

## 8b. 在這頁練 Supervisor router prompt

Supervisor 架構（§2.2）最關鍵是 router prompt。試這個：

<LLMTryout
  title="Ch 14 in-page tryout — Supervisor router"
  defaultSystem="你是 supervisor，看任務 + 目前狀態，決定派給哪個 worker 或結束。回 JSON 格式 {next_action: 'research'|'write'|'review'|'done', instruction: '...', final_answer?: '...'}。當前已有 workers: research / write / review。回應只能是 JSON，不要寫其他字。"
  defaultPrompt="任務：寫一篇 200 字「2026 年 5 月 AI Agent 框架比較」短文。目前狀態：尚未開始。下一步派誰？" />

## 9. 補充閱讀

- [Anthropic — Multi-agent system design](https://www.anthropic.com/engineering/multi-agent-research-system)
- [LangGraph — Multi-agent supervisor](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
- [AutoGen 文件](https://microsoft.github.io/autogen/)
- [MetaGPT paper](https://arxiv.org/abs/2308.00352)
- `datawhalechina/hugging-multi-agent`（1.4K⭐）— MetaGPT 中文教程
- ai-dict Handoffs 段
