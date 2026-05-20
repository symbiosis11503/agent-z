---
title: Ch 8 — Cost 觀測 / 介入
description: Token 預算 / 三個常見燒錢 pattern / cost cap fail-closed pattern / 介入機制。
---

# Ch 8 — Cost 觀測 / token 預算 / 介入

> **45-60 分鐘**。讀完你會懂：怎麼追蹤 agent 花多少錢、設預算上限、看失敗模式、長 task 怎麼中斷、預防爆炸。
>
> 動手練習：算一次 agent 跑完真實花了多少、設一個 budget cap、強制中止一個 runaway agent。
>
> 前置：完成 [Ch 7](../ch07_skills_plugins/) — Skills 寫得出來。
>
> 🛠 **Starter code**: [`starter-code/ch08_cost_observability/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch08_cost_observability) — drop-in Anthropic SDK wrap + SQLite log + daily cap fail-closed + by_model/by_run report + 7 條常見地雷。

---

## 1. 為什麼這章重要？

CLI agent 很危險的一個特性：**一個指令可能 call 幾百次 LLM**。

你打：「幫我把整個 codebase migrate 從 Python 3.9 到 3.12 + 更新所有 dependency」

agent 可能：
- 跑 200 次 LLM call
- 讀 500 個檔案
- 寫 100 個檔案
- 花 30 分鐘
- 燒 $5-15

如果你沒看著、設好上限，它可能：
- 卡在無限 loop（一直改 / 一直 lint / 一直跑 test）
- 花掉你整個月的 API budget
- 改錯方向（你以為 plan 對，結果方向錯，改了 100 個檔案要 revert）

**Operator 階段最後一章專門講這個——不會控成本跟介入，Builder 階段更危險。**

---

## 2. 三個觀測層次

### 2.1 Token 層 (最細)

每次 LLM API call 回的 `usage`：
```json
{
  "input_tokens": 1234,
  "output_tokens": 567,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 0
}
```

乘 pricing → 這次 call 多少錢。

Claude Code 內建 `/cost` 指令看當前 session 累積。

### 2.2 Run 層

一個 agent run 從你輸入指令到拿到答案 — 包含 N 次 LLM call。Claude Code 會 print 像：
```
Tokens used: 12,345 input / 3,456 output  ($0.12)
Time: 2m 14s
```

### 2.3 Day / Month 層

長期帳：到 Anthropic / OpenAI Console 看每日 token + spend。**設帳號層級的硬上限**（多數家都有 monthly cap 可設）。

---

## 3. 三個常見「燒錢失敗模式」

### 3.1 Tool loop

agent 重複 call 同一個 tool 想求結果：
```
read file A → modify → run lint → fail → read A again → modify → run lint → fail → ...
```

每 loop ~10K token，10 圈就 100K token + $1+。

**症狀**：你發現 task 跑超久但進度停滯。

### 3.2 Context bloat

agent 把太多 file 讀進 context（fast scan 一次讀 50 個 file），每次 LLM call 都帶這 50 個 file 進 prompt：

```
input_tokens 每輪 = 50 files × 平均 2K token = 100K
10 輪 LLM call = 1M input token = $3 / round
```

**症狀**：對話越聊越貴，每個 turn cost 飆升。

### 3.3 Runaway plan

agent 自己擴張 scope。你說「修這個 bug」，它變「修 bug + 重構這 module + 加 test + 寫 doc」。

**症狀**：你的 git diff 看了傻眼，完全超過你 ask 的範圍。

---

## 4. 怎麼預防 / 介入？

### 4.1 設 budget cap

Claude Code 在 settings.json：

```json
{
  "costBudgetUSDPerRun": 1.0,
  "costBudgetUSDPerDay": 10.0
}
```

超過會自動暫停問你（pre-flight 不會精準，但比沒有好）。

V3 / 自己寫 agent 一定要有 cost cap。後面 Ch 15 會講怎麼自己實作。

### 4.2 階段性確認（Plan-first）

Ch 5 講過的 Search → Plan → Execute → Verify。**Plan 階段 plan-only**，不動 code 不花太多 token，你 review plan 再 execute。

### 4.3 強制中止：Ctrl+C / `/abort`

agent 跑到一半你覺得方向不對 — **不要等它跑完**：
- Claude Code: `Ctrl+C` 立刻中止當前 turn，下一輪你可以更正方向
- `/abort` 中止整個對話、清 context

### 4.4 Hook 攔截

Ch 5 講的 hook 可以做 PreToolUse 攔截：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "echo $TOOL_INPUT | grep -v 'rm -rf /' || exit 1" }]
    }]
  }
}
```

意思：agent 想跑 bash 但 input 含 `rm -rf /` 直接擋。

### 4.5 用便宜 model 跑 routine 部分

`/model claude-haiku-4-5` 切便宜 model。Haiku 4.5 比 Sonnet 便宜 5x，多數重複動作（讀檔 / lint / format）用 Haiku 就夠。

---

## 5. 一個真實 cost 估算

以下是我（CC）在 V3 開發某天的真實數字（2026-05）：

| 任務 | LLM call 次數 | token in | token out | cost (USD) |
|---|---|---|---|---|
| 寫一個 module + test（150 行） | 18 | 89K | 12K | $0.32 |
| Debug 一個 race condition | 35 | 287K | 23K | $0.95 |
| Refactor + cross-check（含 sub-agent） | 56 | 412K | 41K | $1.85 |
| 改 doc 50 處 typo | 4 | 18K | 5K | $0.07 |
| **整天 (3 hr coding)** | **231** | **1.4M** | **148K** | **$5.40** |

**重點**：debug 跟 refactor 比寫 new code 貴 3-5x（context 大、call 多）。寫 code 反而比看 code 便宜。

### 5.1 2026-05 多 vendor token 單價對照

要算自己 cost 前先有單價。下表 2026-05 主流 LLM API token 單價（USD per 1M token），按單價遞增：

| Model | Input ($/1M) | Output ($/1M) | Vendor | 適合場景 |
|---|---|---|---|---|
| DeepSeek-Chat V3 | $0.27 | $1.10 | DeepSeek | 中文 / cost-sensitive batch |
| Gemini 2.5 Flash | $0.30 | $2.50 | Google | high-volume / 多模態 routine |
| Claude Haiku 4.5 | $1.00 | $5.00 | Anthropic | 大量 routine action / read-only / lint |
| Gemini 2.5 Pro | $1.25-2.50 | $10-15 | Google | 跨模態 reasoning |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Anthropic | agent coding 主力（Claude Code 預設） |
| GPT-4o | $5.00 | $15.00 | OpenAI | 與 Sonnet 同 tier，OpenAI 生態 |
| GPT-4 (legacy) | $30.00 | $60.00 | OpenAI | 已老化、不建議新案 |
| Claude Opus 4.6 | $15.00 | $75.00 | Anthropic | critical reasoning / cross-check / 1M context 用 |

**快速估算公式**：`月成本 ≈ 月 task 數 × 平均 token/task × (input_price × 80% + output_price × 20%) / 1M`

範例：每月 1000 task、平均 100K token、用 Sonnet 4.6（$3/$15）：`1000 × 100,000 × (3×0.8 + 15×0.2)/1,000,000 = 1000 × 0.1 × 5.4 = $540/月`

**省錢三招**：
1. **路由不同 tier** — routine（lint / format / read）走 Haiku 4.5；critical reasoning 走 Sonnet 4.6；cross-check 才用 Opus 4.6。同任務可省 60-80%。
2. **Prompt Cache** — 重複 system prompt 用 Anthropic cache_control（4 個 break point）+ OpenAI prompt cache、命中折扣 50-90%（依 vendor）。
3. **不要 hard-code 單價** — 寫 `MODEL_PRICING` 設定檔，每月對 vendor pricing page 校（[Anthropic](https://www.anthropic.com/pricing) / [OpenAI](https://openai.com/api/pricing) / [Google](https://ai.google.dev/pricing)）— 單價變動就改設定不改 code。

⚠️ 上表為 2026-05-12 snapshot — 單價變動快，**部署前必查官方 pricing page**。完整 11 家對照（含 OpenRouter aggregator + DeepSeek / Groq / Mistral / Llama 自架）見 [LLM Providers · 商業 API](../../site/llm-providers/commercial.md) 與 [Cheatsheet · Pricing](../../site/cheatsheet/pricing.md)。

---

## 6. Anthropic 訂閱 vs API pay-as-you-go

如果你常用 Claude Code，**訂閱通常比 API token 划算**：

| 方案 | 月費 | 適合 |
|---|---|---|
| Claude Pro | $20 | 偶爾用 / 個人實驗 |
| Claude Max ($100) | $100 | 中量使用 / 每天 1-2hr coding |
| Claude Max ($200) | $200 | 重度使用 / 全天 coding |
| API token | pay-as-you-go | 自寫 agent / 多人用 |

訂閱 Claude Code 走 OAuth bridge，token 不限制（但有 rate limit）。重度 coding 一天可能 $5-10 token 帳，月帳就 $200-300，那訂閱就賺。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 4 — Failure Modes**：context decay / attention degradation / runaway agent
- **Section 7 — Work Modes**：human-in-the-loop / cost monitoring / accept-edits

---

## 8. 動手練習

### 練習 8.1：算真實 cost

挑一個你最近做的 task（修 bug / 寫 module / 寫 doc 任一），用 Claude Code 重做一次，記錄：

| 指標 | 數字 |
|---|---|
| `/cost` 顯示總 cost | $ |
| LLM call 次數 | |
| 用了多少 token in / out | |
| 你 cost 跟自己預想的差多少？（高 / 低 / 一樣） |

**成功標準**：四欄全填，cost 算對。

### 練習 8.2：跑一個 runaway，故意停下

故意給 agent 一個會 over-do 的指令（例：「幫我把這 module 改更好」），跑 1 分鐘後 `Ctrl+C` 中止。

回答：
- agent 中止前已經改了多少檔案？
- 你 revert 用了多少時間？
- 下次怎麼設計 prompt 避免 over-do？

**成功標準**：理解中止 + revert 的成本，會用更明確 prompt。

### 練習 8.3：設 budget cap

在你 `~/.claude/settings.json` 加：

```json
{ "costBudgetUSDPerRun": 0.5, "costBudgetUSDPerDay": 5.0 }
```

跑一個會貴的 task，看到 budget 警告。
**成功標準**：實際看到 budget 觸發、agent 停下來問你。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 token / run / day 三層觀測
- [ ] 知道 3 個常見燒錢失敗模式（tool loop / context bloat / runaway plan）
- [ ] 會設 budget cap
- [ ] 會在跑到一半中止 (`Ctrl+C`)
- [ ] 知道 hook 能攔截危險動作
- [ ] 知道訂閱 vs API token 怎麼選
- [ ] 跑完練習 8.1 / 8.2 / 8.3

打勾 5 個以上，恭喜——**Operator 階段完工**！

---

## Operator 階段（Ch 4-8）回顧

你現在會什麼：
- 4 家主流 CLI agent 都裝得起來、會選
- CLAUDE.md / slash command 寫得出
- 知道 MCP 是什麼、會接也會寫
- 知道 Skill 跟 MCP 差別、能用 Progressive Disclosure 寫 Skill
- 控成本、會在跑爆前中止

下一階段（**Builder**, Ch 9-15）：你會**自己寫 agent**，不再只是用別人的。

---

## 9a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **沒設 monthly limit** | 帳單一個月 $500 | Anthropic Console / OpenAI Billing 都有 monthly limit, 學習階段設 $20 |
| **PRICING 寫死過期** | 帳單跟 log 對不起來 | 每月對 [vendor pricing page](https://www.anthropic.com/pricing) 校；用 cost tracker 抽成設定檔 |
| **retry 也算 cost** | 失敗 retry 5 次燒 5x | retry policy 寫進 budget; 429 retry 用 exponential backoff |
| **prompt cache 沒用** | 大 system prompt 每次都付全錢 | 用 `cache_control` beta 把 system prompt cache 1 hr, 可省 90% |
| **streaming 不關 connection** | 算 cost 算到中斷後也累計 | 收到 `message_stop` 確認 token 後才結算 |
| **多 process 寫 SQLite** | `database is locked` | WAL mode 或升 PostgreSQL |
| **estimate vs actual 對不起來** | pre-flight 估 200 token 實際燒 1000 | estimate 用 tiktoken-like lib 加 20% buffer |
| **沒 per-user cap** | 一個 user 燒爆所有人 budget | 加 user_id quota，per-user daily / hourly cap |
| **prod 跟 dev 共 quota** | dev 試壞 prod 也炸 | 不同 API key + 不同 cost db |
| **/cost 數字看了不行動** | 看到燒 $1 還繼續跑 | 自動化 trip wire（程式攔截），不靠人類紀律 |

---

## 9b. 在這頁讓 LLM 分析你的 cost trace

把你最近一次 agent run 的 token 數字貼進去，看 LLM 怎麼診斷：

<LLMTryout
  title="Ch 8 in-page tryout — cost trace 診斷"
  defaultSystem="你是 agent cost analyst。看使用者提供的 token / call / 時間數字，診斷有沒有 3 個常見失敗模式（tool loop / context bloat / runaway plan），並建議怎麼改 prompt 或設 cap。回繁中。"
  defaultPrompt="我的 agent 跑一個「重構這個 module」task，花了 87 次 LLM call、142K input token、18K output token、跑 8 分鐘。診斷一下。" />

## 10. 補充閱讀

- [Anthropic — Cost optimization guide](https://docs.anthropic.com/en/docs/build-with-claude/optimization)
- [Claude Code — settings reference](https://docs.claude.com/en/docs/agents-and-tools/claude-code/settings)
- ai-dict Failure Modes 段：https://ai-dict.gh.miniasp.com/
- 後面 **Ch 15 會用 Helix V3 的 cost cap / audit / replay 當完整 case study**

---

> 🛟 **卡關時看這裡**：
> - cost 燒太兇 / runaway loop → [故障排除 § Cost/預算](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - cost cap pattern fail-closed code + Prompt Cache (省 90%) → [速查卡 § Cost cap](https://symbiosis11503.github.io/agent-z/cheatsheet/patterns#cost-cap-pattern)
> - 名詞看不懂 → [70+ 名詞表](https://symbiosis11503.github.io/agent-z/glossary)
