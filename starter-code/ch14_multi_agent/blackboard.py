"""Ch 14 Blackboard multi-agent — 共享狀態 + 自由參與。

跑：
    uv run blackboard.py "用繁中介紹 GRPO 給已會 RL 的人"

架構：
    所有 agent 看同一個 shared workspace (blackboard)。
    每輪 agent 自己決定要不要動、要動什麼、寫回 blackboard。
    其他 agent 看到 blackboard 變化、決定要不要回應。

適合：研究 / 創作 / 開放性問題。不適合：流程明確的任務（用 Pipeline 比較好）。
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import anthropic


@dataclass
class Blackboard:
    """共享 workspace。"""
    topic: str
    notes: list[dict] = field(default_factory=list)  # 每條: {"author": ..., "text": ..., "step": ...}

    def render(self) -> str:
        """為 LLM 渲染目前狀態。"""
        if not self.notes:
            return f"(empty blackboard, topic: {self.topic})"
        lines = [f"Topic: {self.topic}", "Blackboard contents:"]
        for i, n in enumerate(self.notes):
            lines.append(f"[{i+1}] ({n['author']}, step {n['step']}): {n['text']}")
        return "\n".join(lines)

    def add(self, author: str, text: str, step: int):
        self.notes.append({"author": author, "text": text, "step": step})


AGENTS = {
    "fact_finder": {
        "system": (
            "你是 fact-finder agent。看到 blackboard 後決定: "
            "(1) 還缺什麼事實？需要時加 1-2 條 [fact] 到 blackboard "
            "(2) 已經夠了 → 回 'pass'。不要重複別人寫過的事實。"
        ),
        "tag": "[fact]",
    },
    "structurer": {
        "system": (
            "你是 structure agent。看到 blackboard 後決定: "
            "(1) 事實散亂 → 寫一段 [structure] 提出大綱建議 "
            "(2) 大綱清楚了 → 回 'pass'。"
        ),
        "tag": "[structure]",
    },
    "critic": {
        "system": (
            "你是 critic agent。看 blackboard 內容後決定: "
            "(1) 看到事實或大綱有問題 → 寫一段 [critique] 指出 "
            "(2) 沒問題 → 回 'pass'。"
        ),
        "tag": "[critique]",
    },
    "writer": {
        "system": (
            "你是 writer agent。看 blackboard 後決定: "
            "(1) 事實 + 結構都齊了 → 寫一段 [draft] 300 字繁中文章 "
            "(2) 還沒齊 → 回 'pass'。"
        ),
        "tag": "[draft]",
    },
}


def call_agent(agent_name: str, blackboard: Blackboard) -> Optional[str]:
    """讓 agent 看 blackboard、回應。回 None = pass。"""
    spec = AGENTS[agent_name]
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=600,
        system=spec["system"],
        messages=[{"role": "user", "content": blackboard.render()}],
    )
    text = resp.content[0].text.strip()
    if text.lower().startswith("pass") or len(text) < 20:
        return None
    return text


def blackboard_run(topic: str, max_rounds: int = 4) -> Blackboard:
    """跑 blackboard 多輪、直到 writer 寫出 draft 或 max_rounds 到。"""
    bb = Blackboard(topic=topic)

    # 固定順序: fact → structure → critic → writer，每輪 4 個 agent 都過一次
    agent_order = ["fact_finder", "structurer", "critic", "writer"]

    for round_i in range(max_rounds):
        print(f"\n========== Round {round_i+1} ==========")
        any_action = False
        for agent_name in agent_order:
            print(f"\n--- {agent_name} ---")
            out = call_agent(agent_name, bb)
            if out is None:
                print("(pass)")
                continue
            bb.add(agent_name, out, step=round_i + 1)
            print(out)
            any_action = True

            # writer 寫了 draft 就結束
            if agent_name == "writer":
                print(f"\n✅ Writer 寫了 draft，blackboard 完成")
                return bb

        if not any_action:
            print(f"\n⚠️  Round {round_i+1} 全 pass，blackboard 停滯，結束")
            break

    return bb


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    topic = " ".join(sys.argv[1:]) or "用繁中介紹 GRPO 給已會 RL 的人"
    bb = blackboard_run(topic)
    print(f"\n========== Final blackboard ==========")
    print(bb.render())
    print(f"\nTotal notes: {len(bb.notes)}")
