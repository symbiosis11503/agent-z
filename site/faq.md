# FAQ — 常見問題

學員 / 訪客最常問的問題集中回答。沒看到你的問題？開 [Discussion](https://github.com/symbiosis11503/agent-z/discussions) 問。

[[toc]]

---

## 適不適合我

### Q: 完全沒寫過 code，我跟得上嗎？
A: 跟得上。從 [Ch-1](./chapters/ch-1_zero_basics/) 沙發讀完，[Ch 0](./chapters/ch00_setup/) 從怎麼開 Terminal 教起。需要的時間多一點（建議多花 50% 比正常進度慢），但每章都有「成功標準」可以驗證自己沒跳。

### Q: 已經會 Python / 用過 Claude Code，跳哪章？
A: 看 [課程地圖](./roadmap) 的「計畫 D」對照表。
- 想用 Claude Code 變強 → Ch 4-8
- 想寫 agent → Ch 9-15
- 想訓 model → Ch 17

### Q: 我學 ML / DL 一陣子了，這跟 LLM training 課程差在哪？
A: AgentZ 主軸是 **agent system 構建**（prompt + tool use + orchestration + governance），不是 model training。Ch 17 有 Agentic-RL 一章（SFT/GRPO 入門），但深度不到 Karpathy zero-to-hero 級別。要深學 LLM training 推薦 mlabonne/llm-course。

### Q: 我看完別本（hello-agents / agents-course）了，AgentZ 還值得讀嗎？
A: 值得看 **Part 2 Operator**（Ch 4-8）— Claude Code / MCP / Skills 那條線，其他教程多數一筆帶過或沒講。Builder 跟進階分流也有獨家 V3 case study（Ch 15）。

---

## 錢的事

### Q: 學完要花多少錢？
A: 預期 **$10-30**：
- Anthropic API：充 $10，跟 Haiku 走 Ch -1 到 Ch 14 < $10
- 練 Ch 15 V3 governance：再 +$5-10
- 不想花錢：用 Groq 免費層 + Gemini 免費層 替代，**零成本** 也能走完 80%
- 想進 Ch 17 RL：要 GPU（runpod $1.5-3/hr × 5-10 hr = $10-30）

### Q: 沒信用卡綁 API 怎麼辦？
A: 三條路：
1. **Groq**（最推薦）：[console.groq.com](https://console.groq.com) 免信用卡免費層每天上千次 request
2. **Google Gemini**：[aistudio.google.com](https://aistudio.google.com) 用 Google 帳號免費 2M context
3. **Ollama 本地跑**：[ollama.com](https://ollama.com) 完全離線、零成本，但要本機有 GPU 或 Apple Silicon M1+
看 [LLM / API 申請指南](./llm-providers) 完整對照。

### Q: 哪家 LLM 最划算？
A: 學習階段：Haiku 4.5 ($1/M input)。實戰：根據用量決定。
- 量小（每天 < $1）：Haiku / Gemini Flash
- 量中（每月 < $200）：Sonnet 4.6 / Gemini Pro
- 量大需要省：DeepSeek R1（推理）/ Qwen 自架
- 完整對照看 [LLM / API 申請指南](./llm-providers) 的「怎麼選」段。

---

## 環境

### Q: Mac / Windows / Linux 都能用嗎？
A: 都能。
- **Mac / Linux**：原生最順
- **Windows**：建議用 WSL2（Windows Subsystem for Linux）跑，Claude Code 在 WSL2 跑很穩
- **Chromebook**：用 GitHub Codespaces 雲端跑，AgentZ Ch 0 教你

### Q: 我電腦很爛能跑嗎？
A: 取決於走到哪：
- Ch -1 到 Ch 15：4GB RAM 任何電腦都行（重要的是 API 在雲端）
- Ch 17（Agentic-RL）：需要 GPU 或 Apple M3+，**或** 用 Colab / runpod 雲 GPU
- 個人助理（Ch 18 Maker）：Mac M2 8GB 起跳建議

### Q: 我要不要學 Python 才能繼續？
A: Ch -1 / Ch 0 / Ch 1-3 不用。Ch 4-8（Operator）也 mostly 不用，是用 Claude Code 跑指令。**Ch 9（Builder 開始）正式進 Python**。建議先把 Python 基礎打到「會看、會改、能 debug」即可，[Ch 0](./chapters/ch00_setup/) 有 Python 環境設定 + 5 條基礎建議。

---

## 時間 / 節奏

### Q: 多久能走完？
A: 看 [課程地圖](./roadmap) 4 個學習計畫：
- 全職投入：1 個月
- 週末班：3 個月
- 晚上慢慢看：6 個月
- 挑你要的：2-4 週

### Q: 一週能花多少時間最理想？
A: 5-8 小時最甜蜜點。少於 5 hr 進度太慢、容易忘；多於 15 hr 會 burnout、學了沒消化。

### Q: 我可以跳章節嗎？
A: 部分可以。
- Ch -1 / Ch 0 可跳（你已經會的話）
- Watcher（Ch 1-3）盡量別跳，跳了後面有概念漏洞
- Operator（Ch 4-8）可挑你需要的（看 [計畫 D](./roadmap)）
- Builder（Ch 9-15）**強烈建議按序**，每章有依賴
- 進階分流（Ch 16-18）依目的選一條，三條不用都看

---

## 內容 / 範圍

### Q: AgentZ 為什麼這麼強調 Claude Code？
A: 因為 2025-2026 年 CLI agent 是工程師日常工具，而 Claude Code 是最成熟生態（MCP / Skills / Plugins / Marketplace 四大柱子最齊全）。本書 vendor-neutral，每章 LLM 範例多家並列；但 **agent harness 那層** Claude Code 是事實標準，所以重點放它。Codex CLI / OpenCode 在 [Ch 4](./chapters/ch04_cli_agents/) 也有並列對照。

### Q: 為什麼用 V3 當 Ch 15 案例？
A: V3（Helix V3）是維護者自家在做的 production agent platform，有完整 audit / replay / cost cap / MCP / multi-provider 的真 case，原始碼可看可改。教 production agent governance 用「看得到的真 case」比 textbook 章節更有重量。

### Q: AgentZ 涵蓋 EU AI Act / ISO 42001 / NIST AI RMF 嗎？
A: 涵蓋。v1.6 加了 [Ch 15 §5b 合規對照](./chapters/ch15_deploy_audit_replay/#5b-合規--iso-42001--nist-ai-rmf--eu-ai-act) 把三大標準對映到 V3 4 pillar，加 [速查卡 Compliance](./cheatsheet/compliance) 速查 + 罰款 + 時程。**注意：不是法律建議**，production 導入仍需找律師 / 顧問。台灣 AI 基本法草案 2025-11 公布、跟 EU AI Act 對齊。

### Q: 多 agent 系統的新興安全議題（ICE / Consensus Trap / Slopsquatting）AgentZ 有講嗎？
A: 有。[Ch 14 §8c 2026 multi-agent 新興安全](./chapters/ch14_multi_agent/#8c-2026-multi-agent-新興安全議題) 整理 3 個 risk + 防禦表，[Ch 16 §4 進階 ICE](./chapters/ch16_researcher/#進階跨-llm-投票ice--iterative-consensus-ensemble) 給 Python 範例。詞條深入看 [名詞表 § Agent §5](./glossary/agent#_5-multi-agent-verification--安全2026-新加)。

### Q: 我看完能找到 AI Agent 工程師工作嗎？
A: 看完不會直接讓你找到，但能 give you the toolkit：
- 動手做過 Capstone（[Ch 18 Rubric](./chapters/ch18_maker_educator/#5-結尾capstone-是什麼)）→ 面試 portfolio
- 知道 production agent governance（cost / audit / replay）→ 面試聊得進去
- 自寫過 mini framework → 看得懂別人的 framework code review

實務上還需要：1-2 個真實 deploy 過的 agent + GitHub 活躍度 + 對特定 domain（健康 / 金融 / 教育）的理解。

---

## 商用 / 授權

### Q: 我可以把 AgentZ 內容拿來上課嗎？
A: 可以，**MIT 授權**。請保留原書 attribution。建議直接連回 https://symbiosis11503.github.io/agent-z/ 而不是整本 fork。

### Q: 我可以翻譯成簡中 / 英文嗎？
A: 歡迎！開 PR 放 `i18n/<lang>/` 路徑。先在 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 開 thread 避免重工。AgentZ v3 規劃內含自動翻譯，但人工翻譯品質更好。

### Q: 我可以拿 starter code 改成商業專案嗎？
A: MIT — 可以。不用 attribution 但歡迎你 star 一下。

---

## 卡關 / 求救

### Q: 我跑 code 報錯怎麼辦？
A:
1. 先看對應 [starter-code/chXX/](https://github.com/symbiosis11503/agent-z/tree/main/starter-code) 確認有完整版可比對
2. 看 [glossary](./glossary) 確認術語沒誤解
3. 還不行去 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 開 thread，貼錯誤訊息 + 環境（OS / Python / SDK 版本）
4. 如果是書本身錯，開 [Issue](https://github.com/symbiosis11503/agent-z/issues)

### Q: API 跑炸 / 花太多錢
A:
- 第一時間去 [Anthropic Console](https://console.anthropic.com/) 設 monthly limit（推薦 $20）
- [Ch 8 Cost 觀測](./chapters/ch08_cost_observability/) 教你怎麼防
- 用 starter-code `ch08_cost_observability/cost_tracker.py` 包 SDK 用，每 call 自動擋

### Q: 章節讀完不確定有沒有真懂
A: 跑該章「動手練習」+ 對「成功標準」勾。讀完 ≠ 學會，動手才會。

---

## 未來 / 路線

### Q: v2 / v3 什麼時候上？
A:
- **v2**：章節「動手練習」串 Helix V3 sandbox 真跑（學員可用書內按鈕直接跑 agent 而不用裝 Python）。目標 2026 Q3。
- **v3**：自動 zh-CN / EN 翻譯 + 社群投稿 + Capstone leaderboard。目標 2026 Q4。

### Q: 你們會出英文版嗎？
A: 會。v3 階段。先做高品質的繁中。英文版用 [co-op-translator](https://github.com/Azure/co-op-translator) auto-translate 後人工 review。

### Q: 有 Discord / Slack 社群嗎？
A: 目前用 [GitHub Discussions](https://github.com/symbiosis11503/agent-z/discussions)。如果學員數超過 100 會考慮開 Discord。

---

## 還有疑問？

- 開 [GitHub Discussion](https://github.com/symbiosis11503/agent-z/discussions)（問題 + 公開回答，幫到後人）
- 個人聯絡：[symbiosis11503@gmail.com](mailto:symbiosis11503@gmail.com)

回 [首頁](/) · [課程地圖](./roadmap) · [5 分鐘 Quick Win](./quickwin)
