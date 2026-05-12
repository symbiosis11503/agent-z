# 課程地圖 — AgentZ Roadmap

一頁看完 AgentZ 全 20 章的時間、難度、產出、前置依賴。**規劃學習計畫前先讀這頁。**

[[toc]]

---

## 一張表看全本

| 章 | 標題 | 難度 | 時間 | 完成後你會 | 前置 |
|---|---|---|---|---|---|
| Ch-1 | 完全沒寫過 code 也能讀的 AI Agent 全景 | ★☆☆☆☆ | 30 min | 知道 Agent vs ChatGPT 的差別 | 無 |
| Ch 0 | 把工具裝好 | ★☆☆☆☆ | 60-90 min | Terminal / Python / git / API key 都跑得起來 | Ch-1（推薦） |
| Ch 1 | LLM 是什麼 | ★★☆☆☆ | 45-60 min | 解釋 token / context / 模型差異 | Ch 0 |
| Ch 2 | Prompt 設計 | ★★☆☆☆ | 45-60 min | 寫出穩定產出的 system + user prompt | Ch 1 |
| Ch 3 | 什麼是 Agent | ★★☆☆☆ | 45-60 min | 看得懂 agent trace、能解釋 ReAct | Ch 2 |
| Ch 4 | CLI Agent 入門 | ★★☆☆☆ | 30-45 min | 跑得起 Claude Code、能 hello-world | Ch 0 + Ch 3 |
| Ch 5 | CLI Workflow | ★★★☆☆ | 60-75 min | 寫 CLAUDE.md + slash command 拆任務 | Ch 4 |
| Ch 6 | MCP | ★★★☆☆ | 60-90 min | 接 1 個 MCP server、能寫一個 | Ch 5 |
| Ch 7 | Skills / Plugins / Marketplace | ★★★☆☆ | 60-75 min | 寫一個 SKILL.md 並 invoke | Ch 6 |
| Ch 8 | Cost 觀測 + 介入 | ★★★☆☆ | 45-60 min | 設 cost cap、看每 run 多少錢 | Ch 4 |
| Ch 9 | Function calling / Tool use | ★★★★☆ | 75-90 min | 寫 tool schema、跑 tool_use loop | Ch 1 + Python |
| Ch 10 | ReAct / Plan-and-Solve / Reflection | ★★★★☆ | 75-90 min | 寫三種範式各一個 | Ch 9 |
| Ch 11 | Framework 比較 | ★★★☆☆ | 60-90 min | 知道何時用 LangGraph / CrewAI / Smol / Pydantic | Ch 9 |
| Ch 12 | 自寫 mini framework | ★★★★☆ | 90-120 min | 從 0 寫一個 ReAct framework | Ch 10 |
| Ch 13 | Memory & RAG | ★★★★☆ | 90 min | 用 sqlite session memory + Chroma RAG | Ch 12 |
| Ch 14 | Multi-agent | ★★★★☆ | 75-90 min | 寫 Pipeline / Supervisor / Blackboard 各一 | Ch 13 |
| Ch 15 | Deploy + audit + replay + cost cap | ★★★★★ | 120-150 min | 看完 V3 production case study | Ch 14 |
| Ch 16 | Researcher 路線 | ★★★★☆ | 75-90 min | paper-summary-bot + DOI 驗證 + peer review | Ch 15 |
| Ch 17 | Builder 進階 (Agentic-RL) | ★★★★★ | 90-120 min | SFT / GRPO 跑得起來（需 GPU） | Ch 15 |
| Ch 18 | Maker / Educator 路線 | ★★★☆☆ | 60-75 min | 個人助理 / 工作坊大綱寫得出 | Ch 15 |

**全本累計**：~22-28 小時授課時間 + 30-50 小時動手練習時間 = 50-80 小時。

---

## 4 個建議學習計畫

### 計畫 A：全職投入 — **1 個月走完**
- 每天 3-5 小時 × 30 天
- 早上理論 + 下午動手 + 晚上 reflect
- 適合：寒暑假學生 / 找工作中 / 公司 sabbatical

| Week | 章節 | 里程碑 |
|---|---|---|
| 1 | Ch-1 → Ch 5 | 跑得起 Claude Code 真實 task |
| 2 | Ch 6 → Ch 10 | 自寫過 MCP server + Skill + tool-use loop |
| 3 | Ch 11 → Ch 15 | 從 0 寫過 mini framework + multi-agent + audit |
| 4 | Ch 16/17/18 + Capstone | 交一個能 show off 的 portfolio entry |

### 計畫 B：週末班 — **3 個月走完**
- 週末各 4 小時 × 12 週
- 平日只看一點 reading，主力放週末動手
- 適合：上班族、有家庭

| Month | 章節 |
|---|---|
| 1 | Ch-1 → Ch 8 (Operator) |
| 2 | Ch 9 → Ch 15 (Builder) |
| 3 | Ch 16-18 + Capstone |

### 計畫 C：晚上慢慢看 — **6 個月走完**
- 每週 2-3 晚 × 1.5-2 小時 × 26 週
- 適合：副業學習、家裡有小孩

| Bi-month | 章節 |
|---|---|
| 1-2 | Ch-1 → Ch 8 |
| 3-4 | Ch 9 → Ch 13 |
| 5 | Ch 14 + Ch 15 |
| 6 | 1 條進階分流 + Capstone |

### 計畫 D：只挑你要的（最務實）— **2-4 週**
- 不照順序看，按下面表挑：

| 你的目的 | 必讀章 | 可跳 |
|---|---|---|
| 我只想用 Claude Code 變強 | Ch-1, 4, 5, 6, 7, 8 | Builder 全部 |
| 我要面試 / 寫 agent demo | Ch 0, 9, 10, 12, 15 | Operator 大部分 |
| 我要訓自己的 model | Ch-1, 9, 17 | Operator / Maker |
| 我要在學術用 | Ch-1, 9, 13, 16 | Builder 進階 / Operator |
| 我要教別人 | Ch-1, 4, 18 | RL / 進階 |

---

## 4 層 ladder 詳細里程碑

```
┌──────────────────────────────────────────────────┐
│ Watcher（理解）— Ch 1-3                          │
│ ☐ 寫 5 個 prompt 拿到一致的繁中輸出              │
│ ☐ 看懂 agent JSON trace 並解釋每一步             │
│ ☐ 能跟非技術人講「agent vs chatbot」             │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ Operator（操作）— Ch 4-8                         │
│ ☐ Claude Code 用得很順、用 CLAUDE.md 設規則      │
│ ☐ 裝過 1 個 MCP server + 寫過 1 個 SKILL.md      │
│ ☐ 跑過 task + 看 cost dashboard 知道燒多少        │
│ ☐ 知道何時該人類介入                              │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ Builder（構建）— Ch 9-15                         │
│ ☐ 從 0 寫過 function-calling agent               │
│ ☐ 三種範式各跑過一個 task (ReAct/PnS/Reflection) │
│ ☐ 自寫過 mini framework + memory + multi-agent  │
│ ☐ 加過 cost cap + audit log（V3 governance）     │
└──────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────┐
│ 進階分流 — Ch 16/17/18                          │
│ Researcher: paper bot + DOI 驗證 + peer review    │
│ Builder+RL: SFT / GRPO fine-tune 跑起來          │
│ Maker / Educator: 個人助理 / workshop syllabus    │
└──────────────────────────────────────────────────┘
            │
            ▼
        Capstone — 1 個 portfolio entry
```

---

## 你會用到的工具棧

每章用到的工具，按章先後列：

| 工具 | 何時用 | 必要 / 選用 |
|---|---|---|
| Terminal (zsh/bash) | Ch 0+ | 必要 |
| Python 3.10+ | Ch 9+ | 必要 |
| git | Ch 0+ | 必要 |
| uv（推薦）或 pip | Ch 9+ | 必要 |
| Anthropic API key | Ch 0+ | 必要（推薦 Claude）|
| Claude Code CLI | Ch 4+ | 必要 |
| sqlite (內建) | Ch 13, 15 | 必要 |
| Chroma | Ch 13 | 選用 |
| LangGraph / CrewAI / Smolagents | Ch 11 | 任選 1-2 試 |
| TRL / Unsloth / GPU | Ch 17 | 進階分流才需要 |
| Tauri (Rust + JS) | Ch 18 | Maker 路線選用 |

**API key 預算建議**：
- 學習階段：先充 $10-20，跟 Haiku 走完 Ch -1 到 Ch 14 大約 < $10
- 練 V3 case：再 +$5-10（Ch 15 cost cap 練習）
- 太緊不夠：用 Groq / Gemini Flash 免費層替代

---

## 進階分流：哪條合你

每個人到 Ch 15 都會走過完整 Builder。Ch 16-18 是分流：

### Researcher（學術 / 研究方向）
- **適合**：研究員、研究生、有學術企圖
- **重點技能**：paper survey、anti-hallucination、citation 驗證
- **產出**：研究 agent / deep research bot / paper review bot
- **下一步**：發 paper / 開 research blog / 接學術合作

### Builder 進階（深技術 / Agentic-RL）
- **適合**：已是工程師、想做 model layer
- **重點技能**：SFT、DPO、GRPO、reward design
- **產出**：fine-tuned 7B-30B model on specific task
- **下一步**：開源 model 上 HuggingFace、發 fine-tune blog

### Maker / Educator（產品 / 教學方向）
- **適合**：產品經理、個人創業、教育者
- **重點技能**：個人助理設計、教學設計、Tauri 包裝
- **產出**：個人助理 / SaaS / workshop 教材 / YouTube 教程
- **下一步**：上架到產品市場 / 開 workshop / 寫教程獲利

---

## 你現在在哪一層？

跟著下面 5 個問題判斷：

1. **你能跟非技術朋友解釋「agent vs chatbot」嗎？** 不能 → Watcher 起步
2. **你有用過 Claude Code 跑真實 task 嗎？** 沒有 → Operator
3. **你寫過 function-calling agent 嗎？** 沒有 → Builder
4. **你 deploy 過 agent 到 production 嗎？** 沒有 → Builder 後段（Ch 15）
5. **以上都做過？** → 開始選分流

---

## 持續更新提醒

AgentZ 持續迭代中（v1.x），每週可能會：
- 補章節 common pitfalls / case study
- 補 starter code
- 修錯字 / 改用詞

**訂閱更新**：[Watch the repo](https://github.com/symbiosis11503/agent-z) on GitHub。

---

## 開始走

- 完全新手 → [Ch -1 完全沒寫過 code 也能讀](./chapters/ch-1_zero_basics/)
- 想先試試味道 → [5 分鐘 Quick Win](./quickwin)
- 已會 Python → [Ch 0 把工具裝好](./chapters/ch00_setup/)
- 已會 Claude Code → [Ch 9 Function calling](./chapters/ch09_function_calling/)
- 已走完一輪、找速查 → [速查卡 Cheatsheet (7 個分頁)](./cheatsheet) — 每頁 A4 可單獨印
