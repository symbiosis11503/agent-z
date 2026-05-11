---
title: 名詞表 — 實務 (Vibe Coding / Memory / Multi-agent)
description: Vibe Coding / AI Pair / Code-editing Agent / SDD / TDD / AFK / Delegation + Session Memory / Long-term / RAG / Contextual Retrieval + Multi-agent / Pipeline / Supervisor / Handoff
---

# 名詞表 · 實務 (Vibe Coding / Memory / Multi-agent)

[← 回名詞表總覽](../glossary)

## 5. Vibe Coding / 軟體開發新工作方式

> 2025-2026 工作流變遷：從「自己每行寫」到「跟 AI 對話讓它寫」。

### 氛圍編程 / Vibe Coding
- **專業**：Andrej Karpathy 2025 提出。開發者不直接編輯 code、僅透過對話 / 高層指令操控 AI agent；自己只 review diff / 改 prompt / 偶爾 nudge 方向；接受 LLM 偶爾「為什麼這樣寫」自己不完全懂。
- **白話**：「我給氛圍、AI 寫 code」。極限版：你連 syntax 都不太管、跟 AI 講「我想要這個感覺」、看結果不對就再 vibe 一次。
- **範例**：用 Cursor / Claude Code 開發網站 demo——你說「加一個 dark mode toggle 在右上角」、AI 自己寫 CSS + JS + 測試、你只看畫面對不對。**這本書 5/11 全 session 是 vibe coding 真實案例**（boss vibe、CC1 code、~1500 commit / day 量級）。
- **適用**：原型 / demo / 短期專案 / 沒人 review 也能 ship 的場景。**不適用**：核心 production system、安全敏感、需要長期維護。

### AI 結對程式設計 / AI Pair Programming
- **專業**：傳統 pair programming 一個 driver 一個 navigator；AI 版是 AI 當 navigator（給建議 / 抓 bug / catch 問題），你還是 driver 自己打字。
- **白話**：你寫一行、AI 在旁邊看、提示你「下一行可能要這樣」或「這邊有 bug」。
- **範例**：GitHub Copilot inline 自動完成、Cursor Tab。**vs Vibe Coding 的差別**：pair 你還在打字、vibe 你只下指令。
- **章節**：跨 Ch 4-5 提到

### 程式碼編輯代理 / Code-editing Agent
- **專業**：能自主多輪編輯 codebase 的 agent，不是 chat suggestion。會 plan + read multi-file + edit + run test + iterate。
- **白話**：「自己改 codebase 的 AI」——你說「修 bug #42」、它真的 git checkout / 改檔案 / commit。
- **範例**：Claude Code / Aider / OpenDevin / Cline。**vs CLI Agent**：CLI 是介面類別、code-editing 是工作類別，多數 CLI Agent 都是 code-editing agent。
- **章節**：[Ch 4](../chapters/ch04_cli_agents/)

### 規格驅動開發 / SDD (Spec-Driven Development)
- **專業**：先寫詳細 spec（input / output / 邊界條件 / 失敗模式）→ 給 agent 從 spec 生 code + test → 跑 test → 不對 reflection 改。spec 比 code 是 source of truth。
- **白話**：「先把要做什麼寫清楚、再讓 AI 做」。AI 容易在模糊 spec 上犯錯，spec 寫清楚錯就少。
- **範例**：Symbiosis SOP v0.1 的 17 步鏈條核心就是 SDD：Intake → Discovery → Spec → Truth Boundary → SDD → ...
- **章節**：[Ch 5](../chapters/ch05_cli_workflow/) + Helix V3 case study Ch 15

### 測試驅動開發 / TDD (Test-Driven Development)
- **專業**：紅綠重構 cycle：先寫 failing test（紅）→ 寫最少 code 讓 test 過（綠）→ refactor。
- **白話**：先寫「怎樣才算對」（test）、再寫「要怎麼做才對」（implementation）。
- **範例**：給 agent「修這個 bug」前先 `pytest` 看哪個 test 紅、再讓 agent 寫 code 讓那個 test 變綠。配 Hook 自動跑 test 效率高。
- **章節**：跨 Ch 12-15

### AFK 執行 / AFK (Away-From-Keyboard) Execution
- **專業**：agent 在沒有人盯著的時間執行任務（夜跑 / 後台 cron / 長時間 deep research）。需 cost cap + audit + graceful failure。
- **白話**：「你不在電腦前的時候、agent 自己做事」。早上回來看結果就好。
- **範例**：Ch 18 morning briefing agent；夜跑 deep research；長時間 codebase migration。
- **章節**：[Ch 8](../chapters/ch08_cost_observability/) + [Ch 18](../chapters/ch18_maker_educator/)

### 確認暫停 / Acceptance Gating
- **專業**：agent 在執行 high-impact action（寫檔 / push / 寄信 / 刪資料）前停下、要 human 按 Enter / 簽核才繼續。
- **白話**：「agent 動之前停下來等你說 OK」。預設保守、進階用戶可關。
- **範例**：Claude Code 預設 permission mode = ask。`/permission accept-all` 切全自動但要小心。
- **章節**：[Ch 4 §5](../chapters/ch04_cli_agents/#5-第一個真實-task)

### 委派 / Delegation
- **專業**：主 agent 把獨立 subtask 丟給 sub-agent / specialist agent 處理，結果回主 agent 不污染 context。可並行。
- **白話**：agent 也能「外包」——大事自己做、小事交給專門子 agent。
- **範例**：主 agent 收到「重構這個 module」、把「先掃全 codebase 找所有 import」delegate 給 search sub-agent。
- **章節**：[Ch 14](../chapters/ch14_multi_agent/)

---

## 6. Memory / RAG

### 會話記憶 / Session Memory
- **專業**：一次 agent / chat session 內累積的 messages 陣列。LLM 沒有跨 call 持久記憶，session memory 是 client 自己維護。
- **白話**：「這次對話內 agent 記得你說過的話」。對話結束就忘。
- **範例**：你在 ChatGPT 一個對話內說「我叫 Wei、住台北」、它記得。開新對話就忘。
- **章節**：[Ch 13 §3](../chapters/ch13_memory_rag/)

### 長期記憶 / Long-term Memory
- **專業**：跨 session persistent 的 user / world facts。實作可結構化（SQL key-value）或向量（過去對話 embed 進 vector store）。
- **白話**：「跨多次對話 agent 都記得的事」。
- **範例**：「使用者是 Wei、偏好繁中、住台北、用 Mac」這種事實寫進 SQLite。下次 agent 啟動 load 進 system prompt。
- **章節**：[Ch 13 §4](../chapters/ch13_memory_rag/#4-long-term-memory-結構化-vs-向量)

### 檢索增強生成 / RAG (Retrieval-Augmented Generation)
- **專業**：query → embedding → vector DB similarity search top-K chunks → 把 chunks 拼進 prompt → LLM 根據 chunks 回答。
- **白話**：LLM 不知道你公司的事——RAG 把你公司文件存起來、問問題時撈相關片段給 LLM 看。
- **範例**：你公司 SOP / 產品文件 / FAQ 切 chunk 進 Chroma；員工問「請假怎麼申請」、agent 撈 HR 政策 chunk + 回答。
- **章節**：[Ch 13 §5](../chapters/ch13_memory_rag/#5-rag-retrieval-augmented-generation)

### 上下文檢索 / Contextual Retrieval
- **專業**：Anthropic 2024 提出。embed 前先用 LLM 給每個 chunk 加 50-100 字「位置 + 主題」context，再 embed。提升 retrieval recall 35-49%。
- **白話**：「這 chunk 在文件中是哪段、講什麼」先寫清楚再存 vector DB。
- **範例**：原文 chunk「需診斷書。」加 context「假期政策第二條病假規定」→「[CTX: 假期政策第二條病假規定] 需診斷書。」再 embed。問「請病假要什麼」會 retrieve 到。
- **章節**：[Ch 13 §6](../chapters/ch13_memory_rag/#6-contextual-retrieval--anthropic-2024-的優化)

---

## 7. Multi-agent / Orchestration

### 多智能體 / Multi-agent
- **專業**：多個 agent 透過 shared state / handoff / blackboard 等機制協作完成單一任務。每 agent 可有不同 model / system prompt / tool set / 權限範圍。
- **白話**：多個專業 agent 分工合作、不是一個 agent 包山包海。
- **範例**：研究 agent 查資料 → 寫作 agent 寫 draft → review agent 改錯字 → 三人接力完成「寫一篇 paper 比較」。
- **章節**：[Ch 14](../chapters/ch14_multi_agent/)

### 流水線 / Pipeline
- **專業**：固定順序 A → B → C 的 multi-agent 編排，每階段輸出當下階段輸入，無 dynamic routing。
- **白話**：「先做 X、再做 Y、最後 Z」——固定流程，不會中途換方向。
- **範例**：research → write → review 三 agent 流水線。每段失敗整條失敗。
- **章節**：[Ch 14 §2.1](../chapters/ch14_multi_agent/#21-pipeline-流水線)

### 主管模式 / Supervisor
- **專業**：一個 supervisor agent 看任務 + 當前 state、回 JSON 決定派給哪個 worker、回收 worker 結果再決定下一步。
- **白話**：「老闆派工模式」——主管看情況決定誰做什麼。
- **範例**：HR agent + Sales agent + IT agent 三個 worker；supervisor 看到「客戶想知道 SLA」派 sales、「員工請假」派 HR。
- **章節**：[Ch 14 §2.2](../chapters/ch14_multi_agent/#22-supervisor-主管--部屬)

### 交接 / Handoff
- **專業**：agent 認為「這超出我能力」時、把任務 + context 轉給 specialist agent。最乾淨實作：把 handoff 當特殊 tool。
- **白話**：「這事我不會、轉給專家」。
- **範例**：通用 agent 對話到一半發現使用者問法律問題、call `handoff_to_legal_specialist(context)` 把對話交給法律 agent。
- **章節**：[Ch 14 §3](../chapters/ch14_multi_agent/#3-handoff-機制)

---

**其他類別** → [基礎](./foundation) · [Agent / CLI](./agent) · [實務](./practice) · [Production](./production) · [台灣/混淆 pair](./taiwan-misc)
