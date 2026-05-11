# Ch 13 — Memory & RAG

> **75-90 分鐘**。讀完你會懂：LLM 為什麼沒記憶、session memory / long-term memory / RAG / contextual retrieval 各是什麼、怎麼選 vector DB、實作一個個人助理 agent 有記憶。
>
> 動手練習：寫一個有 session memory 的 agent、加一個 RAG layer、做 contextual retrieval 對比。
>
> 前置：完成 [Ch 12](../ch12_mini_framework/) — 有自己的 mini framework 能加 memory。
>
> 🛠 **Starter code**: [`starter-code/ch13_memory_rag/`](https://github.com/symbiosis11503/agent-z/tree/main/starter-code/ch13_memory_rag) — session memory (SQLite-backed) + Chroma RAG pipeline + contextual retrieval demo。

---

## 1. 「LLM 沒有記憶」回顧 + 為什麼需要 memory

[Ch 1 §3](../ch01_llm_basics/#3-context-window-llm-的「記憶」上限) 提過：**LLM 每次 API call 是獨立的**——你看 ChatGPT 記得你前面講什麼，是因為它後端把對話歷史塞進 context。

但 context 有兩個限制：
- **大小**：200K-1M token，塞滿了
- **成本**：每多一輪、前面對話都重新進 context 重新算錢

所以 production agent **必須有 memory 層**——把對話 / 文件 / 知識存外面、需要時撈相關片段進 context。

---

## 2. 三種 memory

| 類型 | 範圍 | 例子 | 實作 |
|---|---|---|---|
| **Session memory** | 一次對話內 | 「剛剛你說我要訂下週五的會議室」 | 累積 messages array，可摘要 |
| **Long-term memory** | 跨對話 | 「使用者是 Wei、住台北、偏好繁中」 | 寫進 DB / vector store / 結構化 store |
| **RAG（檢索增強）** | 外部知識 | 「公司 SOP / 產品文件 / 過去案例」 | vector DB + similarity search |

實務上**三種混合**：對話進行用 session memory，講到特定使用者偏好查 long-term，要查公司知識用 RAG。

---

## 3. Session Memory: 累積 + 摘要

最簡單的版本就是不刪 messages：

```python
messages = []
while True:
    user_input = input("> ")
    messages.append({"role": "user", "content": user_input})
    resp = client.messages.create(model="...", messages=messages, ...)
    messages.append({"role": "assistant", "content": resp.content[0].text})
    print(resp.content[0].text)
```

問題：對話到 50 輪後 context 100K+ token，每輪 $0.10-0.30。

**解法：摘要老對話**。

```python
SUMMARIZE_THRESHOLD = 20  # 20 條 messages 就壓縮

if len(messages) > SUMMARIZE_THRESHOLD:
    # 把舊的 10 條摘要成 1 條 system note
    old = messages[:10]
    summary_resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Summarize this conversation in 100 字 繁中 keep key facts:\n{format_messages(old)}"}
        ],
    )
    summary = summary_resp.content[0].text
    messages = (
        [{"role": "user", "content": f"[CONVERSATION SUMMARY]\n{summary}"}]
        + messages[10:]
    )
```

LangGraph / Claude Code 內部 compaction 是這個機制的進階版（保留結構化資料 / tool call 摘要）。

---

## 4. Long-term Memory: 結構化 vs 向量

### 4.1 結構化（適合確定欄位的事實）

```python
# 簡單 SQLite
import sqlite3
conn = sqlite3.connect("memory.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        user_id TEXT,
        key TEXT,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, key)
    )
""")

# 寫
conn.execute("INSERT OR REPLACE INTO facts VALUES (?, ?, ?, ?)",
             ("wei", "city", "Taipei", datetime.now()))

# 讀
row = conn.execute("SELECT value FROM facts WHERE user_id=? AND key=?", ("wei", "city")).fetchone()
```

agent 對話開始時 load 該 user 所有 facts 進 system prompt：

```python
facts = conn.execute("SELECT key, value FROM facts WHERE user_id=?", (user_id,)).fetchall()
system_prompt = "User facts:\n" + "\n".join(f"- {k}: {v}" for k, v in facts)
```

### 4.2 向量 memory（適合無結構的事件 / 對話）

把「使用者過去說過的話」存 vector store，需要時 semantic search 找相關。

例：使用者今天說「我喜歡日式風格」，下次他問「推薦一家餐廳」時 agent 撈到這條 memory → 推薦日式餐廳。

---

## 5. RAG（Retrieval-Augmented Generation）

把**大量外部知識**（公司 SOP / 產品 doc / 法規）切塊、embed 進 vector DB，agent 收到問題時找相關 chunk 塞進 context。

### 標準 RAG pipeline

```
1. 文件 → chunk（500-1500 token / chunk）
2. chunk → embedding（OpenAI text-embedding-3 / Cohere / 本地）
3. embedding → vector DB（Pinecone / Weaviate / pgvector / Chroma）
4. 查詢時：query → embedding → similarity search → top-K chunk
5. 把 top-K chunk 塞進 prompt 給 LLM
```

### 簡化範例（chromadb）

```python
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")
embedder = embedding_functions.OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"])

collection = client.get_or_create_collection("company_docs", embedding_function=embedder)

# 索引文件
collection.add(
    documents=["產品 A 規格...", "公司假期政策...", "客戶 X 過往案例..."],
    metadatas=[{"src": "doc1.md"}, {"src": "hr.md"}, {"src": "crm.md"}],
    ids=["d1", "d2", "d3"],
)

# 查詢
results = collection.query(
    query_texts=["請假怎麼申請"],
    n_results=3,
)
# results['documents'][0] = ["公司假期政策...", ...]
```

### Vector DB 選擇

| DB | 性質 | 適合 |
|---|---|---|
| **Chroma** | 嵌入式、Python first | 開發階段 / 小規模 |
| **pgvector** | Postgres extension | 已用 PG / 想單一 DB |
| **Pinecone** | 雲端託管 | 不想自運維 |
| **Weaviate** | 自託管 / 雲端 | 需要 hybrid search（vector + keyword） |
| **Qdrant** | 高性能、Rust 寫 | 大規模 / 自託管 |

---

## 6. Contextual Retrieval — Anthropic 2024 的優化

標準 RAG 有個常見問題：chunk 失去上下文。

例如某條 chunk 是「該功能於 2026 年 3 月起停用」——但「該功能」指什麼？前面的 chunk 才講。

**Contextual Retrieval**（Anthropic 2024）做法：**embed 之前，先讓 LLM 給每個 chunk 加一段 50-100 字「這個 chunk 在文件中的位置 + 主題」**。

```python
def contextualize(chunk, full_doc):
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": f"""
給定整篇文件：
{full_doc}

給定其中一個 chunk：
{chunk}

請用 50 字繁中說明這個 chunk 在文件中的位置 + 主題。直接給答案不解釋。
"""}],
    )
    return resp.content[0].text

# 索引時：
for chunk in chunks:
    ctx = contextualize(chunk, full_doc)
    enriched = f"[CONTEXT: {ctx}]\n\n{chunk}"
    collection.add(documents=[enriched], ...)
```

Anthropic 報告 retrieval 召回率提升 35-49%。**成本**：每 chunk 多 1 次 LLM call（用 cheap model + prompt caching 大幅減）。

---

## 7. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 2 — Sessions, Context Windows & Turns**：context window / compaction
- **Section 6 — Memory & Guidance**：persistent memory / RAG / contextual retrieval

---

## 8. 動手練習

### 練習 13.1：Session memory 包進 agentz_mini

擴 Ch 12 的 `Agent` class 加 `session_messages` 屬性，`run(user_message)` 後保留對話。實作 SUMMARIZE_THRESHOLD 自動壓縮。

**成功標準**：跑 30 輪對話，context size 始終 < 50K token。

### 練習 13.2：用 Chroma 做 RAG

挑你 5-10 個文件（doc / blog / SOP），切 chunk、embed 進 chroma，寫一個 agent 能依問題撈相關 chunk 回答。

**成功標準**：問一個只能從你私人文件答得出的問題，agent 答對。

### 練習 13.3：Contextual Retrieval A/B 對比

在練習 13.2 基礎上加 contextual retrieval（每 chunk 加 50 字 context），跑同一組問題 5 個，比較有/沒 contextualize 的召回率。

**成功標準**：用表格顯示 5 題的 contextualize on/off 結果，能說出哪個版本好、為什麼。

---

## 9. 你做完這一章後 ✅

- [ ] 知道 LLM 沒記憶的本質、為何要 memory 層
- [ ] 知道 session / long-term / RAG 三種 memory
- [ ] 會做 session message 壓縮 / 摘要
- [ ] 寫過 SQLite-backed long-term memory
- [ ] 跑過 chromadb RAG pipeline
- [ ] 知道 Contextual Retrieval 為什麼有用
- [ ] 跑完練習 13.1 / 13.2 / 13.3

打勾 5 個以上，進 [Ch 14 — Multi-agent](../ch14_multi_agent/)。

---

## 9a. 常見地雷

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **chunk 切太大 / 太小** | retrieval 不準 | 中文 200-500 字 / 英文 500-1000 token, 重疊 10-15% |
| **沒 contextualize** | chunk 失去上下文 | 加 50-100 字 chunk-position context（[§6 contextual retrieval](#6-contextual-retrieval)）|
| **embedding model 換掉**  | 舊資料 retrieval 突然全錯 | embedding model + version 寫死，每次升級全 re-embed |
| **mixed language** | 中英混搭召回率差 | 用 multilingual model (cohere multilingual / openai 3-large) |
| **沒 metadata filter** | 答案被無關文件淹沒 | 加 `where={"category": "policy"}` 等 filter |
| **k 太大 / 太小** | k=20 太雜、k=3 漏掉 | 從 k=5 起手、看 result 調 |
| **沒 rerank** | top-k 順序很爛 | 加 cohere rerank / cross-encoder 二次排序 |
| **session memory 沒截斷** | 第 30 輪對話 context 撞 200K | 用 summarizer agent 每 10 輪壓縮成 1 段 |
| **vector DB 改路徑** | 重啟後 collection 消失 | `PersistentClient(path=...)` 用絕對路徑 + 不要砍 |
| **chunk overlap 沒設** | 跨 chunk 邊界資訊掉 | overlap 50-100 char / 50 token |
| **PII 直接進 vector DB** | 隱私外洩 | 索引前 mask（姓名/電話/email/身分證）, 或用本地 embedding |
| **RAG 蓋掉 LLM 知識** | 簡單問題給超詳細 RAG 答案 | LLM 判斷「要不要查 RAG」, 簡單問直答 |

---

## 9b. 在這頁練 contextual retrieval 的 prompt

Contextual Retrieval（§6）的核心是「給 chunk 加一段 50-100 字的位置 + 主題」。試試看：

<LLMTryout
  title="Ch 13 in-page tryout — contextual retrieval"
  defaultSystem="你是 contextual retrieval 助手。看使用者給的「整篇文件」+「一個 chunk」，用 50 字繁中說明這個 chunk 在文件中的位置 + 主題。直接給答案不解釋。"
  defaultPrompt="整篇文件：『公司假期政策。第一條：年假 14 天。第二條：病假 30 天需診斷書。第三條：颱風假比照政府公告。』 chunk：『需診斷書。』" />

## 10. 補充閱讀

- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [Chroma 文件](https://docs.trychroma.com)
- [pgvector](https://github.com/pgvector/pgvector)
- `datawhalechina/all-in-rag`（7K⭐）— RAG 中文全棧指南
- ai-dict Memory & Guidance 段

---

> 🛟 **卡關時看這裡**：
> - RAG retrieval 撈錯 / embedding dim mismatch → [故障排除 § Memory/RAG](https://symbiosis11503.github.io/agent-z/troubleshooting)
> - session memory + RAG 起手範式 → [速查卡](https://symbiosis11503.github.io/agent-z/cheatsheet)
> - Fine-tuning vs RAG 怎麼選 → [名詞表 § 常被混淆的 pair](https://symbiosis11503.github.io/agent-z/glossary/taiwan-misc#_11-常被混淆的-pair-對比)
