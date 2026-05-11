# Contributing to AgentZ

歡迎貢獻！AgentZ 是繁中 first-class、vendor-neutral、Claude Code 生態深入的 AI Agent 學習系統。任何讓它「更完善 / 更好讀 / 更可跑」的 PR 都歡迎。

## 你可以怎麼貢獻

### 🐛 報 bug / 改錯字（最歡迎）
- 章節有錯誤 / typo / dead link → 直接開 [Issue](https://github.com/symbiosis11503/agent-z/issues) 或 PR
- 範例 code 跑不起來 → Issue 附錯誤訊息 + 你的環境（OS / Python 版本 / SDK 版本）
- 中文表達不順 → PR 改寫，commit message 說明

### 📝 補章節內容
- 章節「常見地雷」可以加你踩過的坑 → PR
- 補充閱讀（§ 結尾）可以加你看過受用的 resource → PR
- 新增 LLM provider 介紹（[llm-providers.md](./site/llm-providers.md)）→ PR

### 🛠 投稿 starter code
- 章節有對應的 `starter-code/chXX_xxx/` 嗎？看 [INDEX.md](./INDEX.md) 確認
- 補一份你自己改造的 starter（含 README + 跑得起來 + 章節對應）→ PR

### 🌍 翻譯
- 想翻簡中 / EN / 日 / 韓 → 先開 Issue 討論，不要直接整章翻完才送 PR（避免重工）
- 翻譯放 `i18n/<lang>/chXX_xxx/README.md`（v3 規劃中）

### 🎤 Capstone gallery 投稿
- 你做完 AgentZ Ch 18 的 capstone，想 show off → PR 加進 [chapters/ch18_maker_educator/gallery/](./chapters/ch18_maker_educator/)
- 投稿格式：repo link + demo gif/video + 一段 200 字 writeup（學到什麼、卡關在哪）

---

## PR 流程

```bash
# 1. fork 然後 clone
git clone git@github.com:你的名字/agent-z.git
cd agent-z

# 2. 開分支
git checkout -b your-feature

# 3. 改完先跑 build 確認沒壞
npm install
npm run build  # 跑得起來再 PR

# 4. commit + push
git add .
git commit -m "Fix typo in Ch 14 §3.2"
git push origin your-feature

# 5. 開 PR：https://github.com/symbiosis11503/agent-z/compare
```

## PR 撰寫

- **標題**：一句話講做了什麼。Ex: `Fix typo in Ch 14 §3.2 (handoff → handover)`
- **內文**：
  - 為什麼改（如果 obvious 可省）
  - 動了哪幾個檔案
  - 如果是新內容，附上參考 source（避免我去 google）
- **大改動先開 Issue 討論**（> 200 行的章節變更）

## 不接受的 PR

- ❌ 廣告 / 個人專案推銷（補充閱讀加自己 GitHub 連結 OK，但是要有 substance）
- ❌ 簡轉繁機翻（看得出來、會被退）
- ❌ 純美化（章節原本就那個風格，不要硬塞 emoji）
- ❌ 引入新 framework / vendor 強推（要 vendor-neutral 精神，多家並列才接）

---

## Style guide

### 章節寫作
- **繁中**為主，技術詞彙 inline 用 English（例：「Tool use（工具呼叫）」）
- **動手練習為主**：每章至少 1 個練習，有「成功標準」可驗證
- **常見地雷**段：踩過的坑 + 解法，比理論講解珍貴
- **真實 code**：能跑、不是 pseudocode、寫明 dependency
- **vendor 引用順序**：Anthropic Claude → OpenAI GPT → Google Gemini → 其他

### Markdown
- 用 ATX heading（`#` `##`），不要 setext
- code block 一定要寫語言（` ```python `, ` ```bash `）
- 表格盡量短欄、長內容換多行 list
- 連結用 relative path（章節之間 `../chXX_xxx/`），不要寫 absolute URL

### Commit message
- 第一行 < 70 字、英文 imperative mood（`Add Ch 14 starter` not `Added`）
- 大改動 body 解釋 why、列改動點
- 引用 issue: `Fix #123: ...`

---

## Code of Conduct

簡版：
1. **Be kind**：技術討論可以激烈，人身攻擊絕對不行
2. **No spam**：自我推銷請放補充閱讀 + 有 substance
3. **No 違法內容**：generation 涉及版權 / 真實人物 / 偏見 / 違法 — refuse + flag
4. **Respect 繁中文化**：用詞對齊台灣繁中習慣，不直譯英美術語
5. **報問題用 Issue / Discussion，不要私訊**

---

## 授權

AgentZ 內容採 **MIT License**（章節 + starter code 都可商用 / 改 / 再發佈）。
PR 進來就視為同意以 MIT 釋出。

---

## 問問題 / 找人討論

- **General discussion**：[GitHub Discussions](https://github.com/symbiosis11503/agent-z/discussions)
- **Bug / feature request**：[Issues](https://github.com/symbiosis11503/agent-z/issues)
- **私下聯絡**（敏感議題）：Symbiosis (SBS) — symbiosis11503@gmail.com

---

謝謝你想貢獻 AgentZ 🙏 — 一起把繁中 AI Agent 學習資源做厚。
