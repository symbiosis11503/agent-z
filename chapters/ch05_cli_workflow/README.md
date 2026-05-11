# Ch 5 — CLI Workflow（CLAUDE.md / slash commands / 多步驟拆解）

> **60-75 分鐘**。讀完你會懂：怎麼讓 CLI agent 真正高效——CLAUDE.md 寫法、slash command 自製、多步驟任務拆解、agent vs sub-agent 怎麼用。
>
> 動手練習：寫一個 CLAUDE.md、自製一個 slash command、拆解一個大 task 給 agent 做。
>
> 前置：完成 [Ch 4](../ch04_cli_agents/) — Claude Code 已裝好、能跑簡單 task。

---

## 1. 為什麼需要 workflow？

剛裝完 Claude Code 你可能會這樣用：

```
> 改一下 main.py，把 print 換成 logger
```

能跑，但問題：
- agent 不知道你**整個專案**是怎麼回事
- 每次新對話都要重講背景
- 一個複雜需求講不清楚，agent 邊做邊問

**CLI Workflow** 就是解這三個問題的 pattern。核心三件：

1. **CLAUDE.md** — 給 agent 看的「專案手冊」，啟動自動載入
2. **Slash command** — 自製常用任務的快捷指令
3. **多步驟拆解** — 大 task 怎麼分階段交付

---

## 2. CLAUDE.md 是什麼？

CLI agent 啟動時會掃當前目錄 + 上層目錄的 `CLAUDE.md`，把內容塞進 system prompt——**等於每次對話都有這份「背景知識」**。

```
my-project/
├── CLAUDE.md         ← 專案級
├── src/
└── tests/

~/.claude/CLAUDE.md   ← 全域級（所有專案都載入）
```

兩個都會被讀，**全域 + 專案**疊加。

### 該寫什麼？

❌ **不該寫**：所有檔案的位置（agent 用 Glob/Read 自己找）、code style 教學（agent 看你的 code 自然學）

✅ **該寫**：
- 專案是什麼、誰用、解決什麼問題
- 跑起來怎麼跑（`make dev` / `pnpm dev` / `python main.py`）
- 測試怎麼跑（`pytest -q`）
- 不能動的紅線（「不要碰 migrations/ 除非我說」）
- 偏好（「用 繁中 commit message」、「不要寫無用 comment」）
- 你跟 agent 的常用對話縮寫（「fix N 表示修 issue #N」）

### 範例

```markdown
# my-project

## 簡介
洽億 ERP 訂單系統。Docker + PHP 8 + MySQL。給內部 30 人用。

## 怎麼跑
\`\`\`bash
docker compose up -d
\`\`\`
打開 localhost:8088，帳號 bacon / 3213455125

## 測試
\`\`\`bash
docker compose exec php phpunit
\`\`\`

## 不能動
- migrations/ 我自己改，不要自動 generate
- 介面 (templates/) 跟舊系統一致，不要重排版

## 偏好
- commit message 用繁中、imperative form
- 不寫 obvious comment
- 修 bug 前先寫 failing test
```

> 💡 **CLAUDE.md 是活的文件**。第一次寫完不用追求完整——agent 跑了幾次你發現「啊它老是搞錯這個」，就把規則加進去。

---

## 3. Slash command 自製

Claude Code 內建 `/help` / `/status` / `/permission` 等。**你還可以自製**——把常用 prompt 存成檔案，打 `/<name>` 就觸發。

### 怎麼建？

在你專案的 `.claude/commands/<name>.md`：

```markdown
---
description: Fix the failing test and create a PR
---

請依下列順序執行：

1. 跑 `pytest -q` 找出 failing test
2. 讀失敗 test 的 source + 對應 implementation
3. 改 implementation 讓 test 過
4. 跑 `pytest -q` 確認全綠
5. `git commit -m "..."` + `gh pr create`
6. 把 PR URL 回給我
```

然後在 Claude Code 裡打 `/fix-test`（不含 `.md`）就會跑這個 prompt。

### 個人全域 slash command

放在 `~/.claude/commands/<name>.md`（不用在專案內），所有專案都可以用。

### 進階：帶參數

```markdown
---
description: Translate the given text to traditional Chinese
arguments:
  text:
    description: Text to translate
    required: true
---

把以下文字翻譯成繁中：

{{text}}
```

打 `/translate-zh 你要翻的英文` 就會帶參數進去。

---

## 4. 多步驟任務拆解：4 個策略

複雜需求一次塞給 agent 通常會「邊做邊忘」。4 個拆解策略：

### 4.1 Search → Plan → Execute → Verify

最通用 pattern：

```
1. Search（找相關 code）   — Glob / Grep / Read 蒐集 context
2. Plan（先講要做什麼）    — agent 列出步驟給你看
3. Execute（執行）         — 你 OK 後才動手
4. Verify（驗證）          — 跑 test / build / lint
```

對應 prompt：
```
> 我要改 user signup flow 加 email verification。先 search 相關檔案 + 講你打算怎麼改，**先不要動 code**，等我說 OK。
```

agent 會 search + 給 plan，你看完再批准。這跟「直接動手」差別在你**保留撤銷的成本**——你看 plan 看得出方向錯就喊停，不用清掉一堆改過的 code。

### 4.2 一個變更只動一件事

❌ 「順便重構這個 module 跟修 bug 跟加 test」
✅ 「先修 bug，再開新對話討論重構」

agent 一次做太多事更容易出錯、commit message 也亂。**git commit 一次只做一件事的舊規矩，agent 時代依舊適用**。

### 4.3 用 sub-agent 處理獨立子任務

Claude Code 內建 `Agent` 工具（subagent）——大 agent 可以呼叫小 agent 跑獨立任務（例如「找全 codebase 哪些檔案 import 了 X」），結果回來不污染主對話 context。

什麼時候用：
- 子任務的中間結果**很大**（搜尋 100 個檔案）
- 子任務**獨立**（不需要主 agent 的 context）
- 你想**並行**（多個子任務同時跑）

什麼時候**不**用：
- 子任務需要主 agent 的決策連動（會丟 context）
- 任務小到主 agent 一鍵搞定（多餘 overhead）

### 4.4 Hand-off 切換 model

複雜階段用 Opus（強但貴），重複動作切 Haiku（便宜快）。打 `/model <model_name>` 切換。

---

## 5. Slash command 的 anti-pattern

❌ **把整個 `/help` 都寫死成 slash command**：你只是把 prompt 從你打字改成檔案，沒省事
❌ **slash command 裡塞「請仔細思考」廢話**：佔 token、沒效果
❌ **不寫 description**：以後忘記做什麼用

✅ **真正值得做 slash command 的徵兆**：你發現自己**3 次以上**打了類似的長 prompt

---

## 6. Hook：在工具呼叫前後跑你的 code

Claude Code 支援 hook——當 agent 要呼叫某個工具時（PreToolUse / PostToolUse），跑你寫的 shell script。

範例 `.claude/settings.json`：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --fix"
          }
        ]
      }
    ]
  }
}
```

意思：「agent 每次 Write/Edit 完，自動跑 `npm run lint --fix`」。這樣 agent 改完 code 自動格式化。

進階用法：
- 防止改某些檔案（Pre hook 檢查 + exit 1 阻擋）
- 自動 commit / push / 通知
- 記錄 agent 每個工具呼叫到稽核 log

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 7 — Work Modes**：plan-and-act / human-in-the-loop / code review / AFK execution
- **Section 6 — Memory & Guidance**：CLAUDE.md = persistent guidance for the model

---

## 8. 動手練習

### 練習 5.1：寫一個 CLAUDE.md

挑你自己一個專案（沒專案的話用 Ch 0 的 `agentz-learning`），寫一份 CLAUDE.md 包含：
- 專案簡介（30 字以內）
- 怎麼跑
- 怎麼測
- 至少 2 條「不能動」或「偏好」規則

**成功標準**：CLAUDE.md commit 進 git，agent 啟動時你能在 `/status` 確認它載入了。

### 練習 5.2：自製 3 個 slash command

寫 3 個你會常用的：
1. `/commit` — agent 看 staged changes + 提一個 commit message + 等你 confirm 再 commit
2. `/translate-zh` — 帶 text 參數，回繁中
3. 自選一個跟你工作相關的

**成功標準**：3 個都跑得起來，每個都實際用過 1 次以上。

### 練習 5.3：Search → Plan → Execute 跑一個真實任務

挑你自己 codebase 裡一個小重構（拆函式、改變數名、抽常數）。**先讓 agent search + plan，你 review plan 後再 execute**。

比較：
- 你 review plan 的時候有沒有抓到方向錯誤？
- agent execute 完跑 test 通過了嗎？

**成功標準**：完成一輪 Search→Plan→Execute→Verify、寫 100 字心得。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 CLAUDE.md 該寫什麼 / 不該寫什麼
- [ ] 你自己有 CLAUDE.md（至少一個專案 + 一個全域）
- [ ] 自製過 slash command
- [ ] 知道 Search → Plan → Execute → Verify pattern
- [ ] 知道什麼時候用 sub-agent
- [ ] 知道 hook 能做什麼
- [ ] 跑完練習 5.1 / 5.2 / 5.3

打勾 5 個以上，進 [Ch 6 — MCP](../ch06_mcp/)。

---

## 10. 補充閱讀

- [Claude Code — CLAUDE.md best practices](https://docs.claude.com/en/docs/agents-and-tools/claude-code/memory)
- [Claude Code — slash commands](https://docs.claude.com/en/docs/agents-and-tools/claude-code/slash-commands)
- [Claude Code — hooks](https://docs.claude.com/en/docs/agents-and-tools/claude-code/hooks)
- ai-dict Work Modes 段：https://ai-dict.gh.miniasp.com/
- WenyuChiou Stage A2 CLI Workflow Patterns
