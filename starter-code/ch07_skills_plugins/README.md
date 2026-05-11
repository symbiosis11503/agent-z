# Ch 7 — Skills / Plugins starter

對應 [AgentZ Ch 7](../../chapters/ch07_skills_plugins/) 練習 7.1 / 7.2 / 7.3。

## 什麼是 Skill?

Claude Code 的 Skill = **一個資料夾 + SKILL.md**，告訴 Claude「在 X 情境下、按 Y 步驟做事」。

跟 MCP 差別：
- **MCP** = 給 Claude 新的**工具**（read_file, send_email...）
- **Skill** = 給 Claude 新的**工作流程**（「我看到這個情境時 → 走這個 SOP」）

## 這個資料夾包什麼

```
example-skill/
└── SKILL.md   ← skill 主體
```

實際 skill 可以有更多檔案：
- `SKILL.md` (必填)
- `scripts/*.sh` (skill 內的 helper)
- `templates/*.md` (skill 用的模板)
- `README.md` (使用說明、給人讀的)

## 範例 skill 在做什麼

`example-skill/SKILL.md` 寫了一個「Changelog Helper」skill — 用戶說「更新 CHANGELOG」時，Claude 自動：

1. 讀現在的 CHANGELOG.md 學格式
2. 跑 `git log` 看最近改了什麼
3. 問用戶版本號 / 類別 / 摘要
4. 按既有格式產生新 entry
5. 插入檔案，**不自動 commit**（用戶 review 才 commit）

## 怎麼裝這個 skill 進 Claude Code

### Project-scope (這個 repo 內生效)
```bash
mkdir -p .claude/skills
cp -r example-skill .claude/skills/changelog-helper
```

### User-scope (你所有 Claude Code session 都能用)
```bash
mkdir -p ~/.claude/skills
cp -r example-skill ~/.claude/skills/changelog-helper
```

重啟 Claude Code（`/exit` 後重開）。

## 測試

在 Claude Code 內：

```
/skill changelog-helper
```

或直接問：「幫我更新 CHANGELOG」。

Claude Code 會自動 invoke 這個 skill，按 SKILL.md 寫的步驟跑。

## SKILL.md 格式（重點）

```markdown
---
name: my-skill-name           ← 必填，slash 命令用這個
description: 一句話講 skill 做什麼。Claude 用這個判斷何時 invoke。
---

# Skill 名稱

## When to invoke         ← 觸發條件
User says ...

## What you do            ← 步驟
1. ...
2. ...

## Constraints            ← 限制 (不該做什麼)
- Never commit without approval
- Use existing format

## Example                ← 1-2 個範例對話
```

## 練習

- **7.1**: 寫一個 `lint-md` skill — 跑 markdownlint 在當前資料夾的 .md 檔
- **7.2**: 寫一個 `pr-description` skill — 看 `git log` 自動寫 PR 描述（標題 / Summary / Test plan）
- **7.3**: 寫一個 `commit-message` skill — 看 staged diff 寫繁中 commit message + Co-Authored-By trailer

## 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| frontmatter 漏 `name` | skill 不出現 | `---` block 內必填 name + description |
| description 寫太細 | Claude 不知道何時 invoke | description = 「**何時用 + 做什麼**」一句話 |
| 步驟太長 | Claude 漏步驟 | < 7 步，超過拆成多 skill |
| 跨檔案路徑寫死 | 別人 clone 跑不起來 | 用相對路徑或讓 skill 自己 detect |
| 自動執行危險操作 | 把工作搞砸 | 「Never commit/push/delete without approval」 |
| skill 名衝突 | 兩個 skill 都叫 changelog-helper | project-scope 蓋過 user-scope |

## 進階：Plugin / Marketplace

Skill 是「one folder one skill」。**Plugin** 是「一包多 skill + MCP server + commands」打包散發：

```
my-plugin/
├── plugin.json
├── skills/
│   ├── changelog-helper/
│   │   └── SKILL.md
│   └── pr-helper/
│       └── SKILL.md
├── mcp-servers/
│   └── my-tools/
│       └── server.py
└── commands/
    └── /custom-command.md
```

**Marketplace** = plugin registry — 一個 git repo 含 plugins/，用戶 `/plugin install <repo>` 一次裝全套。

## 補充閱讀

- [Claude Code Skills docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills)
- [Claude Code Plugins](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/plugins) — Marketplace 完整概念
- AgentZ [Ch 7 章節](../../chapters/ch07_skills_plugins/) — Progressive Disclosure 設計 pattern
- [Awesome Claude Code Skills (community catalog)](https://github.com/hesreallyhim/awesome-claude-code) — 抄這個改
