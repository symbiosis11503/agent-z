---
title: 引用 AgentZ
description: 在論文、報告、blog 或教學引用 AgentZ — BibTeX / APA / Chicago / Markdown 格式。
---

# 引用 AgentZ

學術論文、課程講義、技術 blog、會議 talk 想引用 AgentZ？這頁列出幾種常見格式，**直接複製貼上即可**。
若引用特定章節，請帶上該章的 URL 與「擷取日期」（內容會持續迭代）。

## BibTeX

```bibtex
@misc{agentz_2026,
  author       = {{C.C.H. (Huang, Chu-Chen)}},
  title        = {AgentZ: 繁體中文 AI Agent 工程師學習地圖},
  year         = {2026},
  howpublished = {\url{https://symbiosis11503.github.io/agent-z/}},
  note         = {Open-source Traditional-Chinese AI Agent curriculum, 20 chapters, vendor-neutral. Latest: v1.6.},
}
```

引用特定章節時，建議用 `@misc` + `chapter` 註記：

```bibtex
@misc{agentz_ch15_v3case_2026,
  author       = {{C.C.H. (Huang, Chu-Chen)}},
  title        = {AgentZ Ch 15: Deploy / Audit / Replay — Helix V3 案例研究},
  year         = {2026},
  howpublished = {\url{https://symbiosis11503.github.io/agent-z/chapters/ch15_deploy_audit_replay/}},
  note         = {Chapter from AgentZ curriculum.},
}
```

## APA 7th

```
C.C.H. (Huang, Chu-Chen). (2026). AgentZ: 繁體中文 AI Agent 工程師學習地圖 (v1.6) [Online curriculum]. https://symbiosis11503.github.io/agent-z/
```

引用特定章節：

```
C.C.H. (Huang, Chu-Chen). (2026). Ch 15: Deploy / Audit / Replay — Helix V3 案例研究. In AgentZ: 繁體中文 AI Agent 工程師學習地圖 (v1.6). https://symbiosis11503.github.io/agent-z/chapters/ch15_deploy_audit_replay/
```

## Chicago 17th (note + bibliography style)

**Note**：

```
1. C.C.H. (Huang, Chu-Chen), AgentZ: 繁體中文 AI Agent 工程師學習地圖, v1.6 (2026), https://symbiosis11503.github.io/agent-z/.
```

**Bibliography**：

```
C.C.H. (Huang, Chu-Chen). AgentZ: 繁體中文 AI Agent 工程師學習地圖. v1.6. 2026. https://symbiosis11503.github.io/agent-z/.
```

## Markdown / Plain text

部落格、README、Slack 連結快速版：

```markdown
參考 [AgentZ](https://symbiosis11503.github.io/agent-z/)（繁中 AI Agent curriculum v1.6, C.C.H., 2026）。
```

特定章節：

```markdown
詳見 [AgentZ Ch 6 MCP](https://symbiosis11503.github.io/agent-z/chapters/ch06_mcp/)（v1.6）。
```

## CITATION.cff（GitHub 認得）

如果你要 fork / mirror 並透過 GitHub「Cite this repository」按鈕顯示：

```yaml
cff-version: 1.2.0
title: "AgentZ: 繁體中文 AI Agent 工程師學習地圖"
authors:
  - family-names: Huang
    given-names: Chu-Chen
    alias: C.C.H.
type: dataset
version: "1.6"
date-released: 2026-05-12
url: "https://symbiosis11503.github.io/agent-z/"
repository-code: "https://github.com/symbiosis11503/agent-z"
license: CC-BY-4.0
keywords:
  - AI Agent
  - LLM
  - Claude Code
  - MCP
  - 繁體中文
  - curriculum
```

## 版本與更新

- 引用時請盡量帶 **版本號**（目前 v1.6）— 內容持續迭代，章節編號穩定但內文會 truth-sync
- 改動紀錄全在 [更新紀錄 (whatsnew)](./whatsnew)
- 若需要 archive 永久連結（防 link rot），建議用 [Wayback Machine](https://web.archive.org/) 主動存檔對應章節 URL，並在 BibTeX `note` 加上 archived URL

## 授權

內容預設 **CC-BY-4.0**（署名即可自由用於教學、課程、商業 derivative，請保留作者署名與來源 URL）。
程式碼片段（`starter-code/` 等）為 **MIT**。

## 致謝

如果 AgentZ 對你的研究、教材或產品有實質幫助，歡迎：

- 在 [GitHub](https://github.com/symbiosis11503/agent-z) 點 ⭐
- 開 [Discussions](https://github.com/symbiosis11503/agent-z/discussions) 分享你怎麼用、跑出什麼結果
- 引用後寄一份你的 paper / talk slides 到 issue tracker，會收進 [Capstone Gallery](./capstone)

— Built by **C.C.H.** （Huang, Chu-Chen）, 2026.
