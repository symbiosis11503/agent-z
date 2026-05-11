"""Ch 14 Pipeline multi-agent — research → write → review 序列 flow。

跑：
    uv run pipeline.py "用繁中介紹 vibe coding 給工程師"
"""
from __future__ import annotations

import os
import sys

import anthropic


def role_call(role_system: str, user_msg: str, model: str = "claude-haiku-4-5") -> str:
    """單 agent call — system prompt 定義角色、user_msg 為輸入。"""
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=1500,
        system=role_system,
        messages=[{"role": "user", "content": user_msg}],
    )
    return resp.content[0].text


def pipeline(task: str) -> dict:
    """Pipeline: A → B → C 序列流。

    每個 stage 的輸出餵下個 stage 的輸入。
    """
    print(f"\n=== Stage 1: Researcher ===")
    research = role_call(
        role_system=(
            "你是 research agent。給定 topic，輸出 5 條 bullet point 的 key facts。"
            "每條一句話，盡量包含具體例子或數字。"
        ),
        user_msg=f"Topic: {task}",
    )
    print(research)

    print(f"\n=== Stage 2: Writer ===")
    draft = role_call(
        role_system=(
            "你是 writer agent。給定研究筆記，寫一篇 300 字繁中介紹文。"
            "結構：引子（1 句）→ 主體（3-4 段）→ 結尾（1 句 takeaway）。"
        ),
        user_msg=f"研究筆記：\n{research}\n\n目標讀者: 工程師。寫成完整文章。",
    )
    print(draft)

    print(f"\n=== Stage 3: Reviewer ===")
    review = role_call(
        role_system=(
            "你是 reviewer agent。檢查文章 (1) 是否有事實錯誤 (2) 結構是否清楚 (3) 是否符合 300 字。"
            "輸出 3 段 critique + 1 段「整體 verdict: pass / revise」。"
        ),
        user_msg=f"原 task: {task}\n\n文章:\n{draft}",
        model="claude-sonnet-4-6",  # reviewer 用大模型
    )
    print(review)

    return {
        "task": task,
        "research": research,
        "draft": draft,
        "review": review,
    }


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    task = " ".join(sys.argv[1:]) or "用繁中介紹 vibe coding 給工程師"
    result = pipeline(task)
    print("\n=== Pipeline complete ===")
    print(f"Task: {result['task']}")
    print(f"Draft length: {len(result['draft'])} chars")
