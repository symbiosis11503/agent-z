# 5 分鐘 Quick Win — 跑你第一支 AI Agent

> **完全沒寫過 code 也能跟。5 分鐘看到 agent 真的在做事。** 全程不用裝 Python、不用申請 API key。
>
> 5 分鐘後你會：（1）看 agent 在你的瀏覽器跑（2）改 prompt 改行為（3）知道 AgentZ 從哪章開始。

---

## 0. 你要準備的（30 秒）

只要兩樣：
- **任一瀏覽器**（你正在看這頁，已備齊）
- **Claude.ai / ChatGPT / Gemini 任一帳號**（免費版就行）

**完全不用**：API key、信用卡、Terminal、Python。

---

## 1. Step 1 — 跟 ChatGPT / Claude 講話（30 秒）

打開你的 [Claude.ai](https://claude.ai) 或 [ChatGPT](https://chat.openai.com) 或 [Gemini](https://gemini.google.com)。

貼這段：

```
你是研究助理。請按下面流程做:
1. 想：為了介紹「vibe coding」我需要找什麼？
2. 列出 3 個你需要的 fact
3. 假裝你查了，寫出你會找到的 3 個 fact
4. 把 fact 整合成 200 字繁中介紹

每步驟前先寫「Step X:」標籤，讓我看到你的推理過程。
```

你會看到 ChatGPT / Claude 開始**逐步思考**，每一步寫出來。

**這就是 Agent 的核心 pattern**——「想 → 做 → 看結果 → 想下一步」的循環。叫做 [ReAct](./chapters/ch10_react_paradigms/)。

---

## 2. Step 2 — 改 prompt 改行為（1 分鐘）

把上面 prompt 改一個地方，看 agent 行為怎麼變：

### 變體 A：加角色
在第一行加「你是工程師背景」。看 agent 寫的「vibe coding」介紹會偏技術細節。

### 變體 B：加限制
最後加「結論不能超過 50 字」。看 agent 真的會自我約束。

### 變體 C：加錯誤
故意問「介紹一個叫做 `XYZAgent-9999` 的框架」。看 agent 怎麼處理「不存在的東西」。

> **發現**：好的 agent 會說「沒這東西」，爛的 agent 會掰一個。
> AgentZ Ch 16 整章在講怎麼**強制 agent 不掰**（DOI 驗證 / Reflection critique）。

---

## 3. Step 3 — 看真正的 Agent code（1 分鐘）

剛剛只是用聊天 UI 模擬 agent。**真正的 agent 是一個 Python loop**：

```python
# AgentZ Ch 12 mini framework 簡化版
def agent_loop(goal, max_steps=5):
    history = []
    for step in range(max_steps):
        # 1. 想：給 LLM 看歷史、要它決定下一步
        thought = llm(f"Goal: {goal}\nHistory: {history}\nNext action?")

        # 2. 解析：agent 要不要呼叫工具？
        if "USE_TOOL:" in thought:
            tool_name, args = parse_tool(thought)
            # 3. 做：真的去 call 工具
            result = run_tool(tool_name, args)
            history.append({"thought": thought, "tool_result": result})
        else:
            # 4. 完成：agent 認為任務 done
            return thought

    return "max steps reached"

result = agent_loop("找下星期飛東京最便宜的機票")
```

這個 loop 就是 [Ch 12 起手寫的東西](./chapters/ch12_mini_framework/)。你 5 分鐘看完這頁、Ch 12 寫得起這 loop。

---

## 4. Step 4 — 看 agent 怎麼接 production（1 分鐘）

剛剛的 loop 太簡單。真實上線的 agent 還要：

- **Cost cap**：花超過 $0.10 自動停（[Ch 8](./chapters/ch08_cost_observability/)）
- **Audit log**：每步驟記資料庫、能回放（[Ch 15](./chapters/ch15_deploy_audit_replay/)）
- **Tool sandbox**：能用哪些 API、不能用哪些（[Ch 6 MCP](./chapters/ch06_mcp/)）
- **Memory**：跨 session 記住事（[Ch 13](./chapters/ch13_memory_rag/)）

AgentZ Ch 15 案例研究的 V3 框架就是把這 4 件事都做進去：

```
V3 governance stack (Ch 15)
├── ProviderKeyVault     ← API key 存哪、誰能用
├── Cost cap engine      ← 日花費上限、超了自動停
├── Audit + Replay       ← 每步寫 sqlite、能回放每個 run
└── MCP tool sandbox     ← agent 只能 call 允許的工具
```

學會這 4 件事 = 你能上線一個會花錢、安全、不會炸的 agent。

---

## 5. Step 5 — 你要從哪一章開始？（1 分鐘）

回答 3 個問題：

### Q1：你會寫 Python 嗎？

- **不會** → 從 [Ch -1（完全沒寫過 code）](./chapters/ch-1_zero_basics/) 開始
- **會** → 跳 Q2

### Q2：你用過 LLM API 嗎？（Anthropic / OpenAI / Gemini）

- **沒用過** → 從 [Ch 0（裝工具）](./chapters/ch00_setup/) 開始
- **用過** → 跳 Q3

### Q3：你會用 Claude Code / Codex CLI 嗎？

- **不會** → 從 [Ch 4（CLI agent 入門）](./chapters/ch04_cli_agents/) 開始
- **會** → 從 [Ch 9（function calling 第一原理）](./chapters/ch09_function_calling/) 開始

---

## 6. 你完成了 ✅

如果你跟著做了上面：
- [ ] Step 1: 跟 LLM 講過話、看到「想 → 做 → 看」的步驟
- [ ] Step 2: 改過 prompt、看到行為變化
- [ ] Step 3: 看完真實 agent loop code
- [ ] Step 4: 知道 production agent 需要 cost / audit / sandbox / memory
- [ ] Step 5: 決定你要從第幾章開始讀

打勾 4 個以上 = 你已經比 99% 的「想學 AI agent」的人**進入更深的層次**了。

繼續往 [你的起始章節](#5-step-5-—-你要從哪一章開始-1-分鐘) 走。

---

## 接下來

| 你的目的 | 建議路線 |
|---|---|
| **想用 agent 提升工作效率** | Ch -1 → Ch 0 → Ch 4-8（Operator 路線） |
| **想寫一個自己的 agent** | Ch 0 → Ch 1-3 → Ch 9-15（Builder 路線） |
| **想看 AgentZ 全景** | Ch -1 → Ch 0 → 一章章往下 |
| **想申請 LLM API** | [LLM / API 申請指南](./llm-providers) |
| **想理解專業名詞** | [60+ 名詞表](./glossary) |
| **想要 A4 可印速查卡** | [速查卡 Cheatsheet](./cheatsheet) |
| **跑 code 出錯不知怎修** | [故障排除](./troubleshooting) |

---

> 「Don't read about agents. Build them.」  
> —AgentZ 哲學

[首頁](/) · [章節](./chapters/ch-1_zero_basics/) · [GitHub](https://github.com/symbiosis11503/agent-z)
