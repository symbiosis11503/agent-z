# Ch 10 — ReAct / Plan-and-Solve / Reflection 範式

> **75-90 分鐘**。讀完你會懂：三個經典 agentic 範式怎麼手寫、token / latency / quality 對比、什麼任務用哪個。
>
> 動手練習：寫三個版本的同一個 agent（ReAct / Plan-and-Solve / Reflection）+ 對比結果。
>
> 前置：完成 [Ch 9](../ch09_function_calling/) — tool use loop 寫得出來。

---

## 1. 三個範式總覽

| 範式 | 一句話 | 適合 | 缺點 |
|---|---|---|---|
| **ReAct** | reason → act → observe，逐步推進 | 資訊不完全、需要動態調整 | 中間決策不一定全局最佳 |
| **Plan-and-Solve** | 先規劃完整步驟、再執行 | 多步驟、可預期、 deterministic | 計畫死 / 不能 adapt 中途突發 |
| **Reflection** | act → critique → redo | 答案要高品質 / 需要 self-correct | 慢、多 LLM call |

實務上多數複雜 agent 是 **三者混合**。本章拆開講原理，下一章（Ch 11）框架比較會看混合用法。

---

## 2. ReAct（你已經會了）

Ch 3 + Ch 9 已經實作過。一句話：

```
while not done:
    Reason: LLM 想下一步要 call 什麼工具
    Act:    執行該工具
    Observe: 把結果回去
    LLM 看著結果再決定下一步
```

優點：**simple、tool integration 自然**。
缺點：每一步只看局部，**容易繞遠路**（5 步能完的事跑 12 步）。

### 觀察一個 ReAct 「繞路」例子

任務：「找出 Anthropic / OpenAI / Google 三家 LLM 最新 Haiku 級小 model 的 input 價格」

ReAct loop 可能：
```
Round 1: search "Anthropic Haiku pricing"  → 抓到 page
Round 2: read page, decide 答案 in another sub-page → fetch sub-page
Round 3: 摘要 Anthropic 部分
Round 4: search "OpenAI gpt-4o-mini pricing"  → page
Round 5: read → 答案
Round 6: search "Google gemini-flash pricing"  → page
Round 7: read → 答案
Round 8: 整理三家給最終回應
```

8 次 LLM call。**但人類做一定先列「我要查 3 家 → 每家用 search → 整理」**——這就是 Plan-and-Solve 想做的事。

---

## 3. Plan-and-Solve

來自 [Wang et al. 2023](https://arxiv.org/abs/2305.04091)。

**第一步：LLM 不 call 工具，只列計畫**。
**第二步：依計畫一步一步執行**（每步可 call 工具）。

### 實作

```python
PLAN_SYSTEM = """
你是 task planner。看到任務，**只**輸出計畫，不要執行也不要 call 工具。
格式：
1. <步驟 1>
2. <步驟 2>
...

每步要具體，能直接執行。最多 7 步。
"""

EXEC_SYSTEM = """
你是 task executor。依照給定的 plan 一步一步做，每步可以 call 工具。
完成所有步驟後給最終回答。
"""

def plan_and_solve(task: str):
    # 第一階段：plan
    plan_resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        system=PLAN_SYSTEM,
        messages=[{"role": "user", "content": task}],
    )
    plan = plan_resp.content[0].text
    print(f"=== PLAN ===\n{plan}\n")

    # 第二階段：execute（用 ReAct loop）
    return run_agent_with_tools(
        user_message=f"Plan:\n{plan}\n\nTask: {task}\n\n依 plan 一步步做。",
        system=EXEC_SYSTEM,
    )
```

### 何時用 Plan-and-Solve

- 任務**多步驟且結構明確**（搜集資料 → 整理 → 比較）
- 你想**人類 review plan**（safety / governance 場景）
- 你想**重用 plan**（同樣 plan 跑 3 個不同輸入）

### 何時**不**該用

- 任務不確定（plan 寫了沒用、執行階段才知道下一步）
- 中途會突發狀況需要動態 adapt

---

## 4. Reflection

來自 [Shinn et al. 2023 Reflexion](https://arxiv.org/abs/2303.11366)。

**核心**：agent 做完後，**自己 critique**「答得好不好」、不滿意就 redo。

### 實作（簡化版）

```python
CRITIQUE_SYSTEM = """
你是 code reviewer。看一段 agent 的答案，**只**回兩件事：
1. 評分 0-10（10 = 完美）
2. 改進建議（如果 < 8 分）

格式：
SCORE: 7
FEEDBACK: 答案少了 X 部分，建議補上 Y。
"""

def reflection(task: str, max_iter: int = 3, target_score: int = 8):
    history = []  # 紀錄每次嘗試 + critique
    for i in range(max_iter):
        # 1. 執行
        answer_resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1500,
            messages=build_messages(task, history),
        )
        answer = answer_resp.content[0].text

        # 2. critique
        critique_resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            system=CRITIQUE_SYSTEM,
            messages=[{"role": "user", "content": f"Task: {task}\n\nAnswer:\n{answer}"}],
        )
        critique = critique_resp.content[0].text
        score = parse_score(critique)
        feedback = parse_feedback(critique)

        history.append({"attempt": answer, "score": score, "feedback": feedback})

        if score >= target_score:
            return answer

    # 達到 max_iter，回最高分版本
    return max(history, key=lambda h: h["score"])["attempt"]
```

### 何時用 Reflection

- 答案要**高品質**（code / 寫作 / 設計建議）
- 任務有**客觀標準**可以 critique（pass test / 文章長度 / 結構符不符）
- 你有**token 預算**（reflection 至少 2 倍成本）

### 何時**不**該用

- 簡單 Q&A（第一次答對機率高，reflection 是浪費）
- LLM **自己 critique 不可靠**的領域（critique 跟 produce 用同一個 LLM，盲區會重疊）

---

## 5. 三個範式對比

來假設一個任務：「寫一個 Python function 算 fibonacci，含 unit test」。

| 範式 | LLM call | token | latency | 答案品質（主觀） |
|---|---|---|---|---|
| ReAct（無工具） | 1 | 800 | 2s | 7/10 |
| Plan-and-Solve（無工具） | 2（plan + execute） | 1,500 | 4s | 8/10 |
| Reflection (3 iter) | 6（3 attempt + 3 critique） | 4,800 | 12s | 9/10 |

**重點**：品質提升的成本是 6x token + 6x latency。**不是所有任務都值得**。

---

## 6. 混合策略

Production-grade agent 多數**三者混合**：

```python
def hybrid_agent(task):
    # 1. Plan
    plan = generate_plan(task)

    # 2. ReAct execute（含 tool use）
    answer = react_loop(plan, task)

    # 3. Reflect 一次（不是 N 次，太貴）
    critique = self_critique(task, answer)
    if critique.score < 7:
        answer = react_loop(plan, task, hint=critique.feedback)

    return answer
```

這也是 Claude Code / Codex 內部大致的策略：plan → tool-use loop → 最後一次 self-check（自動）。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 7 — Work Modes**：plan-and-act / reflection / iterative refinement

---

## 8. 動手練習

### 練習 10.1：手寫 ReAct + Plan-and-Solve 對比

挑一個你會的任務（建議：「找出某個 GitHub repo 最近 5 個 issue 的標題跟標籤」，假裝有 search / fetch 工具）。
寫兩個版本：
- `react_agent.py` — 純 ReAct
- `plan_and_solve_agent.py` — Plan-and-Solve

記錄：
| 指標 | ReAct | Plan-and-Solve |
|---|---|---|
| LLM call 次數 | | |
| token in / out | | |
| latency | | |
| 答案完整度（主觀 1-10）| | |

**成功標準**：表格填齊。

### 練習 10.2：Reflection 套在 9.1 weather agent

把 Ch 9 的 weather agent 用 Reflection 包：critique 看「答案有沒有覆蓋使用者問的所有城市」、不到 8 分 redo。

**成功標準**：故意問「比較 5 個城市」、看 reflection 第一次答案漏了一個 → critique 抓到 → redo 補上。

### 練習 10.3：混合策略

寫一個 `hybrid_agent.py` 串 Plan → ReAct → 一次 Reflection，跑「研究 3 個 OSS agent framework 並寫比較表」。

**成功標準**：跑得出來、最終答案比純 ReAct 完整。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 ReAct / Plan-and-Solve / Reflection 三範式
- [ ] 知道每個的優缺點 + 何時用
- [ ] 看過 ReAct「繞路」的真實例子
- [ ] 寫過 Plan-and-Solve（plan 階段不 call 工具）
- [ ] 寫過 Reflection（critique loop）
- [ ] 知道混合策略
- [ ] 跑完練習 10.1 / 10.2 / 10.3

打勾 5 個以上，進 [Ch 11 — 框架比較](../ch11_frameworks/)。

---

## 10. 補充閱讀

- [ReAct paper (Yao et al. 2022)](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve paper (Wang et al. 2023)](https://arxiv.org/abs/2305.04091)
- [Reflexion paper (Shinn et al. 2023)](https://arxiv.org/abs/2303.11366)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- `nibzard/awesome-agentic-patterns`（4.5K⭐）— pattern catalog
