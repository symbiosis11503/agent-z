"""Ch 14 Cross-Model Review skeleton — 練習 14.4。

用兩個不同模型互審，比較三版（model-A only / model-B only / cross-reviewed）品質。

成功標準：能具體指出 cross-review 抓到了哪些單一模型漏掉的問題。

需要設定環境變數：
  ANTHROPIC_API_KEY — for Claude
  OPENAI_API_KEY   — for GPT (or use another provider)
"""
from __future__ import annotations

import os

import anthropic

# Optional: uncomment if you have openai installed
# import openai

MODEL_A = "claude-haiku-4-5"  # Claude as model A
MODEL_B = "claude-sonnet-4-5"  # Use a different model as B (swap to GPT if you have openai)


def generate_with_claude(client: anthropic.Anthropic, task: str, model: str = MODEL_A) -> str:
    resp = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": task}],
    )
    return resp.content[0].text


def review_with_claude(client: anthropic.Anthropic, task: str, draft: str, model: str = MODEL_A) -> str:
    """Have a model review another model's output."""
    # TODO 14.4: write a review prompt that asks the reviewer to:
    # 1. List factual errors or omissions
    # 2. Rate completeness (1-5)
    # 3. Suggest specific improvements
    raise NotImplementedError("Complete review_with_claude for exercise 14.4")


def revise_with_model(client: anthropic.Anthropic, task: str, review: str, model: str = MODEL_A) -> str:
    """Revise the draft based on cross-model review feedback."""
    # TODO 14.4: incorporate review feedback to produce an improved version
    raise NotImplementedError("Complete revise_with_model for exercise 14.4")


def main():
    client = anthropic.Anthropic()

    task = "Compare PostgreSQL vs MySQL for a startup's first production database. " \
           "Cover performance, scalability, ecosystem, and operational complexity. " \
           "Write 200-300 words in Traditional Chinese."

    print("=" * 60)
    print("Step 1: Generate with Model A (Claude Haiku)")
    print("=" * 60)
    draft_a = generate_with_claude(client, task, MODEL_A)
    print(draft_a[:500])
    print("...\n")

    print("=" * 60)
    print("Step 2: Generate with Model B (Claude Sonnet)")
    print("=" * 60)
    draft_b = generate_with_claude(client, task, MODEL_B)
    print(draft_b[:500])
    print("...\n")

    print("=" * 60)
    print("Step 3: Cross-review (B reviews A, A reviews B)")
    print("=" * 60)
    try:
        review_of_a = review_with_claude(client, task, draft_a, MODEL_B)
        review_of_b = review_with_claude(client, task, draft_b, MODEL_A)
        print(f"Review of A by B:\n{review_of_a[:300]}...\n")
        print(f"Review of B by A:\n{review_of_b[:300]}...\n")
    except NotImplementedError:
        print("[skip] review_with_claude not implemented yet — complete the TODO!\n")
        return

    print("=" * 60)
    print("Step 4: Revise based on cross-review")
    print("=" * 60)
    try:
        revised = revise_with_model(client, task, review_of_a, MODEL_A)
        print(f"Cross-reviewed final:\n{revised[:500]}...\n")
    except NotImplementedError:
        print("[skip] revise_with_model not implemented yet — complete the TODO!\n")
        return

    print("=" * 60)
    print("Step 5: Compare the 3 versions")
    print("=" * 60)
    print(f"  Model A only:     {len(draft_a)} chars")
    print(f"  Model B only:     {len(draft_b)} chars")
    print(f"  Cross-reviewed:   {len(revised)} chars")
    print()
    print("Your job: read all 3 and identify what cross-review caught that single-model missed.")


if __name__ == "__main__":
    main()
