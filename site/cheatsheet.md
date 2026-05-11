---
title: 速查卡 Cheatsheet — 6 個分頁主題
description: AgentZ 速查卡分 6 個焦點頁面：CLI/Git · SDK · Pricing · Patterns · MCP/Skills · Governance。各頁 A4 可印一頁，不再擠在單頁。
---

# 速查卡 Cheatsheet

學完 AgentZ 後忘了哪個指令、模板、模型名、cost 公式時翻這裡。**分 6 個焦點頁面**，每頁可單獨列印 A4。

> 想要單頁全本？舊版 v1.2 single-page release 仍在 [GitHub releases](https://github.com/symbiosis11503/agent-z/releases)。新版分頁設計目的：每個焦點頁更短、更好查。

[[toc]]

---

## 速查 6 頁

| 主題 | 內容 | 何時翻 |
|---|---|---|
| 📟 [**CLI / Git**](./cheatsheet/cli) | Claude Code CLI 核心指令、CLAUDE.md 推薦結構、Git / Repo conventions | 忘了 slash command / commit message 寫法 |
| 🧪 [**SDK**](./cheatsheet/sdk) | Anthropic SDK basic / tool_use / streaming / Prompt Cache / 多家 SDK 對照 | 寫 API call 卡在 SDK syntax |
| 💰 [**Pricing**](./cheatsheet/pricing) | 11 家 LLM pricing 2026-05 + AgentZ 章節練習 cost 估算 | 不確定哪個 model 對應 budget |
| 🔁 [**Patterns**](./cheatsheet/patterns) | ReAct / Plan-and-Solve / Reflection 範式 + Cost cap fail-closed | 寫 agent loop 不知怎起手 |
| 🧩 [**MCP / Skills**](./cheatsheet/mcp) | FastMCP boilerplate + scope + Computer Use + Subagent + Skill auto-load + SKILL.md | 接 MCP / 寫 Skill / Computer Use |
| 🛡 [**Governance**](./cheatsheet/governance) | V3 4 道閘門 + 模型路由建議 + Anti-hallucination 5 條 | 上 production / 訓 research agent |

---

## Quick lookup

| 想找的 | 翻這頁 |
|---|---|
| `/cost` / `/mcp` / `/skill` 指令 | [CLI / Git](./cheatsheet/cli) |
| CLAUDE.md 模板 | [CLI / Git](./cheatsheet/cli) |
| Anthropic API `messages.create` 範例 | [SDK](./cheatsheet/sdk) |
| `stop_reason` 處理 | [SDK](./cheatsheet/sdk) |
| `cache_control: ephemeral` | [SDK](./cheatsheet/sdk) |
| Haiku / Sonnet / Opus 價格 | [Pricing](./cheatsheet/pricing) |
| 走完 AgentZ 預估花費 | [Pricing](./cheatsheet/pricing) |
| `react_loop()` snippet | [Patterns](./cheatsheet/patterns) |
| Cost cap `DAILY_CAP` pattern | [Patterns](./cheatsheet/patterns) |
| FastMCP `@mcp.tool()` boilerplate | [MCP / Skills](./cheatsheet/mcp) |
| `--scope project` MCP 指令 | [MCP / Skills](./cheatsheet/mcp) |
| `computer_20241022` tool 範例 | [MCP / Skills](./cheatsheet/mcp) |
| SKILL.md frontmatter | [MCP / Skills](./cheatsheet/mcp) |
| V3 4 道閘門 | [Governance](./cheatsheet/governance) |
| 哪個 task 用 Haiku / Sonnet / Opus | [Governance](./cheatsheet/governance) |

---

## 卡關速查

| 你在 | 看這頁 |
|---|---|
| 不知道哪章開始 | [Quick Win](./quickwin) / [Roadmap](./roadmap) |
| 哪家 LLM 申請 | [LLM / API 申請指南](./llm-providers) |
| 報錯不會修 | [故障排除](./troubleshooting) |
| 不確定該不該讀 | [FAQ](./faq) |
| 名詞看不懂 | [名詞表](./glossary) |
| 做完想 show off | [Capstone Gallery](./capstone) |

---

> 列印建議：個別頁面 Cmd-P / Ctrl-P 直接 A4 出。`@media print` 自動隱藏 nav / sidebar / 編輯連結等 chrome。

[首頁](/) · [完整章節](./chapters/ch-1_zero_basics/) · [GitHub](https://github.com/symbiosis11503/agent-z)
