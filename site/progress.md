# 學習進度檢核

打勾標記已完成的章節。進度只存在你的瀏覽器（`localStorage`），不上傳任何伺服器。

<ProgressTracker />

---

## 為什麼有 milestone evidence？

讀完 ≠ 學會。AgentZ 的 4 層 ladder（Watcher → Operator → Builder → 進階）每層都要求**具體交付物**：

- **Watcher**：能用 prompt 拿到你要的東西、看得懂 agent JSON trace
- **Operator**：CLI agent 真實 task 跑完、CLAUDE.md / Skill / MCP server 寫過
- **Builder**：自寫過 agent / framework / multi-agent 系統
- **進階**：依分流路線完成 portfolio 作品

把練習答案（截圖 / GitHub link / sandbox run_id）存在一個地方（你 Notion / Obsidian / GitHub Project 任一），結業時是你最強的學習 portfolio。

---

## 每章 milestone evidence 模板

每章做完，**1 行紀錄 + 1 個 artifact**。範本：

```markdown
## Ch X — <章名稱>
- 完成日: YYYY-MM-DD
- 動手練習做完: ☐ X.1 ☐ X.2 ☐ X.3
- Artifact: <GitHub link / 截圖 / run_id / sandbox URL>
- 學到最深的一條: <一句話>
- 我還沒搞懂的: <列 1-3 點，下次回來補>
```

### 為什麼這樣設計

| 欄位 | 為什麼 |
|---|---|
| **完成日** | 看自己學習節奏，回頭優化計畫 |
| **練習做完 box** | 避免「讀完當做完」的錯覺 |
| **Artifact** | 客觀證據，找工作面試直接拿出來 |
| **學到最深的一條** | 強化記憶；3 個月後回看也記得 |
| **我還沒搞懂的** | metacognition — 知道自己不會什麼比知道什麼還重要 |

---

## 推薦工具

| 工具 | 用法 |
|---|---|
| **GitHub Project (kanban)** | 每章一張 card、columns 用「Reading / Doing / Done / Stuck」|
| **Obsidian / Notion** | 寫長一點的 reflection、可加圖 |
| **私人 GitHub repo** | 練習 code 全 push，結業 = 全本 portfolio |
| **Notion timeline** | 看自己學習節奏 |
| **Logseq / Roam** | atomic notes，跨章節串概念 |

挑你已經在用的、不要為了 AgentZ 學新筆記工具。

---

## Capstone portfolio 模板

走到 Ch 18 後要交 Capstone（[Rubric 5 條](./chapters/ch18_maker_educator/#5-結尾capstone-是什麼)）。Repo structure 建議：

```
my-agentz-capstone/
├── README.md              ← 完整介紹 + 為什麼做 + 怎麼跑
├── agent/                 ← agent source code
│   ├── main.py
│   ├── tools/
│   └── prompts/
├── governance/            ← 從 Ch 15 學到的
│   ├── cost_tracker.py
│   ├── audit.db
│   └── policy.yaml
├── tests/                 ← 至少 1 個 hands-on test
│   └── test_agent.py
├── docs/
│   ├── demo.gif           ← 跑起來的動畫
│   └── reflection.md      ← 200 字學習心得
└── pyproject.toml
```

README 必填段：
1. **為什麼做這個 agent**（1 段）
2. **怎麼跑**（pre-req + 5 步驟內）
3. **技術選擇理由**（用 Haiku/Sonnet/Opus？哪個 framework？為什麼？）
4. **踩過什麼坑**（給後人省時間）
5. **下一步 roadmap**（你會怎麼擴它）

---

## Reflection prompt 範本

每完成一個 ladder 寫一段（給未來的你看）：

### Watcher 結束 reflection

```
1. 我現在能跟 5 歲小孩解釋「agent vs ChatGPT」嗎？試試看
2. 我看過的 5 個 prompt 範例裡，哪個讓我「啊原來這樣寫」？
3. 我現在最大的概念盲點是什麼？
```

### Operator 結束 reflection

```
1. 我用 Claude Code 跑過最長 / 最複雜的真實 task 是什麼？耗時？
2. 我寫過的 SKILL / MCP server 是不是有複用價值？
3. cost 我看得懂嗎？最近一次 run 燒多少？
```

### Builder 結束 reflection

```
1. 我自寫的 mini framework 跟 LangGraph / CrewAI 差在哪？
2. 我的 multi-agent 設計遇到什麼 deadlock / 同步問題？
3. 我能 deploy 一個 agent 上 production 並讓它撐 1 個月不炸嗎？
```

### 進階分流結束 reflection

```
1. 我選了哪條路線？為什麼？
2. 我的 Capstone 解決什麼真實問題？
3. 結業後我接下來 3 個月想做什麼？
```

---

## 你卡關時怎麼辦？

| 狀況 | 建議 |
|---|---|
| **某章看不懂** | 跳回前 1-2 章看看前置概念有沒有跳。再不行去 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 問 |
| **API key 跑炸了** | 看 [LLM / API 申請指南](./llm-providers) 確認 cost cap 設好 |
| **code 跑不起來** | 看對應 [starter-code](https://github.com/symbiosis11503/agent-z/tree/main/starter-code) 有沒有完整版本 |
| **想找人陪走** | 開 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 或在 LinkedIn / X post 你的進度，會吸引同路人 |
| **覺得學得太慢** | 看 [課程地圖](./roadmap) 4 個學習計畫對照、調整節奏 |
| **學完不知道做什麼** | Ch 18 maker / educator 路線給你 capstone 候選清單 |

---

## 結業後

完成 Capstone 後：
- ✅ 你已從「LLM 使用者」變「Agent 系統構建者」
- ✅ 你有一個能 show off 的 GitHub repo
- ✅ 你能拿這個 repo 面試 / 接案 / 開教學 / 寫 blog
- ✅ 你能回來貢獻 AgentZ（[CONTRIBUTING.md](https://github.com/symbiosis11503/agent-z/blob/main/CONTRIBUTING.md)）

歡迎在 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 分享你的 Capstone 連結 — 第一批投稿會放進首頁 capstone gallery。
