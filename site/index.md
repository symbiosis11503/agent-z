---
layout: home

hero:
  name: "AgentZ"
  text: "從零到 AI Agent 構建者"
  tagline: 繁中 first-class · vendor-neutral · Claude Code 生態深入 · 真零基礎 onramp
  image:
    src: /hero.svg
    alt: AgentZ
  actions:
    - theme: brand
      text: 5 分鐘 Quick Win →
      link: /quickwin
    - theme: alt
      text: 從 Ch-1 開始
      link: /chapters/ch-1_zero_basics/
    - theme: alt
      text: 已經會 Python? 跳 Ch 1
      link: /chapters/ch01_llm_basics/
    - theme: alt
      text: LLM / API 申請指南
      link: /llm-providers
    - theme: alt
      text: GitHub
      link: https://github.com/symbiosis11503/agent-z
    - theme: alt
      text: 下載 PDF 離線版
      link: https://github.com/symbiosis11503/agent-z/releases/latest

features:
  - icon: 🪜
    title: 4 層 ladder，循序漸進
    details: 零基礎 → Watcher（理解）→ Operator（操作）→ Builder（構建）→ 進階分流。每層有 milestone evidence。
  - icon: 🇹🇼
    title: 繁中 first，不是翻譯腔
    details: 全本繁中撰寫、用詞對齊 Claude Code 生態系。簡中圈被 hello-agents 統治，繁中圈這本是 first-class curriculum。
  - icon: 🔄
    title: Vendor-neutral
    details: Claude / OpenAI / Gemini / Groq / OpenRouter / DeepSeek 一視同仁。不綁 Azure / HF 任何單家，每章範例多家並列。
  - icon: 🧩
    title: Claude Code 生態系深入
    details: MCP / Skills / Plugins / Marketplace 各章獨立，含 Progressive Disclosure 設計 pattern。多數教程一筆帶過的這條真空地帶。
  - icon: 🏃
    title: 真零基礎 onramp
    details: Ch-1 沙發讀完不打開任何工具。Ch 0 從怎麼開 Terminal 教起。連 ChatGPT 都沒用過的人也能跟。
  - icon: 🛠
    title: 動手練習不准跳
    details: 每章 1-3 個練習，題目 + 成功標準清楚。完成 milestone evidence 解鎖下章。v2 後串 Helix V3 sandbox 真自動驗證。
  - icon: 🔑
    title: 11 家 LLM API 申請懶人包（3 分頁）
    details: <a href="/agent-z/llm-providers">商業 / 開源聚合 / 本地主權</a> 三分類頁，每家 5 段（介紹 / 申請 / curl+Python 範例 / 費用 / AgentZ 章節）+ 決策矩陣 + 安全 7 條。
  - icon: 🇹🇼
    title: TAIDE 主權 LLM 整合
    details: 台灣國科會 + 工研院 TAIDE 模型自架步驟，含 M3 Ultra Ollama recipe（<a href="/agent-z/llm-providers/local-sovereign">本地 / 主權頁</a>）。AgentZ Ch 13 / Ch 17 用得到。
  - icon: 📖
    title: 70+ 名詞表 5 分類
    details: <a href="/agent-z/glossary">基礎 / Agent / 實務 / Production / 台灣&pair</a> 五分類頁，每詞 4 欄（專業 / 白話 / 範例 / 章節）。含 vibe coding、SDD、TDD、AFK、Computer Use、Subagent、MCP Scope。
  - icon: 📋
    title: 速查卡 7 個分頁 A4 可印
    details: <a href="/agent-z/cheatsheet">CLI / SDK / Pricing / Patterns / MCP / Governance / Compliance</a> 七焦點分頁，每頁 A4 可單獨印，要全本翻 <a href="/agent-z/cheatsheet/all">all-in-one</a>。學完忘了哪個指令翻這裡。
---

## 為什麼又一本？

中文圈的 AI Agent 學習資源有兩個空缺：

1. **沒有繁中 first 的 curriculum** — 簡中圈 `datawhalechina/hello-agents` 已經很強（47K⭐），但繁中只有 `WenyuChiou/awesome-agentic-ai-zh` 是學習地圖（818⭐），不是 curriculum。
2. **多數教程綁特定 vendor** — Microsoft Beginners = Azure，HuggingFace Course = HF 生態。實務上你需要在 Claude / OpenAI / Gemini 之間切換。

AgentZ 補上這兩塊，並且把 **Claude Code 生態系**（MCP / Skills / Plugins / Marketplace）當一級題材深入講——這是 2025-2026 年最重要、但其他教程多數一筆帶過的真空地帶。

## 你會走過

```
零基礎          →  Watcher          →  Operator          →  Builder          →  進階分流
（連 Terminal     （理解 LLM、         （CLI agent、        （從 0 寫 agent、    （Researcher /
  都沒打開）        prompt、agent）     MCP、Skills）        framework、deploy）   Builder / Maker /
                                                                                Educator）
```

四層 ladder，**每層都有 milestone evidence**——做完該章節，你會有一個 GitHub repo / run ID / portfolio entry 證明你真的會了，不是看過。

## 一頁看完

- 📋 [**5 分鐘 Quick Win**](./quickwin) — 不裝 Python 體驗 agent，了解你適合哪一章開始
- 🗺 [**課程地圖**](./roadmap) — 20 章難度/時間/4 學習計畫對照
- 🔑 [**LLM / API 申請指南 (3 分頁)**](./llm-providers) — 11 家 LLM：商業 / 開源聚合 / 本地主權
- 📖 [**70+ 名詞表 (5 分類)**](./glossary) — 基礎 / Agent / 實務 / Production / 台灣&pair
- ❓ [**FAQ**](./faq) — 22 題 6 大類常見問題
- ✅ [**學習進度檢核**](./progress) — milestone evidence + portfolio repo 模板
- 🏆 [**Capstone Gallery**](./capstone) — 學員作品集 + 投稿入口
- 📋 [**速查卡 (7 個分頁)**](./cheatsheet) — CLI / SDK / Pricing / Patterns / MCP / Governance / Compliance，每頁 A4 可印
- 🛠 [**故障排除**](./troubleshooting) — 12 大類常見錯誤 + 症狀 + 解法

## 規模 (v1.6, 2026-05)

```
20 章 / 6,700+ 行繁中 / 60+ 動手練習
10 starter-code dirs (ch06-15) — 全部跑得起來
18/20 章有「常見地雷」section
70+ 名詞表 (5 分類) / 7 個 A4 速查卡 (含合規 ISO/NIST/EU AI Act)
2026 議題：A2A 協議 / OTel GenAI / ICE / Consensus Trap / Slopsquatting
全章 SEO sitemap / editLink / 在 GitHub 編輯本頁
MIT 授權，章節 + code 都可商用
```

## 課程版本

**v1.x**（你正在看的）：完整 markdown + 互動式 site + PDF release，持續迭代擴充中
**v2**（規劃中）：每章動手練習可在頁面內串 Helix V3 sandbox 真跑、貼自己 API key 立刻看結果
**v3**（規劃中）：自動 zh-CN / EN 翻譯、社群投稿、portfolio leaderboard

[查 Changelog →](https://github.com/symbiosis11503/agent-z/blob/main/CHANGELOG.md)

## 哲學

> 「Don't build smarter LLMs—build smarter integrations.」
>
> 「AI 可以幫你寫腳本，但**『什麼叫好』，還是要人來定義**。」 — [@kojenchieh](https://www.threads.com/@kojenchieh/post/DYNwkBekqVz)
>
> 工具進步快、整合永遠是瓶頸；工具寫 code 容易、定義「好」永遠是你。AgentZ 訓練的是這兩條。
