# Ch 16 — Researcher 路線（進階分流）

> **60-75 分鐘**。讀完你會懂：怎麼把 agent 用在學術 / 研究情境—paper 整理、文獻比較、deep research、multi-agent peer review。
>
> 動手練習：搭一個 paper-summary-bot、跑 deep research agent、用 multi-agent review 一篇 paper。
>
> 前置：完成 Builder 階段全部章節（Ch 9-15）。

---

## 1. 為什麼學術 / 研究適合 agent？

- **資訊量大**：一個研究領域動輒 1000+ paper、人類讀不完
- **任務 well-defined**：找相關文獻 / 摘要 / 比較 / 抽 table — 都能 specs 化
- **結構化輸出**：BibTeX / table / citation — agent 擅長
- **可驗證**：摘要對不對、 citation 是不是真的——可以查 DOI

劣勢：
- **hallucinated citation**——agent 會掰假 paper。**必須**用 search/fetch + DOI 驗證。
- **paywall**：很多 paper 抓不到全文，只能 abstract

---

## 2. 4 個典型研究 agent 任務

### 2.1 Paper Summary Bot

input：一個 arxiv / DOI URL → output：300 字繁中摘要 + 3 個 takeaway。

```python
@tool
def fetch_arxiv(arxiv_id: str) -> str:
    """Fetch arxiv paper abstract + intro."""
    return httpx.get(f"https://arxiv.org/abs/{arxiv_id}").text

agent = Agent(model="claude-haiku-4-5", tools=[fetch_arxiv],
              system="你是學術 paper 摘要助理。回傳繁中 300 字摘要 + 3 個 key takeaway。")
result = agent.run("摘要 arxiv 2402.01030 (CodeAct paper)")
```

進階：加 fetch_pdf + 抽圖表 + 拉 references。

### 2.2 文獻比較 / Survey

input：「比較 ReAct / Plan-and-Solve / Reflection 三篇 paper」→ output：表格對比 + 統一 narrative。

走 multi-agent：3 個 researcher agent 各讀一篇 → 1 個 synthesizer 整合。

### 2.3 Deep Research

input：「2024-2026 multi-agent framework 發展趨勢」→ output：完整研究報告（含 5-10 篇 paper、發展時序、優劣比較、未來方向）。

跟 [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) / [Perplexity Deep Research](https://www.perplexity.ai/) 同類。本質：**Plan-and-Solve + parallel search + Reflection**。

V3 案例：`datawhalechina/hello-agents` 第十四章「自動化深度研究智能體」有完整實作參考。

### 2.4 Peer Review

input：一篇 paper draft → output：4 個 agent reviewer 各從不同維度評論（methodology / novelty / writing / impact）→ 1 個 area chair 整合 decision。

---

## 3. 必備工具集

| 工具 | 用途 | 來源 |
|---|---|---|
| arxiv search / fetch | 找 / 拉 arxiv paper | arxiv API |
| semanticscholar | citation graph / influential paper | Semantic Scholar API |
| google scholar | 通用學術搜尋 | 第三方 wrapper |
| DOI resolver | 確認 paper 真實存在 | crossref.org |
| PDF parser | 抽 paper 內容 | unstructured / PyPDF2 / pymupdf |
| reference manager | Zotero MCP / NotebookLM | MCP server |
| Notion / Obsidian | 寫筆記 | MCP server |

---

## 4. Anti-hallucination 模板

**必須的 5 條：**

1. **每個 citation 必經 DOI / arxiv ID 驗證**——agent 講「Smith et al. 2024」必須要能 fetch 該 paper 確認存在。
2. **distinguish 摘要 vs 推論**——你的 prompt 要求 agent 標 `[直接引用]` vs `[基於 X 推論]`。
3. **Reflection critique 必含「fact-check」**——critique agent 專門檢查 citation 是否真實。
4. **多 source 對比**——同一事實至少 2 source 才寫進報告。
5. **uncertainty 標記**——「2024 年某月 X 發布 Y」如果不確定日期就標「2024」不要瞎掰月份。

---

## 5. 動手練習

### 練習 16.1：Paper Summary Bot

寫 `paper_bot.py` 用 arxiv API + LLM 摘要任一 arxiv ID。
**成功標準**：給「2402.01030」回傳合理摘要 + 3 takeaway。Citation 內含 DOI / arxiv ID。

### 練習 16.2：Multi-agent paper compare

3 個 researcher agent 各讀 ReAct / Plan-and-Solve / Reflection 三篇 → synthesizer 整合成比較表。
**成功標準**：表格輸出包含 method / when to use / limitation 三欄。

### 練習 16.3：DOI 驗證

在 16.1 加 `verify_doi(doi)` 工具、強制 agent 每個 citation 都 call 一次驗證。
**成功標準**：故意 prompt「引用一篇假 paper」、agent 抓到 verify fail 拒絕掰。

---

## 6. 你做完這一章後 ✅

- [ ] 知道 4 個典型研究 agent 任務（summary / compare / deep research / peer review）
- [ ] 知道 7 個必備工具（arxiv / semantic scholar / DOI / Zotero / Notion 等）
- [ ] 知道 anti-hallucination 5 條
- [ ] 跑完練習 16.1 / 16.2 / 16.3

打勾 3 個以上，進 [Ch 17](../ch17_builder_advanced/) 或 [Ch 18](../ch18_maker_educator/)（依你的目的選）。

---

## 6b. 在這頁練 paper summary prompt

paper bot 的核心 prompt。試這個（不接 arxiv API，但能看 LLM 的摘要結構）：

<LLMTryout
  title="Ch 16 in-page tryout — paper summary"
  defaultSystem="你是學術 paper 摘要助理。看 paper title + abstract，輸出：(1) 一段 200 字繁中摘要 (2) 3 個 key takeaway，每個一句話。標記不確定的事實用 [推測]。"
  defaultPrompt="Title: ReAct: Synergizing Reasoning and Acting in Language Models.
Abstract: While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning and acting have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner..." />

## 7. 補充閱讀

- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/)
- [Perplexity Deep Research](https://www.perplexity.ai/)
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- `datawhalechina/hello-agents` 第十四章 — 自動化深度研究智能體
- Zotero MCP / NotebookLM Skill — 參考 [Ch 6](../ch06_mcp/) 跟 WenyuChiou catalog
