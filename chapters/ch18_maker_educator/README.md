# Ch 18 — Maker / Educator 路線（進階分流）

> **60-75 分鐘**。讀完你會懂：怎麼把 agent 變成「個人助理 / 桌面 app / 家庭自動化」、或者怎麼當老師教別人學 agent。
>
> 動手練習：你選——寫一個個人 daily assistant 或寫一份 4 hr workshop syllabus。
>
> 前置：Builder 階段（Ch 9-15）夠用。Ch 17 advanced 不需要。

---

## 1. 兩條子分流

這章兩個小路線，挑你要的：

| 路線 | 適合 | 重點 |
|---|---|---|
| **Maker** | 想做出「自己會用的東西」、不想當工程師 | 個人助理 / 桌面 app / 家庭自動化 |
| **Educator** | 想教別人 / 公司內訓 / 寫部落格 | 教學設計 / workshop / 互動式材料 |

---

## 2. Maker 路線

### 2.1 目標：個人 daily assistant

讓 agent 變成你的「私人助理」：
- 早上跟你說今天行程（從 Google Calendar 撈）
- 提醒重要 deadline（從 Notion 撈）
- 抓你 email 整理重點（用 Gmail MCP）
- 你語音 / chat 跟它對話、它幫你寫 todo / 設提醒

**Stack 推薦**：
- Claude Code CLI 是最簡單 — `claude` 一打就跑、MCP 接東西方便
- 想要 desktop 介面：Tauri (Rust + JS) / Electron / 直接用 Helix V3 Tauri scaffold (Ch 15)
- 想語音：Whisper STT (本地) + ElevenLabs TTS / Mac VoiceOver
- 想 always-on：launchd (macOS) / systemd (Linux) cron + 通知中心 (apprise)

### 2.2 範例：morning briefing agent

```python
# morning_briefing.py
import os
from agentz_mini import Agent, tool

@tool
def get_calendar(date: str) -> str:
    """Get Google Calendar events for date (YYYY-MM-DD)."""
    # 用 google calendar API (Ch 6 MCP catalog 有現成 MCP server)
    return "..."

@tool
def get_unread_emails(max_n: int = 10) -> str:
    """Get last N unread emails from Gmail."""
    return "..."

@tool
def get_notion_todos() -> str:
    """Get incomplete Notion todos."""
    return "..."

agent = Agent(
    model="claude-haiku-4-5",
    tools=[get_calendar, get_unread_emails, get_notion_todos],
    system="""
你是早晨簡報助理。每天早上 8 點被叫起來。
任務：
1. 撈今天行程
2. 撈未讀 email (高優先級的)
3. 撈未完成 Notion todo
4. 整合成 3 段繁中：
   - 今天行程（最多 5 條）
   - 重要 email（最多 3 條）
   - 今天該做的 todo（最多 5 條）
最後給一個「今天最該專注的 1 件事」結論。
""",
)

# 用 launchd / cron 每天早上 8 點跑
result = agent.run("產出今天的早晨簡報")
print(result.answer)

# 用 apprise / mail 寄給自己
os.system(f"echo '{result.answer}' | mail -s '今日簡報' you@email.com")
```

進階：包進 Mac menubar app（Tauri）一鍵看。

### 2.3 家庭自動化

- HomeAssistant + agent（控燈光 / 冷氣 / 音響）
- agent 看公開資料（天氣 / 空品 / 交通）自動調整環境
- 跟小孩聊天 / 故事生成器（Skill 控限制兒少不宜內容）

### 2.4 你的 capstone 候選

- 「我的助理 v1」— morning briefing + evening review
- 「我的閱讀 agent」— 餵 URL 自動加進 Obsidian + 摘要 + 月底總結
- 「我的健康 tracker」— Apple Health 撈資料 + 給建議
- 「我的編輯助理」— 寫部落格 draft → Reflection 改 → publish

---

## 3. Educator 路線

### 3.1 教什麼 / 怎麼教

學了一遍 AgentZ，**你可能想轉過來教別人**。市場現在缺：

- 公司內訓（傳統工程團隊轉 agent 開發）
- 大學選修課（很多教授還沒摸過 agent）
- bootcamp 短訓（2-4 hr workshop）
- YouTube / 部落格教程

### 3.2 教學設計 4 個原則

1. **動手練習為主、概念為輔**
   - AgentZ 全書遵守這條。動口講 1 hr 不如自己跑 1 個 task。
2. **錯誤是教材**
   - 故意讓學員看到 agent 燒錢 / 幻覺 / 失敗。學員看到痛才會記住規則。
3. **跨 vendor 練、不綁單家**
   - 學員出社會用什麼公司什麼模型不確定。教 generic 概念 + 換 vendor 練。
4. **milestone 證明而不是考試**
   - 期末交 portfolio repo（5 個能跑的 agent），比 multi-choice 考試實用 100x。

### 3.3 範例：4 hr workshop syllabus

target: 已會 Python、沒接過 LLM API

```
Hour 1 — Watcher
  - 15 min: AgentZ Ch 1 - LLM 是什麼、token / context
  - 15 min: AgentZ Ch 2 - prompt 設計、4 欄位框架
  - 30 min: 動手：跑 3 家 LLM 比較

Hour 2 — Tool Use & Agent
  - 30 min: AgentZ Ch 3 + Ch 9 - tool_use loop 概念 + 範例 code
  - 30 min: 動手：寫 weather agent（不靠 framework）

Hour 3 — Claude Code 生態
  - 20 min: AgentZ Ch 4 + Ch 5 - CLI agent + CLAUDE.md
  - 20 min: AgentZ Ch 6 - MCP demo
  - 20 min: 動手：裝 GitHub MCP、跑「列出我未 review 的 PR」

Hour 4 — 整合 + Cost
  - 20 min: AgentZ Ch 8 - cost / 介入 / 失敗模式
  - 30 min: 動手：把學員的 weather agent 加 cost cap + audit log
  - 10 min: Q&A + 下一步推薦 reading
```

### 3.4 教材製作建議

- **slide ≠ live demo**。slide 5 個就夠。重點全在 live demo + 學員跟著敲。
- **準備 fallback**：API 掛了用 mock provider、學員 key 出問題用 Groq 免費 tier
- **錄影**：學員回家會想複習，錄影 + 公開放 YouTube
- **學員池小開始**：第一次 workshop 5-10 人。**問題即時 debug** 才能優化教法

### 3.5 你的 capstone 候選

- 「8 hr AI Agent 入門」workshop 教材包（slide + exercise repo + cheatsheet）
- 你自己錄一個「AgentZ 走讀」YouTube playlist
- 為公司內部寫一份「我們 team 怎麼用 agent」runbook
- 翻譯 AgentZ 一章成英文 / 簡中（社群貢獻）

---

## 4. 你做完這一章後 ✅

- [ ] 知道 Maker / Educator 兩條子分流的差別
- [ ] Maker 路線：選一個 capstone 候選、開始做
- [ ] Educator 路線：寫一份 workshop syllabus 或部落格大綱
- [ ] 計算過你的 capstone「定義完成」是什麼樣（具體交付物 + 驗證條件）

---

## 5. 結尾：Capstone 是什麼？

走完 18 章你還剩**最後一件事**：交一個 portfolio entry。

**規模**：1 個能跑、能 demo、能 show off 給人看的 agent 系統。
**載體**：GitHub repo + README + demo video / GIF + 部署連結（任選 1）。
**內容**：
- 完整 README（為什麼做、怎麼跑、技術選擇理由）
- agent source code（套用本書學到的 governance：cost cap / audit / replay 至少 2 個）
- 至少一個 hands-on test 證明它能跑
- 一段 reflective writeup（200 字繁中）：學到什麼、哪裡卡關、未來怎麼擴

走完這一步、你就**從本書的 Builder 階段畢業**。

---

## 6. 補充閱讀

- AgentZ Capstone gallery — 等待貢獻者投稿
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Building a startup with AI agents (a16z)](https://a16z.com/podcasts/)
- WenyuChiou Branch decision tree: https://github.com/WenyuChiou/awesome-agentic-ai-zh

---

## 走完 AgentZ 18 章你會什麼？

```
✅ 前言     — 沙發上就能讀完 / 從 Terminal 打開始
✅ Watcher  — LLM 機制懂 / prompt 寫得好 / Agent 內部結構懂
✅ Operator — Claude Code 用得順 / CLAUDE.md / MCP / Skills / cost / 介入
✅ Builder  — 從零寫 agent / 框架 / memory / multi-agent / production governance
✅ 進階     — 依你目的挑路線（研究 / RL / Maker / Educator）
✅ Capstone — 一個能 show off 的作品集 entry
```

**從「LLM 使用者」變成「Agent 系統構建者」。** 任務完成。

---

> 「Don't build smarter LLMs—build smarter integrations.」  
> —AgentZ 默認哲學
