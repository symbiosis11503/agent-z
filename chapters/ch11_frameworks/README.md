# Ch 11 — Agent 框架比較

> **75-90 分鐘**。讀完你會懂：4 個主流 agent framework 的設計哲學、什麼任務該用 framework / 什麼任務直接寫 raw API、怎麼選。
>
> 動手練習：用 LangGraph + CrewAI 寫同一個 agent、比較程式碼行數 / debug 體驗。
>
> 前置：完成 [Ch 10](../ch10_react_paradigms/) — ReAct / Plan / Reflection 範式都寫過。

---

## 1. 什麼時候用 framework？

很多人學 LLM 一開始就跳進 LangChain，**這是錯的**。

> 「If you can solve it with a single LLM call, don't use a workflow. If you can solve it with a workflow, don't use an agent. If you need an agent, the simplest implementation usually wins.」
> — [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

**用 framework 的好理由**：
- 多 agent 編排（5+ agent 互相 handoff）— framework 提供 graph / state machine 抽象
- 大量 state management（複雜 memory / cache / checkpoint）
- 你的團隊**已經會**這個 framework，沒人想重學

**不該用 framework 的情境**：
- 你只是要 ReAct loop — Ch 9 的 200 行夠了
- 你不確定要做什麼 — framework 鎖住你的思路
- 學習階段 — 先學原理（raw API）才看得懂 framework 內部

---

## 2. 4 個主流 framework

| Framework | 設計哲學 | 強項 | 弱項 |
|---|---|---|---|
| **LangGraph** | 圖式 workflow + checkpoint + state machine | production 級、replay、稽核軌跡 | 學習曲線陡 |
| **CrewAI** | 角色扮演（role-based multi-agent） | 上手快、API 直覺 | 大規模 multi-agent debug 難 |
| **Smolagents** | LLM 寫 Python code 當 action (CodeAct) | 表達力強、不用 JSON-schema 包工具 | 安全性需要 sandbox |
| **Pydantic AI** | 強型別、結構化輸出第一公民 | TypeScript 開發者熟悉、可組合 | 生態剛起步 |

### 2.1 LangGraph

LangChain 團隊出的 graph-based agent runtime。

**核心抽象**：你定義 nodes（function）跟 edges（轉移條件），整個 agent 就是一張圖。

```python
from langgraph.graph import StateGraph, END

class State(TypedDict):
    messages: list
    next_action: str

def reason_node(state):
    # call LLM, decide next step
    ...
    return {"next_action": "search" or "answer"}

def search_node(state):
    # call search tool
    ...

graph = StateGraph(State)
graph.add_node("reason", reason_node)
graph.add_node("search", search_node)
graph.add_conditional_edges("reason", lambda s: s["next_action"], {
    "search": "search",
    "answer": END,
})
graph.add_edge("search", "reason")  # 搜尋完回去 reason
graph.set_entry_point("reason")

app = graph.compile(checkpointer=memory_saver)
```

**亮點**：built-in checkpointing — 整個 graph 跑到一半可以 pause / resume / time-travel。production 必備。

**配套**：LangSmith 做 observability。

### 2.2 CrewAI

Role-based multi-agent framework。

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Senior Researcher",
    goal="Find latest AI agent framework comparison",
    backstory="Expert in tech analysis.",
    tools=[search_tool, scrape_tool],
)
writer = Agent(
    role="Tech Writer",
    goal="Write a 500-word comparison article",
    backstory="Award-winning tech writer.",
    tools=[],
)

task1 = Task(description="Research...", agent=researcher)
task2 = Task(description="Write...", agent=writer, context=[task1])

crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff()
```

**亮點**：直覺、適合「demo / 小團隊 multi-agent」。

**陷阱**：role-play 把問題藏在 prompt 裡，scale 起來 debug 痛苦。

### 2.3 Smolagents

Hugging Face 出的輕量 framework。**獨特點**：用 **Python code 當 action**，不用 JSON tool schema。

```python
from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),
)

agent.run("找出 2026 年最賣座的電影前 5 名")
```

LLM 生成的 action 像：
```python
results = search("2026 top grossing movies")
top_5 = [r["title"] for r in results[:5]]
print(top_5)
```

**亮點**：表達力強——一段 code 可以 chain 多個動作、做迴圈、處理 error。論文 ([CodeAct](https://arxiv.org/abs/2402.01030)) 證明效果優於 JSON tool。

**陷阱**：LLM 寫的 code 必須 sandbox 跑（不然 RCE 風險）。

### 2.4 Pydantic AI

Pydantic 團隊出的型別安全 agent framework。

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class WeatherResult(BaseModel):
    temp: float
    desc: str
    confidence: float

agent = Agent(
    "claude-haiku-4-5",
    result_type=WeatherResult,
    system_prompt="You are a weather assistant.",
)

result = agent.run_sync("台北現在天氣")
print(result.data.temp)  # 26.0
```

**亮點**：強型別、IDE 補全好。

**陷阱**：生態新（2024-2025 才起），社群還小。

---

## 3. 同一個 agent，4 個版本對比

任務：「找出 Apple 最新 iPhone 售價」

| Framework | 程式碼行數 | 寫起來時間 | debug 體驗 |
|---|---|---|---|
| Raw API (Ch 9) | 150 | 1 hr | 你自己控制 print |
| LangGraph | 80 | 1.5 hr（要學圖式） | LangSmith trace 漂亮 |
| CrewAI | 30 | 30 min | role-play debug 痛 |
| Smolagents | 25 | 30 min | code execution log 直接讀 |
| Pydantic AI | 45 | 1 hr | 型別錯誤即時抓 |

**沒有「最好」**——看你的需求。

---

## 4. 決策樹

```
你的任務是？
├─ 單一 agent + 幾個 tool → Raw API（Ch 9 的 200 行）夠了，不要 framework
├─ Multi-agent + 簡單 role-based handoff → CrewAI
├─ 複雜 workflow + 需要 replay / time-travel → LangGraph
├─ LLM 要寫程式邏輯（迴圈 / 條件） → Smolagents
├─ Python 強型別偏好 / 跟現有 Pydantic codebase 整合 → Pydantic AI
└─ 你還在學原理 → Raw API（學完才看得懂 framework）
```

---

## 5. AutoGen / OpenAI Agents SDK 順帶一提

| Framework | 出品 | 性質 |
|---|---|---|
| **AutoGen** | Microsoft | 早期 multi-agent，社群活躍 |
| **OpenAI Agents SDK** | OpenAI | 2025 新出，跟 GPT 生態深整合 |
| **AgentScope** | Alibaba | 中國團隊，多 agent 模擬 |
| **MetaGPT** | DeepWisdom | 多 agent 軟體公司 simulation |

這 4 個本書不深入講，但你**至少要知道存在**。後面 [Ch 17 進階](../ch17_builder_advanced/) 會點到 Agentic-RL 的時候提。

---

## 6. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 7 — Work Modes**：framework abstraction / orchestration

---

## 7. 動手練習

### 練習 11.1：LangGraph + CrewAI 各寫同一個 agent

任務：「找出 2 個 GitHub repo 最近的 release notes、整理成比較表」。
寫兩版：
- `exercises/11.1_langgraph.py`
- `exercises/11.1_crewai.py`

比較：程式碼行數、寫起來時間、跑完時間、答案品質。

**成功標準**：兩版都跑得起來、比較表填滿。

### 練習 11.2：Smolagents CodeAct 體驗

裝 smolagents：`uv add smolagents`，用上面範例跑一個任務。
**觀察**：LLM 生成的 code 是什麼樣？有沒有用迴圈？有沒有 error handling？

**成功標準**：能描述 Smolagents 跟 JSON tool 的差異。

### 練習 11.3：你會選哪個？

寫一個 markdown 表（200 字）說：
- 你會把學到的 4 個 framework 用在什麼真實情境
- 哪兩個你會「絕對不用」、為什麼

**成功標準**：你能說出每個 framework 的「真實有用」場景，不是 framework feature 翻譯。

---

## 8. 你做完這一章後 ✅

- [ ] 知道何時用 framework / 何時不用
- [ ] 知道 LangGraph / CrewAI / Smolagents / Pydantic AI 的設計哲學
- [ ] 看過 4 個 framework 的 hello-world 程式碼
- [ ] 知道 CodeAct 跟 JSON tool 的差異
- [ ] 能依任務選對的 framework（不是「最熱門」）
- [ ] 跑完練習 11.1 / 11.2 / 11.3

打勾 5 個以上，進 [Ch 12 — 自寫 mini framework](../ch12_mini_framework/)。

---

## 9. 補充閱讀

- [LangGraph 文件](https://langchain-ai.github.io/langgraph/)
- [CrewAI 文件](https://docs.crewai.com)
- [Smolagents 文件](https://github.com/huggingface/smolagents)
- [Pydantic AI 文件](https://ai.pydantic.dev/)
- [CodeAct paper (Wang et al. 2024)](https://arxiv.org/abs/2402.01030)
- [Best Multi-Agent Frameworks 2026](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
- WenyuChiou Stage 4: https://github.com/WenyuChiou/awesome-agentic-ai-zh
