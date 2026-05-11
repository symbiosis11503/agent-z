# Ch 7 — Skills / Plugins / Marketplace

> **60-75 分鐘**。讀完你會懂：Skill 是什麼、跟 MCP 差在哪、為什麼 2025 變熱、寫第一個 Skill、Plugin / Marketplace 怎麼運作。
>
> 動手練習：寫一個自己的 Skill、從 Marketplace 裝一個、用 progressive disclosure 設計第三個。
>
> 前置：完成 [Ch 6](../ch06_mcp/) — 已經會裝 MCP server + 自己寫一個。
>
> 🛠 **Starter code**: [`starter-code/ch07_skills_plugins/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch07_skills_plugins) — changelog-helper SKILL.md template + project / user-scope install + 6 條常見地雷。

---

## 1. Skill 跟 MCP 差在哪？

新手最常問。簡單答案：

| 比較項 | MCP | Skill |
|---|---|---|
| **是什麼** | 工具（給 LLM call） | 文件 + 程式碼 + 規則的包（給 LLM 讀） |
| **觸發** | LLM 主動 call | LLM 看到觸發條件主動載入 |
| **內容** | function + schema | markdown SOP + 可選 reference files + 可選 script |
| **狀態** | server 跑 / 接 API | 純檔案（沒進程） |
| **何時用** | 動態查詢 / 動態執行 | 固定流程 / 規範 / 領域知識 |

**最簡單記法**：
- **MCP = 函式庫**（要 call 才執行）
- **Skill = 規格書 + cheat sheet**（LLM 讀完照做）

舉例：
- 「查 Notion 某個 page」→ MCP（要 API call）
- 「公司寄客戶信的 5 步驟 SOP」→ Skill（規則 + 範例 template，不需 API）

> 💡 一個任務常常**兩個都要**：Skill 告訴 LLM「按 SOP 走」，SOP 第 3 步 call MCP server 真的寄信。

---

## 2. Skill 的內部結構

一個 Skill 就是一個 directory：

```
.claude/skills/email-customer/
├── SKILL.md            # 主檔案（必要）
├── reference/
│   ├── tone-guide.md   # 詳細參考（按需載入）
│   └── examples.md
└── scripts/
    └── send.sh         # 可執行（按需呼叫）
```

`SKILL.md` 的 frontmatter：

```markdown
---
name: email-customer
description: 寫客戶寄信，遵照公司 5 步驟 SOP 跟 tone guide
---

# 寄客戶信 SOP

1. 確認收件人姓名 + 公司名（如果使用者沒給就先問）
2. 確認信件目的（自選或請使用者選）：[詢價 / 報價 / 道歉 / 通知 / 致謝]
3. 依目的選 template（見 `reference/examples.md`）
4. 寫 draft，**先問使用者再寄**
5. 使用者批准後 → 呼叫 `scripts/send.sh`

## tone 原則
- 開頭稱呼用「親愛的 X 先生 / 小姐」
- 結尾用「敬祝 商祺」
- 詳細風格請讀 `reference/tone-guide.md`

## 不可
- 不要主動寄沒 review 的信
- 不要批評客戶
- 不要在信裡放內部 ID / token
```

---

## 3. Progressive Disclosure — Skill 的核心設計 pattern

LLM 每多載入一段文字 = 多花 token + 注意力被分散。所以 Skill 設計的目標是：

**只在需要時載入細節**。

### 三層 disclosure

```
Level 1: SKILL.md frontmatter (always loaded)
         description + 一句話功能簡介
         ↓
Level 2: SKILL.md 主體 (matched 時載入)
         觸發後完整步驟、原則、不可做
         ↓
Level 3: reference / scripts (LLM 主動載入)
         細節 SOP、範例、可執行腳本
```

寫得好的 Skill：
- frontmatter 描述精準（不會誤觸發）
- 主檔短（< 500 行）
- 細節都在 reference/，按需讀

寫得爛的 Skill：
- 把所有 reference 全塞進 SKILL.md → 每次 match 都 load 一大塊
- frontmatter 寫得模糊 → LLM 亂載入

---

## 4. Skill 怎麼觸發？

Claude Code 看到 user prompt + context 判斷：「這次任務有沒有對應的 Skill？」如果 SKILL.md 的 description 跟當前情境匹配，自動載入。

例如：
```
> 幫我寫一封信給洽億的 Bacon 客戶
```

Claude Code 看到「寫信給客戶」→ 載入 `email-customer` Skill。

也可以**手動觸發**：

```
> /skill email-customer 幫我寫信給 Bacon
```

---

## 5. Plugin = Skill + 設定 + 模板 的包

Plugin 是「給整個團隊用」的 Skill 包裝。一個 plugin 通常包含：

- 多個 Skills
- 預設的 settings.json
- MCP server 設定（一鍵裝）
- slash commands

例如 Anthropic 官方的 **claude-code-guide** plugin，就把 Claude Code 自己的文件、常用 hook、推薦設定包成一包。

Plugin 用 `.claude-plugin/plugin.json` manifest：

```json
{
  "name": "claude-code-guide",
  "version": "1.0.0",
  "description": "Anthropic 官方 Claude Code 文件助手",
  "skills": ["skill-1", "skill-2"],
  "mcpServers": { ... },
  "commands": ["commands/foo.md"]
}
```

---

## 6. Marketplace = Plugin 的目錄

2025-2026 起 Anthropic / Claude 社群開始有 plugin marketplace（類似 VS Code extension marketplace）。

裝一個 plugin：

```bash
$ /plugin install <plugin-name>
# 或 git clone <plugin repo> 到 ~/.claude/plugins/
```

幾個推薦逛的 marketplace（2026 Q1）：
- Anthropic 官方 marketplace（內建 `/plugin marketplace`）
- `awesome-claude-code-plugins`（GitHub 社群整理）
- WenyuChiou MCP-Skills catalog 也涵蓋部分 plugin

---

## 7. 寫第一個 Skill：「程式碼 review 助手」

```bash
$ mkdir -p .claude/skills/code-review/reference
```

`SKILL.md`：

```markdown
---
name: code-review
description: Review a PR / diff and produce structured feedback in 繁中
---

# Code Review SOP

當使用者要 review PR / git diff 時：

1. 先讀 diff（git diff / gh pr diff）
2. 按下列維度評論：
   - 正確性（bug / edge case）
   - 可讀性（命名 / 結構）
   - 效能（明顯 N+1 / 不必要的 IO）
   - 安全性（input validation / 敏感資訊）
   - 測試（有沒有對應 test / coverage）
3. 用繁中、條列輸出
4. 結尾標註：「整體 ✅ 通過 / ⚠️ 需修改 / ❌ 嚴重問題」

## 風格
- 不批評作者，批評 code
- 改建議要具體（不要說「這裡可以更好」要說「改成 XXX 因為...」）
- 抓到 bug 一定要建議怎麼修

## 詳細格式參考
見 `reference/format.md`
```

`reference/format.md`（按需載入）：

```markdown
# Review 詳細格式

## 範例 1：正面 review

✅ 整體通過

**正確性**: 沒有發現問題。
**可讀性**: 命名清楚，建議補一個 module-level docstring。
**效能**: N/A。
**安全性**: SQL 用 parameterized query，✅。
**測試**: 新增的 function 已有對應 test，覆蓋了 happy path 跟 error case。

## 範例 2：要修改

⚠️ 需修改

**正確性**: line 42 的 `if x:` 改 `if x is not None:`，避免空字串被當 falsy 略過。
**可讀性**: 命名 `do_thing` → `validate_user_input`。
**效能**: 沒問題。
**安全性**: line 67 直接把 user input 拼進 SQL，必須改 parameterized。
**測試**: 缺 SQL injection 的 negative test。
```

裝好後 Claude Code 啟動，做 `gh pr view 123 --json files` 拉 diff，Claude 會自動載入這個 Skill 給你格式化的 review。

---

## 8. Skill anti-patterns

❌ **太大**（>1000 行的 SKILL.md）→ 拆 reference
❌ **description 太寬泛**（「all-purpose helper」）→ 不會觸發或亂觸發
❌ **內含 hardcoded API key**（commit 上 GitHub 就完蛋）→ 用 env var
❌ **沒寫「不可做」**（only happy path）→ agent 會 over-reach
❌ **不版控**（散在 .claude/skills/）→ 跟 code 一起 commit，團隊可共享

---

## 9. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 6 — Memory & Guidance**：progressive disclosure / persistent guidance
- Skill 對應 ai-dict 的「persistent guidance you can reuse across sessions」

---

## 10. 動手練習

### 練習 7.1：寫一個 Skill

挑你自己的工作流程（例：寫 commit message / review PR / 寫日報 / 翻譯文件），寫一個 Skill：
- SKILL.md frontmatter description 精準
- 主檔 < 200 行
- 至少 1 個 reference 檔
- 至少 1 條「不可做」

**成功標準**：Claude Code 在對的情境會自動載入它（觀察 `/status` 看載了什麼）。

### 練習 7.2：從 Marketplace 裝一個 plugin

打 `/plugin marketplace`（Claude Code 內建）逛逛，挑一個你會用的裝起來。
**成功標準**：plugin 裡的 Skills / commands 你能用、會用。

### 練習 7.3：練 Progressive Disclosure

把練習 7.1 的 Skill 拆成 3 層：
- Level 1: frontmatter（10 行內）
- Level 2: SKILL.md 主體（100 行內）
- Level 3: 詳細 reference（隨意）

**成功標準**：Claude Code 觸發 Skill 時你能在 trace 看到 reference 是「按需」載入，不是一次全 load。

---

## 11. 你做完這一章後 ✅

- [ ] 能說出 Skill 跟 MCP 的差別
- [ ] 知道 Skill 的內部結構（SKILL.md + reference + scripts）
- [ ] 知道 Progressive Disclosure 的 3 層架構
- [ ] 知道什麼時候手動 vs 自動觸發
- [ ] 知道 Plugin = Skill + 設定 + 模板 的包
- [ ] 自己寫過至少一個 Skill
- [ ] 從 Marketplace 裝過至少一個 plugin

打勾 5 個以上，進 [Ch 8 — Cost 觀測 / 介入](../ch08_cost_observability/)。

---

## 11a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **description 寫太空** | LLM 不觸發 / 誤觸發 | description = 「**何時用 + 做什麼**」一句話，<150 字 |
| **frontmatter 缺 name** | skill 不出現 | `---` 區塊內必填 `name` + `description` |
| **steps 太長** | LLM 跳步驟 | 砍到 < 7 步，再長就拆兩個 skill |
| **絕對路徑寫死** | 別人 clone 跑不起 | 用相對路徑或 skill 自 detect cwd |
| **跨 SKILL 命名衝突** | project / user 兩個同名 | project-scope 蓋過 user-scope，命名加 prefix |
| **危險動作沒 confirmation** | skill 自動刪檔 / push | Constraints 段明寫「Never commit/push/delete without approval」 |
| **沒寫 Constraints** | LLM 自由發揮 | Constraints 列邊界, 比 Steps 還重要 |
| **改完不重啟** | 規則沒生效 | `/exit` 重新 `claude` 後驗 `/skill` |
| **Skill 跟 MCP 混淆** | 把 tool 塞進 SKILL.md | SKILL = 工作流程 / MCP = 工具，分清楚 |
| **Progressive Disclosure 不分層** | 一次塞 100 條規則 | 用 `## 看到 X 時` `## 看到 Y 時` 條件式呈現 |

---

## 11b. 在這頁直接練 Skill description

最關鍵是 frontmatter `description`——寫得好 LLM 會精準觸發，寫得糟會誤觸發 / 不觸發。

<LLMTryout
  title="Ch 7 in-page tryout — Skill description 評估"
  defaultSystem="你是 Skill design reviewer。看使用者給的 Skill description，評估 (1) 是否精準（不會誤觸發）(2) 是否完整（涵蓋主要場景）(3) 給 1-2 個改寫建議。回繁中。"
  defaultPrompt="評估這個 description：「幫助使用者寫 email」" />

## 12. 補充閱讀

- [Claude Code — Skills 文件](https://docs.claude.com/en/docs/agents-and-tools/claude-code/skills)
- [Anthropic Skills 設計原則 (Progressive Disclosure)](https://www.anthropic.com/engineering/claude-code-best-practices)
- WenyuChiou MCP-Skills catalog (62 entries): https://github.com/WenyuChiou/awesome-agentic-ai-zh
- ai-dict Memory & Guidance 段：https://ai-dict.gh.miniasp.com/
- `datawhalechina/agent-skills-with-anthropic`（吳恩達 + Anthropic agent skills 課程中文版，1K⭐）

---

> 🛟 **卡關時看這裡**：
> - SKILL.md trigger 不起來 / Plugin 裝壞 → [故障排除 § 框架/Skills](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - SKILL.md 標準格式 + auto-load 順序 → [速查卡 § Skill](https://symbiosis11503.github.io/agent-z/cheatsheet#skill-auto-load-順序)
> - MCP vs Skill 怎麼選 → [名詞表 § 常被混淆的 pair](https://symbiosis11503.github.io/agent-z/glossary#11-常被混淆的-pair-對比)
