# Ch 16 — Researcher 路線（進階分流）

> **75-90 分鐘**。讀完你會懂：怎麼把 agent 用在學術 / 研究情境—paper 整理、文獻比較、deep research、multi-agent peer review、citation 驗證、anti-hallucination 模板。
>
> 動手練習：搭一個 paper-summary-bot、跑 deep research agent、用 multi-agent review 一篇 paper、加 DOI 驗證閘門。
>
> 前置：完成 Builder 階段全部章節（[Ch 9](../ch09_function_calling/) - [Ch 15](../ch15_deploy_audit_replay/)）。

---

## 1. 為什麼學術 / 研究適合 agent？

- **資訊量大**：一個研究領域動輒 1000+ paper、人類讀不完
- **任務 well-defined**：找相關文獻 / 摘要 / 比較 / 抽 table — 都能 specs 化
- **結構化輸出**：BibTeX / table / citation — agent 擅長
- **可驗證**：摘要對不對、citation 是不是真的——可以查 DOI

**劣勢 / 風險**：
- **hallucinated citation**——agent 會掰假 paper（編出作者名 + 年份 + 標題都看似真實）。**必須**用 search/fetch + DOI 驗證。
- **paywall**：很多 paper 抓不到全文，只能 abstract
- **outdated**：模型 cut-off 後的 paper 看不到，要靠外部 search tool
- **過度自信**：agent 講「research shows」要當作「需要驗證」不是「真理」

---

## 2. 4 個典型研究 agent 任務

### 2.1 Paper Summary Bot

input：一個 arxiv / DOI URL → output：300 字繁中摘要 + 3 個 takeaway。

```python
import httpx
from anthropic import Anthropic

client = Anthropic()

def fetch_arxiv_abstract(arxiv_id: str) -> dict:
    """從 arxiv API 拉 metadata (title + abstract + authors)."""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    resp = httpx.get(url, timeout=15.0)
    # arxiv 回 Atom XML — 用 feedparser 或 regex 抽
    import re
    title = re.search(r"<title>(.+?)</title>", resp.text, re.DOTALL).group(1).strip()
    summary = re.search(r"<summary>(.+?)</summary>", resp.text, re.DOTALL).group(1).strip()
    return {"arxiv_id": arxiv_id, "title": title, "abstract": summary}

def summarize_paper(arxiv_id: str) -> str:
    paper = fetch_arxiv_abstract(arxiv_id)
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        system="你是學術 paper 摘要助理。輸入 title + abstract，輸出 (1) 300 字繁中摘要 (2) 3 個 key takeaway。標記不確定推論用 [推測]。",
        messages=[{"role": "user", "content": f"Title: {paper['title']}\nAbstract: {paper['abstract']}\narxiv: {arxiv_id}"}]
    )
    return resp.content[0].text

print(summarize_paper("2402.01030"))  # CodeAct paper
```

進階：加 `fetch_pdf` + 抽 figure / table + 拉 references 做 citation network。

### 2.2 文獻比較 / Survey

input：「比較 ReAct / Plan-and-Solve / Reflection 三篇 paper」→ output：表格對比 + 統一 narrative。

**Pipeline 架構**（[Ch 14 multi-agent](../ch14_multi_agent/)）：

```python
def compare_papers(arxiv_ids: list[str], dimensions: list[str]) -> str:
    # Phase 1: 平行讓 3 個 researcher 各讀一篇
    summaries = []
    for aid in arxiv_ids:
        paper = fetch_arxiv_abstract(aid)
        s = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=800,
            system=f"你是 paper reader。從 {dimensions} 維度抽資訊。每維度一句話、可比較。",
            messages=[{"role": "user", "content": f"{paper['title']}\n\n{paper['abstract']}"}]
        ).content[0].text
        summaries.append({"arxiv_id": aid, "title": paper["title"], "extracted": s})

    # Phase 2: synthesizer 整合表格
    block = "\n---\n".join(f"[{s['arxiv_id']}] {s['title']}\n{s['extracted']}" for s in summaries)
    final = client.messages.create(
        model="claude-sonnet-4-6",  # synthesizer 用大模型，summary 用小的
        max_tokens=1500,
        system="你整合多份 paper 摘要成一張比較表。輸出 markdown table，每列一篇 paper，每欄一個 dimension。",
        messages=[{"role": "user", "content": f"Dimensions: {dimensions}\n\n{block}"}]
    )
    return final.content[0].text

print(compare_papers(
    ["2210.03629", "2305.04091", "2303.11366"],  # ReAct / Plan-and-Solve / Reflection
    dimensions=["method", "when to use", "limitation", "key result"],
))
```

**關鍵設計**：
- summarizer 用便宜 model（Haiku $1/M）、synthesizer 用大 model（Sonnet $3/M）
- 平行抽各篇摘要 → 序列整合，省 token + 速度快
- dimension 必須先 spec，不要讓 synthesizer 自由發揮

### 2.3 Deep Research

input：「2024-2026 multi-agent framework 發展趨勢」→ output：完整研究報告（含 5-10 篇 paper、發展時序、優劣比較、未來方向）。

跟 [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) / [Perplexity Deep Research](https://www.perplexity.ai/) 同類。

**本質**：Plan-and-Solve + parallel search + Reflection（[Ch 10](../ch10_react_paradigms/)）。

```python
def deep_research(topic: str, depth: int = 3) -> str:
    # Step 1: Plan — agent 自己拆 sub-topic
    plan = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="你是研究 planner。輸入 topic，輸出 5-7 個 sub-topic 查詢字串。JSON array.",
        messages=[{"role": "user", "content": topic}]
    )
    subtopics = json.loads(plan.content[0].text)

    # Step 2: 平行搜尋每個 sub-topic（這裡示意，實作用 tavily / brave / serper search API）
    findings = []
    for sub in subtopics:
        results = web_search(sub, k=5)  # 你的 search tool
        # 對每筆 result fetch_pdf / extract_abstract
        for r in results:
            findings.append({"sub": sub, "url": r["url"], "snippet": r["snippet"]})

    # Step 3: Synthesize — 整合成報告
    findings_block = "\n".join(f"[{i}] {f['sub']} | {f['url']} | {f['snippet']}" for i, f in enumerate(findings))
    report = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system="""你寫研究報告。依時序排列發展、引用必標 [編號]、結尾列 5 個未來方向。
        每個論述至少有 2 個 source。標 [推測] for unverified inference.""",
        messages=[{"role": "user", "content": f"Topic: {topic}\n\nFindings:\n{findings_block}"}]
    )

    # Step 4 (optional): Reflection — critique agent 抓 hallucination
    if depth >= 2:
        critique = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system="你是 critique。檢查報告的 (1) citation 對應到 source (2) 有無 hallucination (3) 結論是否 over-claim。",
            messages=[{"role": "user", "content": report.content[0].text}]
        )
        # 把 critique 拿回去讓主 agent 修
        ...

    return report.content[0].text
```

**重點**：
- Plan 階段不要省，讓 agent 拆細，後續每個 sub 都能平行
- Search → Fetch → Extract 三步分離，方便 cache + debug
- Reflection 比一次寫好更重要，能抓 80% hallucination

V3 case：`datawhalechina/hello-agents` 第十四章「自動化深度研究智能體」有完整 Python 實作可參考。

### 2.4 Peer Review

input：一篇 paper draft → output：4 個 agent reviewer 各從不同維度評論 → 1 個 area chair 整合 decision。

**4-reviewer 配置**：

```python
REVIEWER_ROLES = {
    "methodology": "你是嚴格的方法學 reviewer。檢查實驗設計、baseline 是否合理、statistic 是否正確。挑毛病不留情。",
    "novelty": "你是 novelty reviewer。對比現有 work、挑「這跟 X 有什麼不同」。",
    "writing": "你是 writing reviewer。檢查清晰度、邏輯、figure 是否 self-explanatory。",
    "impact": "你是 impact reviewer。問「為什麼讀者要 care」、思考實際應用。",
}

def peer_review(paper_text: str) -> dict:
    reviews = {}
    for role, system in REVIEWER_ROLES.items():
        r = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=system + "\n輸出 (1) 3 個優點 (2) 3 個缺點 (3) accept/borderline/reject 並說明。",
            messages=[{"role": "user", "content": paper_text[:10000]}]  # 截 10K
        )
        reviews[role] = r.content[0].text

    # Area chair 整合
    block = "\n---\n".join(f"=== {r} ===\n{c}" for r, c in reviews.items())
    chair = client.messages.create(
        model="claude-opus-4-7",  # area chair 用最強推理
        max_tokens=2000,
        system="你是 area chair。整合 4 reviewer 看法、做最終 accept/reject decision、寫 meta-review。",
        messages=[{"role": "user", "content": block}]
    )
    return {"individual_reviews": reviews, "meta_review": chair.content[0].text}
```

**討論題**：4 reviewer 哪一條最容易 false-positive accept？提示：novelty 容易被「新組合 = 創新」騙到。

---

## 3. 必備工具集

| 工具 | 用途 | 來源 / 介接 |
|---|---|---|
| arxiv search / fetch | 找 / 拉 arxiv paper | `arxiv` Python lib / arxiv API |
| Semantic Scholar | citation graph / influential paper | `semanticscholar` API（需註冊 free key） |
| Google Scholar | 通用學術搜尋 | `scholarly` lib（rate limit 嚴） |
| Tavily / Brave / Serper | 通用 web search | 各家 API |
| DOI resolver | 確認 paper 真實存在 | `crossref.org` API（免費） |
| PDF parser | 抽 paper 內容 | `unstructured` / `PyPDF2` / `pymupdf` |
| Zotero | 文獻管理 | Zotero MCP server |
| NotebookLM | 多 paper QA | Google NotebookLM Skill |
| Notion / Obsidian | 寫筆記 | MCP server |

---

## 4. Anti-hallucination 模板（**最重要的一節**）

**必須的 5 條**：

1. **每個 citation 必經 DOI / arxiv ID 驗證**——agent 講「Smith et al. 2024」必須要能 fetch 該 paper 確認存在。
2. **distinguish 摘要 vs 推論**——prompt 要求 agent 標 `[直接引用]` vs `[基於 X 推論]` vs `[推測]`。
3. **Reflection critique 必含「fact-check」**——critique agent 專門檢查 citation 是否真實。
4. **多 source 對比**——同一事實至少 2 source 才寫進報告。
5. **uncertainty 標記**——「2024 年某月 X 發布 Y」如果不確定日期就標「2024」不要瞎掰月份。

### DOI 驗證實作

```python
def verify_doi(doi: str) -> dict | None:
    """用 crossref.org 驗證 DOI 真實存在。"""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = httpx.get(url, timeout=10.0)
        if r.status_code == 200:
            msg = r.json()["message"]
            return {
                "doi": doi,
                "title": msg.get("title", [""])[0],
                "year": msg.get("published-print", {}).get("date-parts", [[None]])[0][0],
                "authors": [f"{a.get('family', '')}" for a in msg.get("author", [])[:3]],
                "verified": True,
            }
    except Exception:
        pass
    return None  # 不存在 / 網路 fail

# 整合到 agent loop：每篇 citation tool call 完都過這關
```

### 「拒絕掰」prompt 範本

```text
你是 research agent。寫研究報告時，每個 claim 引用必須符合：

1. 用 verify_doi(doi) 確認 paper 存在
2. 標記引用類型：[直接引用] / [基於 abstract 推論] / [推測 — 需驗證]
3. 找不到 source 的 claim 不要寫，寫「此議題尚需驗證」
4. 同一 claim 至少 2 個 source，差別大就寫「兩方分歧：A 認為 X，B 認為 Y」

違反任一條請拒絕回答並說明原因。
```

---

## 5. 常見地雷（**讀過比沒讀過省 5 小時 debug**）

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **掰 citation** | 講「Wang et al. 2024」但 paper 不存在 | 強制 DOI verify + Reflection fact-check |
| **過度自信** | 「研究顯示...」沒 source | prompt 要求每 claim 標來源編號 |
| **time cutoff 弄錯** | 把 2026 paper 講成 2023 | prompt 給 "today's date" + 標明模型 cutoff |
| **paywall 假裝有讀** | abstract only 卻寫像讀全文 | 把「abstract 內容」跟「full-paper 推論」分開 prompt |
| **synthesizer 偏心** | 4 paper 比較變 1 paper 獨大 | dimension 強制 spec、每維度必填、空白填「未提及」 |
| **無 dimension** | 「比較」變一段 narrative | 強制 markdown table 輸出格式 |
| **平行炸 quota** | 同時開 50 paper fetch 被 ban | 加 `asyncio.Semaphore(5)` 限流 |
| **PDF 抽失敗忽略** | 抽不到內容卻繼續摘要 | 抽完空字串就 fail-fast、不要讓 LLM 編 |

---

## 6. Real case：Anthropic 自家 multi-agent research

Anthropic 2025-06 發表 [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) 講他們內部研究 agent：

- **15× token cost** vs 單 agent
- **+90% quality** on complex research tasks
- **3 keys**: explicit plan / parallel search / critique loop

關鍵設計（部分公開）：
1. Lead agent 拆 4-8 個 sub-task → spawn sub-agent
2. Sub-agent 用 Claude 4 平行跑 search → fetch → summarize
3. Lead agent 整合 + Reflection（critique 自己的 draft）
4. 全程 audit log 在 evals dashboard

**對你的啟發**：複雜研究問題 **必須** multi-agent + Reflection，單 agent + 大 context 不夠。

---

## 7. 動手練習

### 練習 16.1：Paper Summary Bot

寫 `paper_bot.py` 用 arxiv API + LLM 摘要任一 arxiv ID。
**成功標準**：給「2402.01030」回傳合理摘要 + 3 takeaway。citation 內含 DOI / arxiv ID。

### 練習 16.2：Multi-agent paper compare

3 個 researcher agent 各讀 ReAct / Plan-and-Solve / Reflection 三篇 → synthesizer 整合成比較表。
**成功標準**：表格輸出包含 method / when to use / limitation 三欄、每篇都有 arxiv link。

### 練習 16.3：DOI 驗證閘門

在 16.1 加 `verify_doi(doi)` 工具、強制 agent 每個 citation 都 call 一次驗證。
**成功標準**：故意 prompt「引用一篇假 paper：Doe et al. 2024」、agent 抓到 verify fail 拒絕掰、回覆改為「此議題尚需驗證」。

### 練習 16.4：Deep research mini

寫一個 deep_research("agentic-RL 最新進展") 跑 plan → search → fetch → synthesize → reflect 5 步、輸出 markdown 報告。
**成功標準**：報告至少含 5 篇真實 paper、每段有 citation、結尾 5 個未來方向。

---

## 8. 你做完這一章後 ✅

- [ ] 知道 4 個典型研究 agent 任務（summary / compare / deep research / peer review）
- [ ] 知道 9 個必備工具（arxiv / Semantic Scholar / Tavily / DOI / Zotero / NotebookLM 等）
- [ ] 知道 anti-hallucination 5 條
- [ ] 知道 8 個常見地雷（hallucinated citation / time cutoff / paywall 假讀 ...）
- [ ] 跑完練習 16.1 / 16.2 / 16.3，bonus 16.4

打勾 3 個以上，進 [Ch 17](../ch17_builder_advanced/) 或 [Ch 18](../ch18_maker_educator/)（依你的目的選）。

---

## 9. 在這頁練 paper summary prompt

paper bot 的核心 prompt。試這個（不接 arxiv API，但能看 LLM 的摘要結構）：

<LLMTryout
  title="Ch 16 in-page tryout — paper summary"
  defaultSystem="你是學術 paper 摘要助理。看 paper title + abstract，輸出：(1) 一段 200 字繁中摘要 (2) 3 個 key takeaway，每個一句話。標記不確定的事實用 [推測]。"
  defaultPrompt="Title: ReAct: Synergizing Reasoning and Acting in Language Models.
Abstract: While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning and acting have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner..." />

---

## 10. 補充閱讀

- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/)
- [Perplexity Deep Research](https://www.perplexity.ai/)
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — 必讀
- `datawhalechina/hello-agents` 第十四章 — 自動化深度研究智能體
- [Stanford STORM](https://github.com/stanford-oval/storm) — Wikipedia-style 研究報告 agent
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher) — 開源 deep research
- Zotero MCP / NotebookLM Skill — 參考 [Ch 6](../ch06_mcp/) 跟 WenyuChiou catalog
- [crossref.org API docs](https://api.crossref.org/) — DOI 驗證
- [arxiv API docs](https://info.arxiv.org/help/api/index.html) — 學術 paper metadata
