"""Ch 13 Session memory + summarize skeleton — 練習 13.1。"""
from __future__ import annotations

import os
import sys

import anthropic

SUMMARIZE_THRESHOLD = 20  # 超過 20 則就壓老的


def format_messages(msgs: list[dict]) -> str:
    return "\n".join(f"{m['role']}: {m.get('content', '')[:200]}" for m in msgs)


def maybe_summarize(client, messages: list[dict]) -> list[dict]:
    """超過 threshold 就把舊的 10 則壓成 summary。"""
    if len(messages) <= SUMMARIZE_THRESHOLD:
        return messages
    # TODO 13.1: call LLM 摘要 messages[:10] 成 100 字繁中
    # TODO 13.1: 回傳 [summary system msg] + messages[10:]
    raise NotImplementedError("Complete maybe_summarize for exercise 13.1")


def repl():
    client = anthropic.Anthropic()
    messages = []
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=400,
            messages=messages,
        )
        assistant_text = resp.content[0].text
        messages.append({"role": "assistant", "content": assistant_text})
        print(f"\n{assistant_text}\n")
        print(f"  (usage in={resp.usage.input_tokens} out={resp.usage.output_tokens}, msgs={len(messages)})")

        messages = maybe_summarize(client, messages)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    repl()
