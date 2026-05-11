# 故障排除指南 — Troubleshooting Compass

學員 / 操作員 / Builder 跑 agent 時常見的問題 + 解法，按症狀分類。**用瀏覽器 Ctrl-F 找關鍵字最快**。

> 這頁是各章節「常見地雷」段的彙整 + 全文搜尋友好版。詳細解釋見對應章節。
>
> 配套：[速查卡 Cheatsheet](./cheatsheet) — 不報錯但忘了哪個指令時翻這頁。

[[toc]]

---

## 環境 / 安裝

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| `claude` command not found | npm 沒裝起來 / PATH 沒設 | `npm i -g @anthropic-ai/claude-code` 後 `which claude` 確認 | [Ch 4](./chapters/ch04_cli_agents/) |
| `ANTHROPIC_API_KEY not set` | 沒 export env var | 加到 `~/.zshrc` 或 `~/.bashrc`: `export ANTHROPIC_API_KEY="sk-ant-..."` | [Ch 4](./chapters/ch04_cli_agents/) |
| `Node version too low` | Node < 18 | `nvm install 20` 或升級 Node | [Ch 4](./chapters/ch04_cli_agents/) |
| pip install 衝突 | 全域 Python 髒 | 用 `uv venv` 或 `python -m venv .venv` 隔離 | [Ch 0](./chapters/ch00_setup/) |
| WSL2 路徑慢 | Windows / WSL 跨檔案系統 | 把 repo 放在 `~/` (Linux FS) 不要放 `/mnt/c/` | [Ch 0](./chapters/ch00_setup/) |

---

## API / 金鑰 / 認證

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 401 Unauthorized | key 錯 / revoked | 重新 [Anthropic Console](https://console.anthropic.com/) 生 key 並 export | [Ch 0](./chapters/ch00_setup/) / [LLM 申請](./llm-providers) |
| 429 Rate limit | 短時間太多 request | exponential backoff retry，或升級 tier | [Ch 8](./chapters/ch08_cost_observability/) |
| `Invalid API key format` | sk-ant- 跟 sk-or- 混 | 各家 key 開頭不同 (Anthropic `sk-ant-`, OpenAI `sk-`, Groq `gsk_`) | [LLM 申請指南](./llm-providers) |
| key 進 git commit | 不小心 push 上 GitHub | **立刻 rotate key** + `git filter-branch` 移除 history | [Ch 8](./chapters/ch08_cost_observability/) / [CONTRIBUTING](https://github.com/symbiosis11503/agent-z/blob/main/CONTRIBUTING.md) |
| 沒信用卡無法綁 | Anthropic / OpenAI 需信用卡 | 改用 Groq 免費 / Gemini 免費 / Ollama 本地 | [FAQ](./faq#q-沒信用卡綁-api-怎麼辦) / [LLM 申請](./llm-providers) |

---

## Cost / 預算 / 失控

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 帳單一個月 $500 | 沒設 monthly limit | console.anthropic.com Billing → set $20 monthly cap | [Ch 8](./chapters/ch08_cost_observability/) |
| 一個 task 燒 $5 | 沒 per-run cost cap | 包 `cost_tracker.py` 每 call 預估 + 超 cap fail-closed | [Ch 8 starter](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch08_cost_observability) |
| retry 燒 5x cost | retry policy 沒算錢 | retry 也計入 budget, 用 exponential backoff | [Ch 8](./chapters/ch08_cost_observability/) |
| log cost 跟帳單對不起 | PRICING dict 過期 | 每月對 [Anthropic pricing](https://www.anthropic.com/pricing) refresh | [Ch 8](./chapters/ch08_cost_observability/) |
| prompt 重複付全錢 | 沒用 cache_control | 大 system prompt 用 `cache_control: ephemeral` beta，省 90% | [Ch 8](./chapters/ch08_cost_observability/) |

---

## Agent loop / 行為

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| Agent 跑無限步 | 沒 max_steps | `for _ in range(N):` + 偵測 thought 重複 break | [Ch 9](./chapters/ch09_function_calling/) / [Ch 12](./chapters/ch12_mini_framework/) |
| Reflection 永遠 reject | reviewer 太苛刻 | reviewer rubric 寫 measurable criteria + max iterations 3 | [Ch 10](./chapters/ch10_react_paradigms/) |
| ReAct loop 跑同 tool 50 次 | 沒 dedup 偵測 | 偵測「同 thought + 同 input」直接 break | [Ch 12](./chapters/ch12_mini_framework/) |
| Plan 階段太樂觀 step 3 卡住 | plan 沒 mid-way revise | 每完成一步 review plan 允許改 | [Ch 10](./chapters/ch10_react_paradigms/) |
| Agent 亂走不照規則 | system prompt 規則太多 / 矛盾 | CLAUDE.md audit, 同一檔內規則不能衝突 | [Ch 5](./chapters/ch05_cli_workflow/) |
| `/clear` 後失憶 | session memory 沒持久化 | 重要 context 寫 CLAUDE.md / SKILL 或用 memory MCP | [Ch 4](./chapters/ch04_cli_agents/) / [Ch 13](./chapters/ch13_memory_rag/) |

---

## Tool use / function calling

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| `expected tool_result for tool_use_id` | 漏 append tool_result | 收到 `stop_reason='tool_use'` 必加 `{"type":"tool_result", "tool_use_id":..., "content":...}` | [Ch 9](./chapters/ch09_function_calling/) |
| LLM 漏傳參數 | input_schema 沒寫 `required` | input_schema 加 `"required": ["arg1", "arg2"]` | [Ch 9](./chapters/ch09_function_calling/) |
| LLM 不知何時 call tool | description 寫太空 | description 寫「**何時用 + 輸入 + 輸出**」3 段 | [Ch 9](./chapters/ch09_function_calling/) / [Ch 6](./chapters/ch06_mcp/) |
| Parallel tool 只處理 1 個 | iterate 漏接 | `for block in resp.content if block.type == "tool_use"` 全接 | [Ch 9](./chapters/ch09_function_calling/) |
| tool 回 None 報錯 | LLM 收 null 亂答 | tool 一定 return 非空 str/dict, None → `"(empty)"` | [Ch 12](./chapters/ch12_mini_framework/) |

---

## MCP

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| `/mcp` disconnected | command path 找不到 | 用絕對路徑 / `which uv` 確認 / 看 stderr log | [Ch 6](./chapters/ch06_mcp/) |
| stdio mode JSON-RPC 解析錯 | server `print()` 弄壞 stdout | server 內 `print(..., file=sys.stderr)`, stdout 給 MCP | [Ch 6 starter](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch06_mcp) |
| 改 server 後沒生效 | Claude Code 沒重啟 | `/exit` 重新 `claude` | [Ch 6](./chapters/ch06_mcp/) |
| server 一個 tool fail 整個 crash | tool 自己會 raise | 每 tool try/except return `{"error": "..."}` | [Ch 6](./chapters/ch06_mcp/) |

---

## Memory / RAG

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| retrieval 不準 | chunk 切太大 / 太小 | 中文 200-500 字 / 英文 500-1000 token, overlap 50-100 char | [Ch 13](./chapters/ch13_memory_rag/) |
| 舊資料 retrieval 全錯 | embedding model 換版 | embedding model + version 寫死 / 升級全 re-embed | [Ch 13](./chapters/ch13_memory_rag/) |
| 答案被無關文件淹沒 | 沒 metadata filter | 加 `where={"category": "policy"}` | [Ch 13](./chapters/ch13_memory_rag/) |
| 第 30 輪對話 context 撞 200K | session memory 沒截斷 | 用 summarizer 每 10 輪壓 1 段 | [Ch 13](./chapters/ch13_memory_rag/) |
| PII 進 vector DB | 沒 mask 直接索引 | 索引前 mask 姓名 / 電話 / email | [Ch 13](./chapters/ch13_memory_rag/) |

---

## Multi-agent

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 簡單任務拆 5 agent debug 變難 | 過度 multi-agent | prompt 能解就別拆 | [Ch 14](./chapters/ch14_multi_agent/) |
| Supervisor 自己做事不派 worker | system prompt 沒禁 | 寫死「不能自己做、只能 delegate」 | [Ch 14](./chapters/ch14_multi_agent/) |
| Pipeline stage 失敗整條斷 | 沒 retry | 每階段 try/except + retry 1 次再 fail-out | [Ch 14](./chapters/ch14_multi_agent/) |
| 4 agent 平行 + Sonnet 燒 $1/run | 全用大 model | summarizer Haiku, final Sonnet/Opus | [Ch 14](./chapters/ch14_multi_agent/) |
| supervisor 回非 JSON | LLM 自由發揮 | system prompt 強制 + parse fail fallback to ask user | [Ch 14 starter](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch14_multi_agent) |

---

## Production deploy / governance

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 出事不知道發生啥 | 沒 audit log | 每 LLM/tool call 寫 SQLite 7 欄 (ts/run_id/event/payload/cost/error/duration) | [Ch 15](./chapters/ch15_deploy_audit_replay/) |
| replay 不能 reproduce | log 缺欄位 | replay record 含 input + output + model + temperature + seed | [Ch 15](./chapters/ch15_deploy_audit_replay/) |
| HTTP /run 等 60s 才回 | 同步阻塞 | background_task + run_id polling 或 SSE streaming | [Ch 15](./chapters/ch15_deploy_audit_replay/) |
| `database is locked` | 多 process 寫 SQLite | WAL mode 或升 PostgreSQL | [Ch 15](./chapters/ch15_deploy_audit_replay/) |
| runaway agent 無法 abort | 沒 cancellation | `/runs/{id}/abort` endpoint + agent 每 tick check flag | [Ch 15](./chapters/ch15_deploy_audit_replay/) |
| log 含 API key 外洩 | 沒 redact | mask `sk-*` / `sk-ant-*` / `key=*` pattern | [Ch 15](./chapters/ch15_deploy_audit_replay/) |

---

## 框架 / Skills / Plugins

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 單 agent 用 CrewAI 三倍 code | 框架選錯 | 單 agent → vanilla / Pydantic AI; 多 role → CrewAI | [Ch 11](./chapters/ch11_frameworks/) |
| 框架升級整個系統重寫 | 直接綁 framework API | 寫 adapter layer, 換框架只動 adapter | [Ch 11](./chapters/ch11_frameworks/) |
| Skill 不出現在 `/skill` | frontmatter 缺 name 或 description | `---` 區內必填 `name` + `description` | [Ch 7](./chapters/ch07_skills_plugins/) |
| LLM 誤觸發 Skill | description 太空 / 太細 | description = 「**何時用 + 做什麼**」一句話 <150 字 | [Ch 7](./chapters/ch07_skills_plugins/) |
| Skill 自動 commit / push 損失 | 沒 confirmation gate | Constraints 段「Never commit/push/delete without approval」 | [Ch 7](./chapters/ch07_skills_plugins/) |

---

## Researcher / RL (進階)

| 症狀 | 原因 | 解法 | 章節 |
|---|---|---|---|
| 掰假 citation | 沒 grounding | 強制 DOI verify + Reflection fact-check 5 條 | [Ch 16](./chapters/ch16_researcher/) |
| LLM 把 abstract 假裝讀全文 | paywall + 沒區分 | 「abstract 內容」 vs 「full-paper 推論」分開 prompt | [Ch 16](./chapters/ch16_researcher/) |
| GPU OOM | model 太大 | 4-bit + LoRA + 降 batch size | [Ch 17](./chapters/ch17_builder_advanced/) |
| metric 飆升但實際變爛 | reward hacking | 加 eval 跑真實任務 + human spot-check | [Ch 17](./chapters/ch17_builder_advanced/) |
| fine-tune 後通用能力降 | catastrophic forgetting | LoRA 替全參 + KL penalty + retain set | [Ch 17](./chapters/ch17_builder_advanced/) |

---

## Web / Site / VitePress

| 症狀 | 原因 | 解法 |
|---|---|---|
| 看不到 LLMTryout 元件 | 瀏覽器 cache 舊 | hard refresh `Cmd-Shift-R` / `Ctrl-Shift-R` |
| 互動試玩按了沒反應 | API key 沒輸入 | LLMTryout 頂部設 API key 才會 enable 按鈕（不上傳） |
| 行動裝置 sidebar 切不開 | mobile menu | 點左上 hamburger icon |

---

## 還是卡關

1. **搜索本頁**：Ctrl-F 找關鍵字
2. **看對應章節常見地雷**：[18 章節都有「## 常見地雷」段](./roadmap)
3. **看 [FAQ](./faq)**：22 題 6 大類常見問題
4. **看 starter code**：[每章對應 dir](https://github.com/symbiosis11503/agent-z/tree/main/starter-code) 有 working version
5. **開 [GitHub Discussion](https://github.com/symbiosis11503/agent-z/discussions)**：問題公開 + 答案幫到後人
6. **報 bug**：[Open Issue](https://github.com/symbiosis11503/agent-z/issues) 附 OS / Python / SDK 版本 + 錯誤訊息

---

[首頁](/) · [FAQ](./faq) · [Roadmap](./roadmap) · [LLM / API 申請](./llm-providers)
