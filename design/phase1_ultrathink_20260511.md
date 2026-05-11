# Phase 1 — UltraThink: 7 維度差異化 + 系統骨架

**Date:** 2026-05-11
**Trigger:** Boss 拍板路線 C（混合：A 內容打底 + B sandbox 漸進）
**Input:** `survey/phase0_survey_20260511.md`
**Output:** 7 維度差異化定位 + 受眾分級 + curriculum 骨架 + 載體規劃

---

## 1. 專案命名（pending boss）

候選：
- **HelixLearn**（綁 Helix 框架但獨立子品牌）
- **AgentLearn-zh-TW** / **AgentZ**（精簡）
- **學徒島**（中文敘事感）
- **從零到 Agent 構建者**（叙事 title）

→ Phase 2 跟 boss 拍板。先用 **AI-LS** 內部代號。

---

## 2. 7 維度詳細定位

| # | 維度 | 競品做法 | AI-LS 定位 |
|---|---|---|---|
| 1 | **受眾分級** | 多數假設「已有 Python」 | **3 層**：Stage -1 完全零基礎（不會寫 code 也能讀懂） / Stage 0-7 主幹 / Stage 8+ 進階分流 |
| 2 | **漸進路徑** | 線性 16 章 / 12 lesson | **三段式漸進**：理解（Watcher）→ 操作（Operator）→ 構建（Builder），每段都有 milestone evidence |
| 3 | **動手練習** | markdown 題目，自評 | **題目 + 自動驗證 sandbox**（v2 後接 V3 audit / replay / cost / MCP），v1 先給 starter repo + checklist |
| 4 | **評量方式** | HF 有 cert，其他無 | **章節 milestone evidence** — 學員上傳 GitHub 連結或 sandbox run ID，章節右上角從 ☐ → ✅；最後章節公開 portfolio 串接 |
| 5 | **工具整合** | MS = Azure / HF = HF Spaces / Hello-Agents = HelloAgents | **vendor-neutral**：Claude / OpenAI / Gemini / Groq / Mistral / OpenRouter / DeepSeek 都當 first-class，**用 Helix V3 的 multi-provider catalog 當示範** |
| 6 | **中文化深度** | 簡中為主 / 翻譯機翻 | **繁中 first**，用詞跟我們 V3 一致（指揮中心 / 介入 / 派遣 / 看進度）；簡中/EN 是 v2+ co-op-translator automation |
| 7 | **差異化空間** | Claude Code 生態 0 / 一筆帶過 | **Claude Code 生態系**作一級題材：MCP / Skills / Plugins / Marketplace 各一章 + 用 Helix V3 當完整 case study |

---

## 3. 受眾分級 map

```
            零基礎 (Stage -1)
              │
              │ 完全沒寫過 code，連 Terminal 都沒打開過
              │ 用 ChatGPT 但不知道 API 是什麼
              │
              ▼
        Watcher (Stage 0-1)   ← 理解：知道 AI Agent 是什麼、能讀懂別人的 agent
              │
              │ 看得懂教學影片、能跟著 prompt 出結果
              │ 知道 token / context window / role
              │
              ▼
        Operator (Stage 2-4)  ← 操作：能裝 / 跑 / 設定別人寫好的 agent
              │
              │ Claude Code CLI / Codex / OpenCode 任一順手
              │ 會接 MCP server、會寫簡單 Skill
              │ 會 debug 工具呼叫 / cost 控制
              │
              ▼
        Builder (Stage 5-7)   ← 構建：能從 0 寫 agent、設計 multi-agent
              │
              │ ReAct / function calling / Skills 寫得出來
              │ memory / RAG / observability 設得起來
              │ deploy 上線 + audit / replay / cost cap 配齊
              │
              ▼
        Advanced (Stage 8+)   ← 進階分流（依目的）
              ├─ Researcher 路線（paper / DeepResearch / multi-agent simulation）
              ├─ Builder 路線（自寫框架 / Agentic-RL / 上線運維）
              ├─ Maker 路線（個人助理 / Mac app / 日常自動化）
              └─ Educator 路線（教別人怎麼學 agent）
```

每階段交付物（milestone evidence）：
- Stage -1：第一次跑出 LLM Hello-World 截圖
- Stage 0-1：3 個 prompt design 練習 + token cost 計算表
- Stage 2-4：用 Claude Code 跑出真實 task（含 MCP 接 1 個工具）
- Stage 5-7：寫過自己的 agent、有 git repo
- Stage 8+：completion portfolio entry

---

## 4. Curriculum 骨架（首版 18 章）

> 章節數比 hello-agents 多 2 章（多了 -1 真零基礎 + 1 Claude Code 生態 extra），跟 WenyuChiou 7 stages 對得起來

### Part 0 — 真零基礎 onramp（Stage -1）
- **Ch-1** 完全沒寫過 code 也能讀的 AI Agent 全景（30 分鐘讀完）
- **Ch 0** 把工具裝好：Terminal / Python / git / API key 從 0 開始

### Part 1 — 理解 Watcher（Stage 0-1）
- **Ch 1** LLM 是什麼：token / context / 各家比較
- **Ch 2** Prompt 設計：system / few-shot / CoT
- **Ch 3** 什麼是 Agent：工具呼叫 / ReAct / 為何需要

### Part 2 — 操作 Operator（Stage 2-4）
- **Ch 4** CLI Agent 入門：Claude Code / Codex / OpenCode 三家比較與選擇
- **Ch 5** CLAUDE.md + slash command + 多步驟拆解
- **Ch 6** MCP 是什麼、怎麼裝、怎麼接 Notion / Obsidian / GitHub
- **Ch 7** Skills / Plugins / Marketplace 生態
- **Ch 8** Cost 觀測 + token 預算 + 介入（abort）

### Part 3 — 構建 Builder（Stage 5-7）
- **Ch 9** Function calling 跟 tool use 第一原理
- **Ch 10** ReAct / Plan-and-Solve / Reflection 三範式手寫
- **Ch 11** 主流框架 LangGraph / CrewAI / Smolagents 比較動手
- **Ch 12** 自寫一個 mini agent framework
- **Ch 13** Memory & RAG：vector DB / long-term memory
- **Ch 14** Multi-agent 協作 / handoff / 主從架構
- **Ch 15** Deploy + audit + replay + cost cap（用 Helix V3 做完整 case study）

### Part 4 — 進階分流（Stage 8+）
- **Ch 16** Researcher 路線
- **Ch 17** Builder 路線（含 Agentic-RL 入門）
- **Ch 18** Maker / Educator 路線

### Capstone
- 畢業作品集（GitHub portfolio）— 各分流交付一個完整可運行的 agent 系統

---

## 5. 載體規劃（路線 C）

### v1（A 為主，6-8 週）
- **內容載體**：純 markdown + GitHub Pages 線上閱讀 + PDF release
- **網域**：`learn.symbiosis.tw` 或 `agent.symbiosis.tw`（CF Tunnel 進去）
- **repo**：`/Users/wei/Projects/ai-agent-learning-system/` → GitHub public（boss 拍板時機）
- **動手練習**：題目 + 成功標準 markdown，starter repo + checklist；無自動驗證
- **產出**：18 章內容 markdown + Pages 上線 + README + CHANGELOG

### v2（B 漸進整合，v1 後 4-6 週）
- **sandbox 串接**：學員可在每章末「動手練習」打開 Helix V3 sandbox
  - 共用 V3 multi-provider catalog（iter 149/150 已 live）
  - 共用 V3 audit / replay / cost / MCP primitives
  - 學員自帶 API key 或用 mock provider 練習
- **milestone evidence**：學員上傳 sandbox run_id / GitHub PR 到章節 ✅ 標記
- **產出**：V3 加 `/v3/learn/*` 教學模式 endpoint + learner UI shell

### v3（社群化，v2 後持續）
- co-op-translator 自動 zh-CN / EN 翻譯（仿 MS for Beginners）
- 投稿機制（章節貢獻、案例貢獻）
- portfolio leaderboard / 學員作品集

---

## 6. 跟 V3 / Helix / 其他專案的邊界

- **AI-LS = 新獨立專案**，跟 V3 / Helix / SBS / ERP **不混**
- **V3 是 AI-LS 的「示範平台」**——Stage 5 Claude Code 生態 + Part 3 Builder 後段用 V3 當完整 case study
- **V3 提供 sandbox runtime**（v2 後串），不過 V3 本身不為了 AI-LS 改架構
- **記憶體 / 學員資料**：v1 不收個資（純 markdown 站）；v2 後若收 milestone evidence，走 GitHub OAuth + 純連結（不存個資）

---

## 7. 公開化策略

- **v1 release**：GitHub repo public + CHANGELOG + 對 WenyuChiou repo 發 issue 自我介紹（補 zh-TW curriculum 空缺）
- **社群觸及**：DC / 部落格 / Hacker News / r/LocalLLM / Datawhale 二次連結
- **長期定位**：建立「**繁中 vendor-neutral Claude-Code-first 學習 ladder**」的 known reference

---

## 8. Phase 2 設計 gate（要 boss 拍板）

1. **專案名稱**：HelixLearn / 學徒島 / AgentZ / 從零到 Agent 構建者 / 其他？
2. **網域**：`learn.symbiosis.tw` / `agent.symbiosis.tw` / 別的？
3. **v1 章節骨架**：18 章是否合理？要不要 trim / 加？
4. **動手練習 starter repo 要不要 monorepo**（跟主 markdown 同 repo）vs split repo？
5. **GitHub public 時機**：今天先 init 還是內容到 ch 3 + ch 6 + ch 15 三章 done 再 public？
6. **PDF release**：要不要做（pandoc build / Datawhale 風格）？
7. **MIT vs CC-BY-SA**？

---

## 9. 預估時程

- Phase 0 survey：✅ 已完成（~30 分鐘）
- Phase 1 UltraThink：✅ 已完成（~30 分鐘）
- Phase 2 boss 拍板 design gate：等 boss 回 §8 七項
- Phase 3 v1 內容生產：估 6-8 週
  - Week 1：Ch-1 + Ch 0 + Ch 1（真零基礎到 LLM 基礎）
  - Week 2：Ch 2-3（prompt + agent 概念）
  - Week 3：Ch 4-5（CLI agent + workflow）
  - Week 4：Ch 6-7（MCP + Skills）
  - Week 5：Ch 8-10（cost + tool use + 範式）
  - Week 6：Ch 11-12（框架 + 自寫 mini）
  - Week 7：Ch 13-15（memory + multi-agent + deploy 含 V3）
  - Week 8：Ch 16-18 + capstone scaffold
- Phase 4 v2 sandbox 整合：v1 ship 後估 4-6 週

---

## 10. 風險 / Open issue

- **內容生產規模大** — 18 章 × 平均 8K 字 ≈ 144K 字繁中 + 動手 starter code。要不要分批 ship（先 ch -1 到 ch 8 上線、後段邊產邊出）？
- **跟 hello-agents 重疊感** — 我們有 5 個差異點墊底（繁中 / vendor-neutral / Claude Code 深 / 真零基礎 / V3 sandbox），但仍需要在 README 開門見山說清楚。
- **V3 sandbox 串接的 audit cost** — 學員大量 mock provider 跑也是 audit row，要為 learner runs 加 tag 區隔（不污染真實 cost analytics）。v2 設計 gate 處理。
- **boss 自己時間** — 18 章 6-8 週是 CC1 全力產的時程，boss 不在 critical path（只在 design gate 拍板 + portfolio public 拍板）。
