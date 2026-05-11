---
title: 速查卡 — CLI / CLAUDE.md / Git
description: Claude Code CLI 核心指令、CLAUDE.md 推薦結構、Git / Repo conventions。A4 可印一頁。
---

# 速查卡 · CLI / CLAUDE.md / Git

[← 回速查卡總覽](../cheatsheet)

## Claude Code CLI 核心指令

```bash
claude                          # 起 Claude Code
claude --plan                   # 開 plan mode 起手
/help                           # 看 builtin commands
/cost                           # 看當前 session 花費
/mcp                            # MCP server status
/skill                          # 看 / 切換 skill
/clear                          # 清 context
/resume                         # 從上次 session 接著跑
/exit                           # 離開
Esc                             # 中斷當前 task
Ctrl-C × 2                      # 強制 exit
```

## CLAUDE.md 推薦結構

```markdown
# 專案規則

## 角色
- 你是 X 工程師，負責 Y。

## 風格
- 繁中、簡潔、不廢話
- 改 code 前先說「我要 X」

## 規則
- 不 force push
- 不 commit 不 review 過的 secret
- 改 prod 前要 confirmation

## 不要
- 不要寫測試（這個專案沒測試框架）
- 不要重構（保持 minimal change）

## 工具
- 我們用 X 不用 Y
```

## Git / Repo conventions

```bash
git checkout -b <type>/<feature>     # type: feat / fix / docs / chore
# 寫 code
git add <specific files>             # 不要用 git add -A
git commit -m "feat: add ..."        # imperative mood
git push origin <branch>
gh pr create --title "..." --body "..."  # 用 gh, 不要去 web
```

Commit message 範例：
```
feat: add cost cap fail-closed pattern (Ch 8)

- DAILY_CAP env var
- pre-flight check today's total
- raise CostCapExceeded with explicit message

Closes #42
```

---

**下一頁** → [SDK 速查](./sdk) · [Pricing](./pricing) · [Patterns](./patterns) · [MCP / Skills](./mcp) · [Governance](./governance)
