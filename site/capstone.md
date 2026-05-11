# Capstone Gallery — 學員作品集

走完 AgentZ Ch 18 後最後一步：交一個 Capstone 作品。**這頁列所有被收錄的學員作品**，你做完了也歡迎投稿。

[[toc]]

---

## 什麼是 Capstone？

完整定義在 [Ch 18 §5](./chapters/ch18_maker_educator/#5-結尾capstone-是什麼)。簡短版：

> 一個能跑、能 demo、能 show off 給人看的 agent 系統。完整 README + agent source code + governance (cost cap / audit / replay 至少 2 個) + hands-on test + 200 字 reflection。

**Rubric**（5 條，[完整版見 Ch 18](./chapters/ch18_maker_educator/#capstone-rubric評分標準5-條)）：

| 項目 | 通過標準 |
|---|---|
| 能跑 | clone → 跟 README → 30 min 內 demo 出來 |
| 解決真實問題 | 不是 toy demo，你 / 朋友 / 家人會用 |
| 有 governance | cost cap / audit / replay 至少 2 個 |
| 有 reflection | README 講設計理由 + 踩坑 |
| 可擴展 | PR / fork 改造門檻低 |

---

## 怎麼投稿

開 [Pull Request](https://github.com/symbiosis11503/agent-z/pulls) 加你的作品到下面 gallery 區。PR 內容：

1. 加一個區塊（複製下面 template）
2. 提供：
   - **Repo link**（必填）
   - **Demo gif / video URL**（強烈推薦）
   - **200 字 reflection**（必填）
   - **3 個 hashtag** 描述（如 `#multi-agent` `#voice` `#家庭自動化`）
3. PR 描述附「我同意以 MIT 釋出」

### 投稿 template

```markdown
### 你的名字 / handle — 作品標題

**Repo**: <https://github.com/你/你的-capstone>
**Demo**: <gif / video / live URL>
**Tags**: `#tag1` `#tag2` `#tag3`

**簡介**（< 50 字）：
你解決的問題 + 怎麼解的。

**Reflection**（200 字）：
- 為什麼做：...
- 最大的 insight：...
- 踩過最痛的坑：...
- 下一步：...

**用了哪些章**：Ch X, Y, Z
```

---

## 收錄條件

✅ **會收錄**：
- 跟著 AgentZ 走完至少 Builder 階段（Ch 9-15）
- 程式碼公開（MIT / Apache / 任何 OSI 認證）
- README 完整能跑
- 解決一個你 / 朋友 / 家人實際遇到的問題

❌ **不會收錄**：
- 純 hello-world demo
- 抄別人 repo 沒實質修改
- 含敏感資料 / API key 外洩
- 違法用途（spam / 騷擾 / 違反 Acceptable Use Policy）

---

## Gallery（按投稿時間排序）

> 第一批投稿：**等待中**。完成 AgentZ Capstone 的學員，歡迎 PR 投稿成為首批列入 gallery 的範例！

<!-- 投稿區開始 - PR 加在這下面 -->

### 等待第一批投稿

當有學員投稿後，他們的作品會列在這。預期 layout：

```
### Your Name — 個人 Email 助理 v1
**Repo**: https://github.com/your/email-helper
**Demo**: https://github.com/your/email-helper/blob/main/demo.gif
**Tags**: `#operator` `#email` `#maker`

簡介：早上自動撈 email 分類重要 / 待回 / 廢信，用 Helix audit 紀錄全部行為，超 daily $0.50 自動停。

Reflection：
- 為什麼做：每天看 100 封 email 太累
- 最大 insight：cost cap 真的要設、不然你會睡前看到 $5 帳單
- 踩過最痛的坑：Gmail OAuth 拒簽簽不簽快瘋
- 下一步：加 reply 草稿生成（人類最終決定）

用了哪些章：Ch 4, 6, 8, 12, 14, 15
```

<!-- 投稿區結束 -->

---

## 第一批投稿者特權

第一個被收錄的 Capstone：
- 🥇 **首頁 features 區永久 highlight**
- 🥇 **PDF 版 v1.x release notes 列名感謝**
- 🥇 **AgentZ docs 引用案例（章節需要時引用你的 work）**

第 2-5 名：
- 🥈 **gallery 顯著位置**
- 🥈 **AgentZ Discussion 釘選**

---

## 不知道做什麼？— Capstone 點子 12 選

```
🤖 個人助理類
  □ 早晨簡報（calendar + email + Notion todo 整合）
  □ Email 分類 + reply 草稿
  □ 閱讀 agent（餵 URL 自動進 Obsidian + 摘要）

🏠 家庭類
  □ 家庭氣候 agent（PM2.5 + 冷氣 + 通知）
  □ 親子閱讀陪跑（讀繪本 + 問問題）
  □ 寵物日記 agent

💼 工作類
  □ 客服分流 agent（分類 + template 草稿）
  □ Code review agent（PR diff 自動 review）
  □ 開發伴侶（pre-commit hook 自動 lint + 補 test）

🎓 學習研究類
  □ Paper bot + DOI 驗證（Ch 16）
  □ 學科 tutor（題目講解、不直接給答）
  □ Workshop 教材自動生成
```

---

## 不想自己想？看 [Ch 18 Maker / Educator](./chapters/ch18_maker_educator/) 的 capstone 候選清單

---

## 結語

Capstone 不是「為了交作業」。

它是你結業後**唯一能拿出來證明你會的東西**——比結業證書、課程截圖、章節打勾都實在。3 個月後找工作 / 接案 / 開教學，這個 repo 就是你的 portfolio。

寫你會用、會在乎、會 maintain 的 agent。**make it real**。

---

[首頁](/) · [Ch 18 Maker / Educator](./chapters/ch18_maker_educator/) · [CONTRIBUTING](https://github.com/symbiosis11503/agent-z/blob/main/CONTRIBUTING.md) · [PR 投稿](https://github.com/symbiosis11503/agent-z/compare)
