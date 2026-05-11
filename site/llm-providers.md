---
title: LLM / API 申請 — 11 家分 3 個分類
description: 11 家熱門 LLM（Claude/GPT/Gemini/Groq/DeepSeek/Mistral/OpenRouter/Grok/Ollama/TAIDE/Qwen-GLM-Yi）分 3 個分類頁面（商業 / 開源聚合 / 本地主權），每家 5 段（介紹/申請/curl+Python 範例/費用/AgentZ 章節）。
---

# 熱門 LLM 模型 / API 申請 / 使用方法

11 家 AI Agent 圈最常用的 LLM、申請流程、`curl` + Python 第一支呼叫、費用粗估，跟 AgentZ 哪一章會用到。**分 3 個焦點頁面**，不再擠在一頁。

> **不要把 key 貼到任何公開地方（GitHub、Discord、截圖）**。Key 等同信用卡，外洩就被刷光。AgentZ Ch 8 / Ch 15 有講 cost cap + 環境變數隔離。
>
> 想 Ctrl-F 一次搜全本？翻 **[全本一頁](./llm-providers/all)**（自動合成，內容跟 3 分頁同步）。

[[toc]]

---

## 一張表先看完

| 模型家族 | 廠商 | 強項 | 起手價（粗估） | 是否要信用卡 | AgentZ 章節 |
|---|---|---|---|---|---|
| **Claude** (Sonnet / Opus / Haiku) | Anthropic | 長 context (1M) / coding / agent loop 穩 | 約 $3-15 / 1M input tokens | 是 | Ch 1, 4, 9, 15 |
| **GPT** (4o / o1 / o3) | OpenAI | 通用最強、生態最廣 | $2.5-30 / 1M | 是 | Ch 11 對照 |
| **Gemini** (1.5 Pro / 2.0 Flash) | Google | 超長 context (2M) / 影像強 | $0.075-7 / 1M（**有免費額度**） | 否（免費層）/ 是（付費） | Ch 11 對照 |
| **Llama / Llama 3.x** | Meta | 開源、可本地跑 | 自架免費 / cloud $0.2-1 / 1M | 看 cloud provider | Ch 17 |
| **Mistral / Mixtral** | Mistral AI (法國) | 開源 + cloud、歐盟資料合規 | $0.25-8 / 1M | 是 | — |
| **DeepSeek (R1 / V3)** | DeepSeek (中國) | 推理強、便宜 | $0.14-2.19 / 1M | 是 | — |
| **Grok** | xAI | Twitter / X 整合 | 訂閱制 + API | 是 | — |
| **Groq**（注意拼法） | Groq (硬體公司) | 推論超快（~500 tok/s） | 免費層慷慨 + 付費 $0.05-0.79 / 1M | 否（免費） | — |
| **OpenRouter** | 聚合器 | 一個 key 打 100+ 模型 | 各家 list price + 5.5% 手續費 | 是 | Ch 11 |
| **TAIDE** | 國科會 + 工研院 | 台灣主權繁中模型 | 自架免費（**沒有官方雲端 API**） | — | Ch 13 / Ch 17 |
| **Qwen / Yi / 智譜 GLM** | 阿里 / 零一萬物 / 智譜 | 開源中文強 | 自架免費 / cloud 各家 | 看 cloud | — |

---

## 申請 3 分頁

| 分類 | 包含 | 主要強項 |
|---|---|---|
| 💳 [**商業 API**](./llm-providers/commercial) | Claude / GPT / Gemini | 美國三大廠，能力最強、生態最大；要刷卡 |
| ⚡ [**開源 / 聚合 / 速度 / 便宜**](./llm-providers/opensource-aggregator) | Groq / DeepSeek / Mistral / OpenRouter / Grok | 免費試 / 推理便宜 / 一個 key 打全部 / 歐盟合規 |
| 🏠 [**本地 / 主權 / 中文圈**](./llm-providers/local-sovereign) | Ollama 本地 / TAIDE 台灣 / Qwen·GLM·Yi 中文圈 | 不要 cloud key、自己掌握資料 |

---

## 怎麼選？— AgentZ 建議

| 你的情況 | 推薦 |
|---|---|
| **完全新手，跟著 AgentZ 走** | [Claude Haiku 4.5](./llm-providers/commercial#_1-anthropic-claude-agentz-主推) — 便宜、API 穩、直接跟 AgentZ 章節對齊 |
| **不想付錢試** | [Gemini 免費層](./llm-providers/commercial#_3-google-gemini-有免費層)（2M context）或 [Groq](./llm-providers/opensource-aggregator#_4-groq-最快-免費)（速度快）或 [Ollama 本地](./llm-providers/local-sovereign#_9-本地跑-ollama-lm-studio-—-不用-api-key) |
| **要推理便宜跑大量 task** | [DeepSeek R1](./llm-providers/opensource-aggregator#_5-deepseek-推理強-便宜) |
| **要試多家 model 比較** | [OpenRouter](./llm-providers/opensource-aggregator#_7-openrouter-聚合器-一個-key-打全部) — 一個 key 全包，不用 11 個帳號 |
| **歐盟資料合規** | [Mistral](./llm-providers/opensource-aggregator#_6-mistral-ai-歐盟、gdpr-友善) |
| **台灣主權 / 不出國 / 完全本地** | [TAIDE](./llm-providers/local-sovereign#_10-taide-台灣主權繁中模型) + [Ollama](./llm-providers/local-sovereign#_9-本地跑-ollama-lm-studio-—-不用-api-key) 自架 |
| **企業整合 / 已用 Microsoft 365 / Azure** | OpenAI GPT via Azure（[商業頁](./llm-providers/commercial#_2-openai-gpt)） |
| **要 Claude Code CLI 開發 agent** | [Claude](./llm-providers/commercial#_1-anthropic-claude-agentz-主推) — 唯一深度綁定的 CLI agent 生態 |

---

## 安全 + 預算守則（**先看再開帳號**）

1. **絕不 commit key 到 git**——`.env` 加 `.gitignore`。Ch 0 §5 有 setup 範例。
2. **設 monthly limit**——Anthropic / OpenAI / Google Cloud 都能在 dashboard 設「超過 $X 自動停」。新手建議 $5-10。
3. **用 env variable**，別 hard-code：`export ANTHROPIC_API_KEY=sk-ant-...`。Python 用 `os.getenv("ANTHROPIC_API_KEY")`。
4. **cost cap loop**——agent 寫 loop 一定要算 token，設 daily cap（Ch 8 §3 有 pattern）。
5. **key 外洩 → 立即 revoke**——所有家都能在 dashboard 一鍵 disable old key、create new。
6. **不要在 Discord / 截圖貼 key**——就算只是錯字、也已經算外洩。
7. **試 model 用免費層或最便宜款**——Haiku 4.5 / Gemini 2.0 Flash / Groq 都很便宜，比一開始就上 Opus / GPT-4o 省幾百倍。

---

## 相關章節

- [Ch 0 §5 把工具裝好](./chapters/ch00_setup/) — API key 環境變數 setup
- [Ch 1 §6 各家 model 比較](./chapters/ch01_llm_basics/) — Claude / GPT / Gemini / Llama 對比
- [Ch 4 §3 CLI Agent 對照表](./chapters/ch04_cli_agents/) — Claude Code / Codex CLI / OpenCode 用哪家 model
- [Ch 8 §3 三個常見燒錢失敗模式](./chapters/ch08_cost_observability/) — 設 cap 不被 agent loop 吃光
- [Ch 11 §2 5 個 framework 對比](./chapters/ch11_frameworks/) — LangGraph / CrewAI / Smolagents / Pydantic AI 各家綁哪個 LLM
- [Ch 15 §4 production cost cap](./chapters/ch15_deploy_audit_replay/) — V3 4 道閘門
- [Ch 17 §2 開源 model 訓練](./chapters/ch17_builder_advanced/) — Llama / Qwen / DeepSeek 自架訓練
- [速查卡 — Pricing](./cheatsheet/pricing) — 11 家 pricing 2026-05 + 章節 cost 估算

---

> 找不到的家？[GitHub Issue](https://github.com/symbiosis11503/agent-z/issues) 告訴我們補進來。
