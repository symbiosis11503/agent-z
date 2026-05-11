"""
agentz_mini — Ch 12 練習 12.1 starter skeleton.

按照 Ch 12 §3 完成這個 module。完整版~150 行。
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable

import anthropic


# ─── @tool decorator ───────────────────────────────────────────────────────

_TYPE_MAP = {str: "string", int: "integer", float: "number", bool: "boolean",
             list: "array", dict: "object"}


@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict
    fn: Callable


def tool(fn: Callable) -> ToolSpec:
    """Decorator: typed Python function → ToolSpec."""
    sig = inspect.signature(fn)
    props, required = {}, []
    for name, param in sig.parameters.items():
        json_type = _TYPE_MAP.get(param.annotation, "string")
        props[name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return ToolSpec(
        name=fn.__name__,
        description=(fn.__doc__ or "").strip() or fn.__name__,
        input_schema={"type": "object", "properties": props, "required": required},
        fn=fn,
    )


# ─── Result / Usage / Step ─────────────────────────────────────────────────

@dataclass
class Step:
    kind: str
    payload: Any


@dataclass
class Usage:
    input: int = 0
    output: int = 0


@dataclass
class RunResult:
    answer: str
    steps: list[Step] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    cost: float = 0.0


# ─── Cost catalog ──────────────────────────────────────────────────────────

_PRICE = {
    "claude-haiku-4-5": (0.80, 4.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-7": (15.00, 75.00),
}


class CostExceeded(Exception):
    pass


# ─── Agent ─────────────────────────────────────────────────────────────────

class Agent:
    def __init__(
        self,
        model: str = "claude-haiku-4-5",
        tools: list[ToolSpec] | None = None,
        system: str = "",
        max_iter: int = 10,
        cost_cap_usd: float = 1.0,
    ):
        self.client = anthropic.Anthropic()
        self.model = model
        self.tools = tools or []
        self.system = system
        self.max_iter = max_iter
        self.cost_cap_usd = cost_cap_usd
        self._tool_by_name = {t.name: t for t in self.tools}

    def run(self, user_message: str) -> RunResult:
        """
        完成這個 — 練習 12.1 的核心。

        Reference (Ch 12 §3.3):
        1. result = RunResult(answer="")
        2. messages = [{"role": "user", "content": user_message}]
        3. for _ in range(self.max_iter):
            a. resp = client.messages.create(model, tools=..., messages=messages)
            b. update cost, raise CostExceeded if over cap
            c. append step / append assistant message
            d. if stop_reason != "tool_use": return result with final answer
            e. execute tool_uses, append tool_results
        """
        raise NotImplementedError("Complete Agent.run for exercise 12.1")

    # 練習 12.2: 加 run_with_reflection(task, target_score=8)
    # 練習 12.3: 把 result.steps 序列化成 JSON 並可 reload replay


if __name__ == "__main__":
    # Smoke test — 寫完上面再跑
    pass
