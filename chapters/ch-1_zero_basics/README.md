# Ch-1 完全沒寫過 code 也能讀的 AI Agent 全景

> **30 分鐘讀完。本章不用打開任何工具，從沙發上就能讀完。** 讀完你會知道：AI Agent 是什麼、為什麼 2025 年之後變熱、跟你天天用的 ChatGPT 差在哪、自己學要走什麼路。
>
> **沒有 code、沒有 API、沒有 Terminal**。下一章 Ch 0 才開始裝東西。

---

> 「AI 可以幫你寫腳本，但**『什麼叫好』，還是要人來定義**。」——[@kojenchieh](https://www.threads.com/@kojenchieh/post/DYNwkBekqVz) 在效能測試領域講的，整本書都這樣。
>
> 工具（Claude / Cursor / Agent SDK）只佔 10%；定義你要的結果、判斷答案對不對、決定哪些 edge case 必過——這 90% 永遠是你。AgentZ 從第一章到最後一章都在練這 90%。

---

## 1. 30 秒摘要

**ChatGPT 是 LLM**——你問一句、它答一句，對話結束就忘了。

**AI Agent 是會自己跑流程的 LLM**——你給它一個目標（例如「幫我訂下週去東京的機加酒」），它會自己查機票、比價、開瀏覽器、填表單、回來告訴你結果。

差別只有一個詞：**自主**。Agent 可以**自己決定下一步做什麼**，而不是每一步都等你問。

---

## 2. 為什麼 2025 年之後變熱？

2022 年底 ChatGPT 出來的時候，大家發現 LLM 已經能流暢對話。但接下來的 2 年發生了三件事，才讓「Agent」從研究論文變成日常工具：

1. **Tool use（工具呼叫）變穩了**——LLM 學會在回答時，**主動呼叫**外部工具（Google 搜尋、計算機、寄信、看你電腦的檔案）。從前你貼網址它只能憑訓練的記憶亂猜，現在它可以真的去抓最新內容。
2. **長 context 變便宜了**——你可以一次塞 100,000 字的文件給它，它都看得完。
3. **代理商（agent harness）出現了**——像 Claude Code、Codex、OpenCode 這類「Agent 殼」，把 LLM 包進一個可以跑指令、改檔案、開瀏覽器的環境。

這三件事疊起來就是：**LLM 不再只是聊天，而是能「替你工作」**。

---

## 3. Agent vs ChatGPT 三個具體差別

舉個例子：你想找下星期去東京的便宜機票。

| 你做的事 | ChatGPT 會做什麼 | AI Agent 會做什麼 |
|---|---|---|
| 「幫我找下星期去東京最便宜的機票」 | 「我建議你查 Skyscanner」（給你建議） | 自己打開 Skyscanner、輸入日期、抓票價、整理表格給你看 |
| 「幫我訂一張」 | 「請你自己去訂，我不能訂票」 | 自己填訂位資料（需要你授權付款） |
| 「等下幫我提醒 check-in」 | 對話結束就忘了 | 自己設提醒、check-in 時間到自己開瀏覽器幫你 check-in |

**3 個關鍵字**：
1. **工具呼叫**：Agent 能用瀏覽器、Terminal、API
2. **自主決策**：「下一步做什麼」是它決定的，不用你逐步指揮
3. **記憶**：今天交辦的事，明天它還記得

---

## 3b. 5 個你會看到 Agent 真的在做的事

機票太抽象？這 5 個例子是 2025-2026 年已經「上線中」的 agent 應用：

| 場景 | 沒有 Agent 你怎麼做 | Agent 怎麼做 | 真實系統 |
|---|---|---|---|
| **改 code 修 bug** | 看 issue → 翻 code → 想方案 → 改 → 跑測試（30-90 min） | 你貼 issue URL → Claude Code 自己讀 code → 找 root cause → 改 → 跑測試 → 回報結果（5-15 min） | Claude Code、Codex CLI |
| **整理 email** | 一封一封看、分類、回 template | agent 自動分類「重要/可延後/廣告」、起草 3 個 template 等你確認 | Gmail Plus + Anthropic API |
| **寫研究報告** | Google 半天、看 10 paper、自己整合 | agent 跑 5-10 paper、自動摘要、整合成 table 給你 | OpenAI Deep Research、Perplexity |
| **客服分流** | 24/7 人工值班、接到問題慢慢回 | agent 自動分類、簡單問題自己答、複雜題轉真人 | 多數 SaaS 公司內部 |
| **資料分析** | 你 SQL → Excel → chart → narrative | agent 自己跑 SQL → 看結果 → 畫圖 → 寫分析 | Claude Code + sqlite MCP / pandas |

**共通模式**：人類**指定目標**、agent **自己完成執行流程**。本書教你怎麼設計、怎麼用、怎麼寫一個。

---

## 4. Agent 的內部長什麼樣子？

不寫 code 也能理解的版本：

```
你 → 給目標 → ┌──────────────────────┐
              │   AI Agent           │
              │                       │
              │  1. 想：「為了完成這個目標 │
              │     我下一步該做什麼？」    │
              │                       │
              │  2. 決定：「我要用 XX 工具」 │
              │                       │
              │  3. 做：呼叫工具         │
              │                       │
              │  4. 看結果：「夠了沒？      │
              │     不夠的話重來」         │
              └──────────────────────┘
                       ↓ 完成 ↓
                     回報給你
```

這個 **想 → 決定 → 做 → 看結果 → 想下一步** 的循環叫做 **ReAct**（reason + act）。是 2022 年提出的，到今天還是大多數 agent 的核心。後面 Ch 10 會手把手帶你寫一次。

---

## 5. 你會聽到的 5 個關鍵詞（先有印象就好）

讀完這一節你不用會用，只要看到不會嚇到。

- **LLM**（Large Language Model）：大型語言模型。ChatGPT / Claude / Gemini 都是 LLM。
- **Token**：LLM 算錢的單位。一個中文字通常 ≈ 1-2 token，一個英文單字通常 ≈ 1 token。
- **API key**：你向 Anthropic / OpenAI 等公司申請的「鑰匙」，用它呼叫他們的 LLM，會根據用了多少 token 算錢。
- **MCP**（Model Context Protocol）：2024 年底 Anthropic 提出的標準，讓 LLM 跟工具講話有共通語言。**這是 2025-2026 年最重要的新東西**，Ch 6 整章都在講。
- **Skill**：給 LLM 看的「使用手冊」。例如「打開 Excel 的 SOP」、「跟客戶寄信的範本」。Skill 跟 MCP 兩個常被搞混，Ch 7 會講清楚。

---

## 6. 為什麼會出現「Claude Code 生態系」？

> 如果你聽過 Claude Code 跳過這節；如果沒聽過，這節 5 分鐘解釋為什麼這本書花了很多章節在它上面。

ChatGPT 是「Web 版聊天介面」。但 **Claude Code 是「電腦的 Terminal 殼」**——你在你電腦上打 `claude` 就會跑起來，它可以：
- 直接讀你電腦的檔案
- 直接改你的程式碼
- 直接呼叫 Terminal 跑指令
- 接 MCP server 串到 Notion / Slack / Excel 等工具

這跟 Web 版聊天差別在哪？**Agent 真正會做事**。

2025 年下半年起，這種「CLI agent」變成軟體工程師的日常工具——你不再用 ChatGPT「問怎麼寫」、然後手動 copy-paste；你直接告訴 Claude Code「幫我改」，它真的會去改。

本書 Part 2 全部在講怎麼用 CLI agent；Part 3 在講怎麼**寫一個自己的 CLI agent**。

---

## 7. 學習地圖：你會走過的 4 層

```
   你現在的位置（讀完 Ch-1，已經知道 Agent 是什麼）
            │
            ▼
   Watcher（理解）          ← Ch 1-3：LLM、prompt、agent 概念
            │
            │ 看得懂別人寫的 agent、能用 prompt 拿到你要的東西
            ▼
   Operator（操作）         ← Ch 4-8：CLI agent、MCP、Skills、cost
            │
            │ Claude Code 用得很順、會接 MCP、會控成本
            ▼
   Builder（構建）          ← Ch 9-15：tool use、framework、deploy
            │
            │ 從零寫 agent、自己接 LLM API、能 deploy 上線
            ▼
   進階分流                  ← Ch 16-18：Researcher / Builder / Maker / Educator
```

從零基礎到 Operator，估計 4-6 週（每週 5-8 小時）。
從 Operator 到 Builder，估計再 4-6 週。
完整走完進階分流，估 6 個月。

不用怕：每章都會清楚講「**做完這章你會什麼**」，做不到就回頭做動手練習，不是你笨。

---

## 8. 動手練習（這一章唯一一個，不用打開任何工具）

**練習 -1.1**：用紙筆或備忘錄寫下：
1. 你**為什麼想學 AI Agent**？想用來做什麼？（5 句話以內）
2. 你**現在會什麼**？例如「會用 ChatGPT 但不會寫 code」、「會 Python 但沒接過 API」、「會寫程式但沒接觸過 LLM」。
3. 走完本書，你**最想做出來的一個 agent** 是什麼？（一句話）

這 3 題的答案會幫你決定**從哪一章開始讀**——下一章 Ch 0 開頭有自我評估表格。

**成功標準**：寫下答案。沒有對錯。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 Agent 跟 ChatGPT 的核心差別是「自主」
- [ ] 知道工具呼叫 / 自主決策 / 記憶是 Agent 的 3 個關鍵字
- [ ] 聽到 LLM / token / API key / MCP / Skill 不會嚇到
- [ ] 知道 Claude Code 為什麼是 2025-2026 年的重點
- [ ] 寫下了練習 -1.1 的 3 個答案

打勾完三個以上，準備好進 Ch 0 了。

---

## 9b. 你適合讀 AgentZ 嗎？— 30 秒自我檢查

勾 3 個以上你就在對的地方：

- [ ] 我已經會用 ChatGPT / Claude / Gemini 之類的 AI 工具
- [ ] 我知道工作上「我手做的事」哪些可能自動化
- [ ] 我願意一週花 5-8 小時學新東西（**不是 5-8 個月**）
- [ ] 我有 Mac / Windows / Linux 任一電腦（Chromebook 也行）
- [ ] 我願意申請至少一張信用卡綁 LLM API（最低 $5 起跳）— 或用免費層（Groq / Gemini Flash）

**不適合**：
- ❌ 想看「AI 取代人類」哲學討論 → 看 [Anthropic Acceptable Use Policy](https://www.anthropic.com/legal/aup) 比較實際
- ❌ 想 1 天內變成 AI 專家 → 沒有這種教材
- ❌ 完全沒接觸過電腦 / 不打字 → 先學基本電腦操作

**還有問題就跳到 [Ch 0 Setup](../ch00_setup/)** — 有自我評估表能幫你決定從第幾章開始讀。

---

## 9c. 5 個常見誤解

> 跟你周遭的「也在玩 AI」的人聊天前先看這節，會省你很多吵架時間。

| 誤解 | 真相 |
|---|---|
| **Agent = AGI（通用人工智能）** | 不是。Agent 是「LLM + 工具呼叫 + 自主決策 loop」。沒有意識、沒有自我目標、不會「想要」做什麼。 |
| **Agent 會取代我的工作** | 不會直接取代「人」，會取代「工作流程中可被結構化的部分」。會用 Agent 的人取代不會用的人，比 Agent 取代人來得快。 |
| **Agent 完全自主、不用人類** | 不對。最佳實踐是 **人類 in-the-loop**——關鍵決策、外部行動（付錢 / 寄信給客戶 / 改 production code）必須要人類 confirm。本書 Ch 8 / Ch 15 全章都在講「介入」設計。 |
| **Agent 不會出錯** | 會。常見錯包括：掰假 citation、cost 失控、loop 不停、reward hacking、安全漏洞。本書每章都有「常見地雷」一節。 |
| **Agent 都是同一回事** | 完全不對。Tool-use agent / ReAct / Plan-and-Solve / multi-agent / Agentic-RL 是 5 種不同範式，適用情境差很多。Ch 10 / Ch 14 / Ch 17 分開講。 |

---

## 10. 進入下一章前的心態

學 AI Agent 在 2025-2026 年是 moving target——這本書寫完出版的時候，又會冒出 3 個新框架、5 個新 MCP server、2 個新 LLM 公司。

**不要試圖把每個新東西都追完**。本書 18 章的順序設計是這樣：你學會原理之後，新東西進來只是「換個牌子」，你的本質判斷力不變。看到陌生的東西就回到「它是 LLM？是工具呼叫？是 framework？」三個分類去想，多數時候答案會自己出現。

下一章 [Ch 0 — 把工具裝好](../ch00_setup/) 開始動手。
