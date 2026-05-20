---
title: Ch 14 — Multi-Agent 系統
description: Subagent / Pipeline / Supervisor + worker / Handoff / 何時拆 multi-agent 何時不拆。
---

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

## 7a. Cross-Model Review — 讓不同 LLM 互審品質 {#_7a}

§2.2 Supervisor 跟 §2.1 Pipeline 通常全部用同一個 LLM。但 [Agenvoy](https://github.com/agenvoy/Agenvoy)（Go 語言 agent platform）把**跨模型互審**做成內建功能——這是 2026 年 multi-agent 最值得學的 pattern 之一。

### 原理

```
任務 → Planner 決定拆成哪些子任務
                ↓
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  Claude      GPT-4o      Gemini
  (做子任務A)  (做子任務B)  (做子任務C)
    │           │           │
    └─────cross-review──────┘
          互相審對方的 output
                ↓
        Planner 綜合最佳答案
```

核心想法：**你不會讓同一個人寫 code 又 review 自己的 code**。模型也一樣——Claude 審 GPT 的答案能抓到 GPT 的 blind spot，反之亦然。

### 實作

```python
import asyncio

async def cross_model_review(task: str) -> str:
    """用兩個模型平行做，再互審。"""

    # Step 1: 兩個模型平行產出
    draft_a, draft_b = await asyncio.gather(
        call_llm("claude-sonnet-4-6", f"完成這個任務：\n{task}"),
        call_llm("gpt-4o", f"Complete this task:\n{task}"),
    )

    # Step 2: 互相 review
    review_of_b, review_of_a = await asyncio.gather(
        call_llm("claude-sonnet-4-6",
                  f"Review this output for errors/gaps:\n{draft_b}\n\nOriginal task: {task}"),
        call_llm("gpt-4o",
                  f"Review this output for errors/gaps:\n{draft_a}\n\nOriginal task: {task}"),
    )

    # Step 3: 綜合
    final = await call_llm("claude-sonnet-4-6", f"""
Original task: {task}

Draft A (Claude): {draft_a}
Review of A (by GPT): {review_of_a}

Draft B (GPT): {draft_b}
Review of B (by Claude): {review_of_b}

綜合以上，給出最終最佳答案。
""")
    return final
```

### 什麼時候用

| 適合 | 不適合 |
|---|---|
| 重要文件（合約 / 報告 / 對外發布） | 簡單 Q&A |
| code review（不同 model 互審 PR） | 即時對話（太慢太貴） |
| 事實查核（兩模型交叉驗證） | token 預算很緊 |
| 翻譯品質關鍵場景 | 已經用 framework 的 retry 夠了 |

### 成本 vs 品質 trade-off

Cross-review 至少 4x LLM calls（2 draft + 2 review + 1 synthesize）。用在**高價值低頻率**任務。

日常用的 cost-saving 版本：用 cheap model (Haiku) 當 reviewer，只在 reviewer 發現問題時才 escalate：

```python
async def cheap_cross_review(task: str) -> str:
    draft = await call_llm("claude-sonnet-4-6", task)

    # Haiku 快速 review (便宜)
    review = await call_llm("claude-haiku-4-5",
        f"Check for factual errors or logical gaps:\n{draft}")

    if "no issues" in review.lower():
        return draft  # 沒問題就直接用

    # 有問題才 escalate 用另一個 model 重做
    revised = await call_llm("gpt-4o",
        f"Task: {task}\n\nPrevious attempt had issues: {review}\n\nPlease provide a corrected version.")
    return revised
```

### 練習 14.4：Cross-Model Review 實驗

1. 選一個任務（例如「比較 Postgres vs MySQL」），分別只用 Claude / 只用 GPT 產出
2. 實作 cross-review（Claude 審 GPT、GPT 審 Claude）
3. 比較 3 版（Claude only / GPT only / cross-reviewed）的品質

**成功標準**：能具體指出 cross-review 抓到了哪些單一模型漏掉的問題。

---

## 8. 你做完這一章後 ✅

- [ ] 知道 Pipeline / Supervisor / Blackboard 三架構
- [ ] 看過 supervisor 的 router prompt 怎麼寫
- [ ] 知道 handoff 當作 tool 的實作
- [ ] 知道 3 種共享 memory 方式
- [ ] 知道何時用 / 何時不用 multi-agent
- [ ] 知道 Cross-Model Review 的原理 + 成本 trade-off
- [ ] 跑完練習 14.1 / 14.2 / 14.3 / 14.4

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

## 8c. 2026 multi-agent 新興安全議題

學界跟業界 2025 H2-2026 開始系統化關注的三個 multi-agent 特有風險。Ch 14 設計時你要知道有這些，[Ch 15 deploy + audit](../ch15_deploy_audit_replay/) 會回到怎麼防。

| 風險 | 一句話 | 影響 Ch 14 哪段 | 怎麼防 |
|---|---|---|---|
| **ICE**（Inter-agent Communication Exploitation） | 攻擊者把 prompt injection 塞進 agent A 給 agent B 的 handoff 訊息 | §3 Handoff 機制 / §4 共享 memory | handoff payload schema 化 + 對外來 string 預設不信、走 verification subagent |
| **Consensus Trap** | 多 agent 都同意一個錯誤答案（沒人扮演反方）→ 比單一 agent 還危險 | §2.2 Supervisor / §2.3 Blackboard | 強制設「批判 agent」角色、最終決策階段引入溫度高的 dissenter |
| **Slopsquatting** | LLM 幻想出根本不存在的 package 名稱 → 攻擊者搶註後植入惡意 code | §2.1 Pipeline 的 code-gen worker | 每一個 install 前查 PyPI / npm 真實存在 + 對齊 lockfile |

> 詳細白話 + 範例：[名詞表 § Agent 機制](https://symbiosis11503.github.io/agent-z/glossary/agent) → ICE / Consensus Trap / Slopsquatting 三條。

---

## 9. 補充閱讀

- [Anthropic — Multi-agent system design](https://www.anthropic.com/engineering/multi-agent-research-system)
- [LangGraph — Multi-agent supervisor](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
- [AutoGen 文件](https://microsoft.github.io/autogen/)
- [MetaGPT paper](https://arxiv.org/abs/2308.00352)
- `datawhalechina/hugging-multi-agent`（1.4K⭐）— MetaGPT 中文教程
- ai-dict Handoffs 段
- [Slopsquatting research（USENIX 2025）](https://arxiv.org/abs/2406.10279) — 16% of LLM-generated package names don't exist; 攻擊者搶註可植入惡意 code
- [**TauricResearch/TradingAgents**](https://github.com/TauricResearch/TradingAgents)（74K⭐, Apache）— 真實場景 multi-agent: analyst / researcher / trader / risk-manager 分工跑金融交易；§2.2 supervisor 跟 §3 handoff 的 production 級範例

---

> 🛟 **卡關時看這裡**：
> - handoff 卡死 / context 傳錯 → [故障排除 § Multi-agent](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - Pipeline / Supervisor / Blackboard 3 架構 snippet → [`starter-code/ch14_multi_agent/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch14_multi_agent)
> - Subagent vs Multi-agent 差別 → [名詞表 § 常被混淆的 pair](https://symbiosis11503.github.io/agent-z/glossary/taiwan-misc#_11-常被混淆的-pair-對比)
