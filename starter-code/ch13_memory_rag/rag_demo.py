"""Ch 13 Chroma RAG skeleton — 練習 13.2 + 13.3。"""
from __future__ import annotations

import os
import sys

import anthropic
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "./chroma_db"
DOCS = [
    "公司假期政策：年假 14 天、病假 30 天（需診斷書）、颱風假比照政府。",
    "出差申請流程：填表 → 主管核可 → 財務預支 → 出差結束 24 小時內補完憑證。",
    "客戶 A 過往案例：2025 年購買 ERP 模組，2026 年續約並加購 BI dashboard。",
    "技術棧偏好：後端 Python + FastAPI、前端 vanilla JS、DB Postgres。",
    "週會節奏：每週一 10am 例會、雙週四 3pm 技術討論。",
]


def build_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
    )
    collection = client.get_or_create_collection(
        "agentz_demo", embedding_function=embedder
    )
    # TODO 13.2: collection.add documents=DOCS, ids=[...]
    # TODO 13.3: contextualize each doc using Claude before adding
    raise NotImplementedError("Complete build_collection for exercise 13.2")


def query(question: str, k: int = 3):
    """Retrieve top-K chunks then ask Claude with them."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
    )
    collection = client.get_collection("agentz_demo", embedding_function=embedder)
    results = collection.query(query_texts=[question], n_results=k)
    chunks = results["documents"][0]

    context_block = "\n".join(f"- {c}" for c in chunks)
    anth = anthropic.Anthropic()
    resp = anth.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"已知:\n{context_block}\n\n問題：{question}\n\n根據已知回答（繁中）。"
        }]
    )
    return resp.content[0].text, chunks


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY") or not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: set both ANTHROPIC_API_KEY and OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)
    print("Building collection...")
    build_collection()
    print("Querying...\n")
    q = " ".join(sys.argv[1:]) or "颱風假怎麼算？"
    answer, chunks = query(q)
    print(f"=== Retrieved chunks ===\n" + "\n".join(f"- {c}" for c in chunks))
    print(f"\n=== Answer ===\n{answer}")
