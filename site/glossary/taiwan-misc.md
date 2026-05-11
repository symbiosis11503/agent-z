---
title: 名詞表 — 台灣 AI / 常被混淆的 pair / 外部詞典
description: TAIDE / Sovereign AI / Local Inference + 7 對常被混淆 pair (MCP vs Skill, Tool Use vs Function Calling 等) + 外部權威詞典清單
---

# 名詞表 · 台灣 AI / 常被混淆的 pair / 外部詞典

[← 回名詞表總覽](../glossary)

## 10. 台灣 AI / 主權方案

### TAIDE / TAIDE (Trustworthy AI Dialogue Engine)
- **專業**：國科會主導、中研院 + 台大 + 清大 + 交大 + 成大等學界合作開發的本土繁中 LLM。HuggingFace 開放下載 model weights，目前最新 Gemma-3-TAIDE-12b-Chat-2602 (12B params, 2025-02 發布)。
- **白話**：「台灣自己訓的繁中 LLM」。免費下載，自己架。
- **範例**：本地用 Ollama 跑 `ollama pull taide`（社群有 unofficial mirror）或從 HuggingFace 直接 load。配 vLLM 起 OpenAI-compat server、AgentZ / V3 都能接。
- **應用 AgentZ**：M3 Ultra 192GB + Ollama + TAIDE-12b 是「全主權」AgentZ 方案——0 雲端依賴。
- **沒有雲端 API**：要自架。HuggingFace Inference Endpoints 可付費租 GPU 跑。

### 國家主權 AI / Sovereign AI
- **專業**：國家 / 組織能自主控制 base model 訓練、推論硬體、資料管道、policy 規則的 AI 體系。對應 supply-chain risk 跟資料主權。
- **白話**：「不依賴美國雲端 / 中國雲端、自己能 train 跟 serve」的 AI。
- **範例**：TAIDE（台灣）、TII Falcon（UAE）、Mistral（法國）、DeepSeek（中國）、Bharat GPT（印度）都屬此類。
- **章節**：跨 Ch 1 + Ch 17

### 本地推論 / Local Inference
- **專業**：model + inference engine 跑在你掌控的硬體（個人機器 / 自己機房）、不經第三方雲。
- **白話**：「LLM 在我電腦跑、沒網路也能用、資料不出我手」。
- **範例**：Ollama (Mac/Linux 一行裝)、vLLM (GPU server)、MLX (Apple Silicon 加速)、llama.cpp (CPU 也能跑、量化 model)。
- **章節**：[Ch 1 §6 + Ch 17](../chapters/ch01_llm_basics/)

---

## 11. 常被混淆的 pair 對比

學習者最常搞混的 7 組對比。**「兩個都是 X，但...」** 一句話切清楚。

### MCP vs Skill
- **MCP** = agent ↔ 外部「函式庫 / API」的共通 protocol（執行能力）
- **Skill** = 給 LLM 看的「教戰手冊 / SOP」（指引 LLM 怎麼做）
- 一句話：**MCP 給工具、Skill 給說明書**。同一個任務可以兩個都用——MCP 提供「寄信」function、Skill 告訴 LLM「寄信前 5 步檢查」。

### Tool Use vs Function Calling
- **同一個東西的兩個名字**。Anthropic 文件用「tool use」、OpenAI 早期叫「function calling」、現在統一回「tools」。
- API 層面差異：Anthropic `tool_use` block / OpenAI `tool_calls` array — schema 不同但概念同。

### Agent vs Workflow
- **Workflow** = 你預先寫死的 step sequence（A → B → C），無分支決策
- **Agent** = LLM 自己決定下一步（A → ? → ?），自主路由
- 一句話：**Workflow 是火車軌道、Agent 是 GPS 導航**。Workflow 可預測但不靈活；Agent 靈活但要 cost cap / audit 護欄。

### ReAct vs Plan-and-Solve
- **ReAct** = 邊想邊做（每步 reason → act → observe → reason...），動態反應 environment
- **Plan-and-Solve** = 先想完 plan 再 execute（planner 列 5 步、executor 照跑）
- 哪個好？**短任務 / environment 變動大 → ReAct；步驟清楚 / 可預測 → Plan-and-Solve**。實務常混（Plan 主導 + 每步 ReAct 微調）。

### Fine-tuning vs RAG
- **Fine-tuning** = 改模型權重（讓 LLM「內化」某 domain）；成本高、需要 GPU / 訓練資料
- **RAG** = 不改模型，每次推論前撈相關資料塞 context（讓 LLM「查資料庫」）
- 哪個好？**事實 / 知識頻繁更新 → RAG；風格 / tone / 特定格式輸出 → Fine-tuning**。多數情境 RAG 先試（便宜 100x），不夠才 fine-tune。

### Subagent vs Multi-agent
- **Subagent** = 主 agent 派下去做子任務的隔離 agent（context 不共享，只回結果）
- **Multi-agent** = 多個 agent 各自有角色 / 工具集，協作完成任務（context 部分共享或 handoff）
- 一句話：**Subagent 是外包工讀生、Multi-agent 是團隊**。Subagent 是 Multi-agent 的最簡形式。

### CLI Agent vs Code-editing Agent
- **CLI Agent** = 「介面類別」（terminal 跑、shell-driven 的 agent）
- **Code-editing Agent** = 「工作類別」（會自主多輪改 codebase 的 agent）
- 多數 CLI Agent（Claude Code / Codex / OpenCode）都是 code-editing agent；但 code-editing 不一定是 CLI（Cursor / Cline 是 IDE-based）。

---

## 12. 外部權威詞典（不重複造輪）

- 🔗 **[ai-dict.gh.miniasp.com](https://ai-dict.gh.miniasp.com/)** — Matt Pocock AI Coding Dictionary 繁中（保哥技術社群翻譯）。7 sections: Models / Sessions+Context / Tools+Environments / Failure Modes / Handoffs / Memory+Guidance / Work Modes。本書每章末「補充閱讀」會對應到 ai-dict 對應 section。
- 🔗 **[WenyuChiou/awesome-agentic-ai-zh resources/glossary.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/glossary.md)** — 30+ 詞，每個 30-80 字解釋。
- 🔗 **[Anthropic Glossary](https://docs.anthropic.com/en/docs/about-claude/glossary)** — 官方英文 glossary，跟本書名詞 1-1 對齊。


---

**其他類別** → [基礎](./foundation) · [Agent / CLI](./agent) · [實務](./practice) · [Production](./production) · [台灣/混淆 pair](./taiwan-misc)
