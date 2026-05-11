# Phase 0 — AI Agent 學習資料 Survey

**Date:** 2026-05-11
**Trigger:** Boss directive DC msg `1503378534192644157` — 建立 AI Agent 學習系統，新手 → 熟練技術人員，漸進式

---

## 1. 直接對標 / 重點競品（depth-surveyed）

### 1.1 datawhalechina/hello-agents（47,372⭐）
**簡介**：簡中。《从零开始构建智能体》，2025-09 推出，2026-05 仍在更新。Datawhale 社群官方教程。
**結構**：5 部分 / 16 章
- Part 1 基礎（ch1-3）：智能體概念 → 發展史 → LLM 基礎
- Part 2 構建（ch4-7）：ReAct → 低代碼平台 → 框架 → 自研框架 HelloAgents
- Part 3 高階（ch8-12）：記憶/RAG → 上下文工程 → 通信協議 → Agentic-RL → 評估
- Part 4 案例（ch13-15）：旅行助手 / DeepResearch / 賽博小鎮
- Part 5 畢業（ch16）：完整多智能體應用
**獨特點**：自建 HelloAgents 框架；含 Agentic-RL（SFT→GRPO）；GitHub Pages 線上閱讀 + PDF + 社群精選 PR + Datawhale 組隊學習
**門檻**：要有 Python 基礎 + 知道 LLM API 怎麼呼叫
**載體**：markdown + GitHub Pages + PDF + Co-creation 畢業設計

### 1.2 microsoft/ai-agents-for-beginners（61,180⭐）
**簡介**：英文原版，50+ 語言自動翻譯（含 zh-TW 繁中）。Microsoft 官方。
**結構**：12 lessons（00-course-setup → 11+）
**獨特點**：Microsoft Agent Framework（MAF）+ Azure AI Foundry V2 為主軸；含 multi-language CO-OP translator workflow；MS Discord 社群
**門檻**：較低，每 lesson 獨立可從任何一節開始
**鎖定**：Azure 帳號 / MS ecosystem 強綁定

### 1.3 huggingface/agents-course（28,539⭐）
**簡介**：英文。Hugging Face 官方。
**結構**：4 unit + 3 bonus
- Unit 0 Welcome / Unit 1 Agent 介紹 / Unit 2 框架（smolagents / LangGraph / LlamaIndex）/ Unit 3 Agentic RAG / Unit 4 final cert
**獨特點**：完成 cert + leaderboard；HF Spaces 託管動手環境；觀測/評估 bonus unit
**鎖定**：Hugging Face 生態

### 1.4 mlabonne/llm-course（79,193⭐）
**簡介**：英文。最大宗 LLM 教程，agent 是延伸而非重點。
**結構**：3 部分 — Fundamentals / Scientist（訓練 / quant / fine-tune） / Engineer（應用 / 部署）
**獨特點**：每章配 Colab notebook；DeepWiki 進階版；作者出書（LLM Engineer's Handbook）
**focus**：LLM 內部（訓練/量化/合併）多於 agent 上層應用

### 1.5 WenyuChiou/awesome-agentic-ai-zh（818⭐，boss 引用）
**簡介**：繁中三語對照。2026-05-04 推出，今日仍在更新。
**結構**：學習地圖 7 stages + 2 tracks（A: CLI Power User / B: Agent Builder）+ 5 branches（研究員/開發者/教師/知識工作者/日常使用者）
- Stage 0-2 基礎共用（Python/git/LLM/prompt）
- Track A: CLI workflow + production
- Track B: Stage 3-7（tool use → frameworks → Claude Code 生態 → memory/RAG → multi-agent）
**獨特點**：145+ projects + 62-entry MCP-Skills catalog；Claude Code 生態獨立大章（Stage 5）；branch-by-persona；繁中為主三語對照；明確「動手練習不准跳」
**性質**：學習地圖（route + reading + project pointer）**不是**自帶 curriculum，動手練習是「題目+成功標準」要學員自己寫
**門檻**：基本 Python + git + 動機

---

## 2. 中文圈深度教程聚落（datawhalechina 系）

| Repo | ⭐ | 主題 |
|---|---|---|
| hello-agents | 47K | 從零構建智能體（重點對標） |
| self-llm | 30K | 開源大模型部署食用指南 |
| happy-llm | 30K | 從零構建大模型 |
| llm-cookbook | 24K | 吳恩達課程中文版 |
| llm-universe | 13K | 小白大模型應用開發 |
| agentic-ai | 761 | 吳恩達 Agentic AI 中文版（5 modules） |
| hugging-multi-agent | 1.4K | MetaGPT 多智能體實戰 |
| agent-skills-with-anthropic | 1K | Anthropic Agent Skills 中文版 |
| tiny-universe | 4.8K | 手寫 RAG / Agent / Eval（白盒子） |

→ **觀察**：簡中圈 datawhalechina 統治、繁中圈零深度教程（只有 WenyuChiou 學習地圖）

---

## 3. 其他重點 reference

| Repo / URL | ⭐ | 性質 |
|---|---|---|
| Shubhamsaboo/awesome-llm-apps | 109K | 100+ runnable agent apps |
| e2b-dev/awesome-ai-agents | 27K | autonomous agents list |
| nibzard/awesome-agentic-patterns | 4.5K | 設計 pattern catalog |
| anthropics/prompt-eng-interactive-tutorial | 35K | Anthropic 互動 prompt 教程 |
| shareAI-lab/learn-claude-code | 60K | 從 0 構建 nano claude-code-like agent harness |
| WangRongsheng/awesome-LLM-resources | 8K | 簡中綜合資源大全 |
| anxiong2025/25-Day-Agents-Course-by-Google | 225 | Google 25 天 agent 課程 |
| wikit-ai/awesome-llm-courses | 268 | meta-list 課程目錄 |
| `ai-dict.gh.miniasp.com` | n/a | Matt Pocock AI Coding Dictionary 繁中（保哥 community 翻譯）— 7 sections: Models / Sessions+Context / Tools+Environments / Failure Modes / Handoffs / Memory+Guidance / Work Modes（boss 5/11 加入素材）|

---

## 4. 共通 pattern 抽取

### 4.1 結構
- **stage / unit / chapter** 三選一 — 多數人選 12-16 個區塊
- **必做動手練習**幾乎是共識，但**自動驗證 / cert** 少（HF 有）
- **畢業設計 / final project** 通常壓軸，但 Hello-Agents 是 Co-creation 共建模式

### 4.2 受眾分級
- 大多假設「已有 Python 基礎」
- 「真零基礎」onramp 只在 MS Beginners + WenyuChiou setup-guide 出現，且都單薄

### 4.3 vendor lock-in 光譜
- MS: Azure 強綁
- HF: smolagents/HF ecosystem
- Hello-Agents: 自建 HelloAgents 框架
- mlabonne: 多 framework 中立
- WenyuChiou: 多家 vendor 並列
- → **多 vendor 中立**屬少數派但更 future-proof

### 4.4 載體
- 多數 markdown + GitHub Pages
- 少數有 Colab notebook（mlabonne）
- 互動式 platform 幾乎沒有

### 4.5 Claude Code 生態系覆蓋
- 多數 0 / 一筆帶過
- 只有 WenyuChiou Stage 5 + Hello-Agents Extra05 認真寫
- → **MCP / Skills / Plugins / Marketplace** 深度教學是真空地帶

### 4.6 評估 / 認證
- HF cert（hosted leaderboard）
- 多數 no cert
- portfolio-based final project 普遍

---

## 5. 我們的差異化空間（給 Phase 1 UltraThink 用）

**從 survey 抓出 5 個沒人滿足的位子：**

1. **繁中 first-class curriculum**（不是 roadmap 也不是翻譯）
2. **vendor-neutral**（多 provider 一視同仁，不綁 Azure / Anthropic / HF / OpenAI 任一家）
3. **Claude Code 生態系**作一級題材（MCP / Skills / Plugins / Helix 框架做示範）
4. **真零基礎 onramp**（Stage -1：完全沒寫過 code 怎麼開始）
5. **動手 platform 真實 sandbox**（不只 markdown — 串 Helix V3 / Tauri / Mac mini local 環境給學員真跑）

**不該佔的位子**：
- LLM 內部訓練 / quant / fine-tune — mlabonne 已絕對主場
- multi-agent simulation 玩具（賽博小鎮類） — Hello-Agents 已做
- MS Azure 教程 — MS for Beginners 主場

---

## 6. 待 boss 決策（design gate）

從 phase 0 已能看出三條主路線：

**路線 A — 繁中 curriculum book**
markdown 為主 + GitHub Pages + PDF。仿 hello-agents / WenyuChiou 模式，但**繁中 + vendor-neutral + Claude Code 深度**。低成本、可漸進交付。

**路線 B — 互動式學習 platform**
markdown + 學員可登入跑真實 agent 的 sandbox（串 Helix V3 / MCP server / 自動評估）。成本高、差異化最強、跟 V3 共生。

**路線 C — 混合**
A 做主軸（內容），B 做加值（章節練習有真 platform 自動驗證）。成本中、漸進式上線。

→ 推路線 C：先做 A 拿出文字內容站穩，B 在 V3 已有的 audit/replay/cost/MCP primitives 上補一層 learner-friendly UI，自然演化。
