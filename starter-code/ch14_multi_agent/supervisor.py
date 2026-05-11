"""Ch 14 Supervisor multi-agent — orchestrator 看任務、決定派 worker。

跑：
    uv run supervisor.py "幫我寫一份關於 ReAct paper 的繁中筆記，含批判"

架構：
    supervisor (Sonnet) 看 task → 決定派哪個 worker (researcher / writer / critic)
    每個 worker 跑完回報 → supervisor 決定下一步或結束。
"""
from __future__ import annotations

import json
import os
import sys

import anthropic


WORKERS = {
    "researcher": (
        "你是 research worker。給定 query，輸出 5 條 bullet point 的關鍵事實。"
        "每條一句、有具體例子或數字。"
    ),
    "writer": (
        "你是 writer worker。給定研究筆記 + 目標，寫 300 字繁中文章。"
        "結構：引子 → 主體 → 結尾。"
    ),
    "critic": (
        "你是 critic worker。給定文章，輸出 (1) 3 個優點 (2) 3 個缺點 (3) 改進建議。"
    ),
}


def call_worker(worker_name: str, task: str) -> str:
    """讓 worker 跑。"""
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1200,
        system=WORKERS[worker_name],
        messages=[{"role": "user", "content": task}],
    )
    return resp.content[0].text


SUPERVISOR_SYSTEM = """你是 supervisor agent。你有 3 個 worker:
- researcher: 找事實
- writer: 寫文章
- critic: 批判文章

對話流：每輪你要看狀況、回 JSON: {"action": "delegate", "worker": "researcher|writer|critic", "task": "<具體 task>"}
若認為任務完成 → 回 {"action": "complete", "summary": "<最終結果>"}

不要自己直接寫文章 — 交給 worker。
"""


def supervisor_loop(user_task: str, max_steps: int = 6) -> dict:
    """Supervisor loop — 最多 6 步避免燒錢。"""
    client = anthropic.Anthropic()
    history = []
    transcript = []

    history.append({
        "role": "user",
        "content": f"User 給的任務: {user_task}\n\n請決定第一步該派誰、做什麼。",
    })

    for step in range(max_steps):
        resp = client.messages.create(
            model="claude-sonnet-4-6",  # supervisor 用較強模型
            max_tokens=800,
            system=SUPERVISOR_SYSTEM,
            messages=history,
        )
        sup_msg = resp.content[0].text
        print(f"\n=== Step {step+1}: Supervisor ===\n{sup_msg}")

        # 解析 JSON action
        try:
            # 找 JSON block
            start = sup_msg.find("{")
            end = sup_msg.rfind("}") + 1
            action = json.loads(sup_msg[start:end])
        except (ValueError, json.JSONDecodeError):
            print("⚠️  Supervisor 沒回合法 JSON，停止")
            return {"transcript": transcript, "error": "invalid_json", "raw": sup_msg}

        history.append({"role": "assistant", "content": sup_msg})

        if action["action"] == "complete":
            print(f"\n=== ✅ Done ===\n{action['summary']}")
            return {"transcript": transcript, "summary": action["summary"]}

        if action["action"] == "delegate":
            worker = action["worker"]
            worker_task = action["task"]
            print(f"\n--- Worker {worker} 跑 ---\nTask: {worker_task}")
            worker_output = call_worker(worker, worker_task)
            print(worker_output)
            transcript.append({"step": step + 1, "worker": worker, "task": worker_task, "output": worker_output})
            history.append({
                "role": "user",
                "content": f"Worker {worker} 回報:\n{worker_output}\n\n下一步?",
            })

    return {"transcript": transcript, "error": "max_steps_exhausted"}


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: set ANTHROPIC_API_KEY env var first", file=sys.stderr)
        sys.exit(1)
    task = " ".join(sys.argv[1:]) or "幫我寫一份關於 ReAct paper 的繁中筆記，含批判"
    result = supervisor_loop(task)
    print(f"\nFinal transcript: {len(result.get('transcript', []))} worker calls")
