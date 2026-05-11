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

範例：當外面 PM2.5 > 35 + 室內溫度 > 28 → 自動關窗 + 開冷氣 + LINE 通知。

```python
# home_climate.py — 5 分鐘跑一次
@tool
def get_outdoor_pm25(city: str) -> float: ...

@tool
def get_indoor_temp() -> float: ...

@tool
def control_aircon(state: str, target_temp: int = 26): ...

@tool
def line_notify(msg: str): ...

agent = Agent(
    model="claude-haiku-4-5",
    tools=[get_outdoor_pm25, get_indoor_temp, control_aircon, line_notify],
    system="你是家庭氣候助理。每 5 分鐘叫一次。判斷是否需要動作、有的話用工具、講中文。",
)
agent.run("檢查現況、需要的話動作")
```

**安全 + 隱私 3 條**：
1. agent 別連可以下單的工具（PChome / Foodpanda），除非 confirm gate
2. Skill 限制兒少內容、加 deny-list
3. 全程 log，家裡有事可以查（[Ch 15 audit + replay](../ch15_deploy_audit_replay/)）

### 2.4 Mac menubar 包裝（Tauri 範例）

把 daily assistant 包成 macOS menubar app，按一下就跑：

```bash
# 從 V3 Tauri scaffold 改（Ch 15 starter code）
cp -r ~/Projects/helix-framework/v3-mac-app ~/my-assistant
cd ~/my-assistant
# 把 src-tauri/src/main.rs 的 "launchV3" command 換成你的 daily briefing
```

關鍵設計：
- 按 menubar icon → trigger Python 腳本 → 結果 push 通知
- 通知 click → 打開 markdown report
- 用 `launchctl` 設成開機自啟 + 每 30 min 跑一次

### 2.5 你的 capstone 候選

- 「我的助理 v1」— morning briefing + evening review
- 「我的閱讀 agent」— 餵 URL 自動加進 Obsidian + 摘要 + 月底總結
- 「我的健康 tracker」— Apple Health 撈資料 + 給建議
- 「我的編輯助理」— 寫部落格 draft → Reflection 改 → publish
- 「我的家庭氣候 agent」— PM2.5/溫濕度自動調冷氣 + LINE 通知
- 「我的開發伴侶」— pre-commit hook agent 自動 lint + 補 test + 寫 commit msg
- 「我的閱讀理解陪跑」— 給孩子讀繪本，agent 問問題 + 引導思考

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
- **共用 API key**：不要學員自己 setup，準備 workshop 專用 key（設 cost cap $5）
- **練習用 Groq / Gemini 免費層**：學員零成本練熟才會回家自己玩
- **公開教材**：CC-BY 授權放 GitHub，社群會幫你 PR 改錯

### 3.5 常見教學地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **講太多概念** | 學員聽完不會跑 | 砍一半 slide、加 20 min 動手練 |
| **demo 卡關** | 你的 demo 不能跑、現場 debug 20 min | 預錄影片 + 截圖 fallback |
| **學員裝環境炸** | Python 版本 / pip / API key 各種問題 | 用 Colab / GitHub Codespaces 免裝 |
| **進度差異大** | 高手 5 min 寫完、新手卡 30 min | pair programming 或 stretch goal |
| **API quota 爆** | 30 學員同時跑炸 rate limit | 分階段跑或用本地 Ollama（[本地 / 主權 LLM 指南](https://symbiosis11503.github.io/agent-z/llm-providers/local-sovereign)）|
| **沒 reflection** | 學員做完不知道學到什麼 | 結尾 15 min retro：「今天學最深刻的一條」 |

### 3.6 互動式教材技巧

AgentZ 自己用了的 3 招（你可以抄）：

1. **In-page LLM tryout**——章節嵌入 LLM 試玩元件，學員不用切視窗。本書每章 §「在這頁練」就是。
2. **Milestone evidence**——學員交「跑得起來的證據」（screenshot / log）解鎖下章，不是考試。
3. **Progressive disclosure**——基礎章節砍掉 advanced 概念、advanced 章再來，避免 cognitive overload。

### 3.7 你的 capstone 候選

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

### Capstone Rubric（評分標準，5 條）

| 項目 | 通過標準 |
|---|---|
| **能跑** | clone repo → 跟 README 步驟 → 看到結果。新人 < 30 min 上手 |
| **能解決真實問題** | 不是 toy demo，是你 / 朋友 / 家人會用的 |
| **有 governance** | cost cap / audit / replay 至少 2 個（[Ch 15](../ch15_deploy_audit_replay/)）|
| **有 reflection** | README 講「為什麼這樣設計」+「踩過什麼坑」 |
| **可擴展** | 別人 PR / fork 改造門檻低（README 有 contribution 段）|

### 範例 Capstone（虛擬範例，給你抓 scope）

- **學員 A — 個人簡報助理**：morning briefing (calendar + email + todo) → menubar app → reflection log 累積 30 天 → 寫了個「我學到什麼」blog post。技術用 Claude Haiku + Tauri + sqlite。
- **學員 B — 小公司客服分流 agent**：Helpscout → agent 分類（technical / billing / refund）→ 自動回三類 template 草稿 → 客服只負責確認 send。cost cap $2/day、audit 全 log。
- **學員 C — 國中段考題講解 bot**：學生拍題目 → OCR → agent 講解步驟（不直接給答案）→ 反問引導 → 對 100 題後產出弱點分析。用 Gemini 免費層 + Whisper 語音。

走完這一步、你就**從本書的 Builder 階段畢業**。

---

## 5b. 在這頁練 morning briefing prompt

Maker 路線的 morning briefing agent system prompt 試起來：

<LLMTryout
  title="Ch 18 in-page tryout — morning briefing"
  defaultSystem="你是早晨簡報助理。早上 8 點。給定使用者今天的：(1) calendar events (2) 未讀 email (3) 未完成 todo，產出 3 段繁中：今天行程（最多 5 條）/ 重要 email（最多 3 條）/ 該做的 todo（最多 5 條）+ 結尾 1 行「今天最該專注的 1 件事」。"
  defaultPrompt="Calendar: 10:00 客戶會議, 14:30 V3 deploy review, 17:00 健身.
Unread email: client A 詢問報價, internal IT 維護通知, AWS 帳單.
Todo: PR review 3 件, 寫週報, 訂機票." />

## 6. 補充閱讀

### Maker 工具棧
- [Tauri](https://tauri.app/) — Rust+JS desktop app (Mac/Win/Linux)
- [Helix V3 Tauri scaffold](https://github.com/symbiosis11503/helix-framework) — 直接 fork
- [Home Assistant](https://www.home-assistant.io/) — 家庭自動化開源 hub
- [apprise](https://github.com/caronc/apprise) — 一行 code push notification（LINE / Slack / Telegram / email 都支援）
- [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) — 視覺化 multi-agent flow

### Educator 參考
- [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/) — Andrew Ng 教學範本
- [fast.ai Practical Deep Learning](https://course.fast.ai/) — 動手練習為主的教學典範
- [Jupyter Book](https://jupyterbook.org/) — 互動式教材出版平台
- [Software Carpentry](https://software-carpentry.org/) — 給研究員教程式的教學設計參考

### 經典文章
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — 必讀
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Building a startup with AI agents (a16z)](https://a16z.com/podcasts/)
- [Karpathy — vibe coding](https://x.com/karpathy/status/1886192184808149383) — 新時代開發者心法
- WenyuChiou Branch decision tree: https://github.com/WenyuChiou/awesome-agentic-ai-zh

### 社群
- AgentZ Capstone gallery — 等待貢獻者投稿（PR welcome！）
- AgentZ Discussions — [github.com/symbiosis11503/agent-z/discussions](https://github.com/symbiosis11503/agent-z/discussions)

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
