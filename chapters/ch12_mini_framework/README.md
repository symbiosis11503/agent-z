# Ch 12 — 從零造輪：寫一個 Mini Agent Framework

> **90-120 分鐘**。讀完你會懂：怎麼把 Ch 9-10 的 raw API 包成一個重用 framework，~200 行 Python。
>
> 動手練習：跟著章節寫完 `agentz_mini.py`、用它跑 3 個不同 task。
>
> 前置：完成 [Ch 11](../ch11_frameworks/) — 知道現成 framework 長什麼樣。

---

## 1. 為什麼要造輪？

「能用 LangGraph 為什麼還要造輪？」

三個好答案：
1. **你不會懂 framework 怎麼運作，除非自己寫一個**。
2. **production 場景常要極簡 + 完全自控**——LangGraph 上線 Lambda / Edge 你會痛苦。
3. **本書 v2 sandbox / Helix V3 都是這種規模**——能跟你自己的程式深度整合。

寫完這章，你會發現「framework 沒那麼神」——它只是 raw loop 加上 nice 的抽象。

---

## 2. 我們要造的東西

`agentz_mini.py` ~200 行 Python，提供：

```python
@tool
def get_weather(city: str) -> str:
    return f"{city}: 26°C, 晴"

@tool
def search(query: str) -> str:
    return f"results for: {query}"

agent = Agent(
    model="claude-haiku-4-5",
    tools=[get_weather, search],
    system="You are a helpful assistant.",
)

result = agent.run("比較台北跟東京天氣")
print(result.answer)
print(f"Tokens: {result.usage.input}/{result.usage.output}")
print(f"Cost: ${result.cost:.4f}")
print(f"Steps: {len(result.steps)}")
```

支援：
- `@tool` decorator 自動產生 input_schema（讀 type hints + docstring）
- 完整 tool-use loop + max_iter cap
- token / cost tracking + budget cap
- step trace 紀錄（給 audit / replay 用）
- parallel tool call

---

## 3. 完整實作

### 3.1 `@tool` decorator

```python
import inspect, json
from typing import Callable, Any
from dataclasses import dataclass, field

@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict
    fn: Callable

_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}

def tool(fn: Callable) -> ToolSpec:
    """Decorator that turns a typed Python function into a ToolSpec."""
    sig = inspect.signature(fn)
    props = {}
    required = []
    for name, param in sig.parameters.items():
        py_type = param.annotation
        json_type = _TYPE_MAP.get(py_type, "string")
        props[name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return ToolSpec(
        name=fn.__name__,
        description=(fn.__doc__ or "").strip() or fn.__name__,
        input_schema={
            "type": "object",
            "properties": props,
            "required": required,
        },
        fn=fn,
    )
```

### 3.2 Step trace + Result

```python
@dataclass
class Step:
    kind: str  # "llm_call" | "tool_call" | "tool_result" | "final"
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
```

### 3.3 主 Agent class

```python
import anthropic, asyncio

# Q1 2026 pricing per million token
_PRICE_TABLE = {
    "claude-haiku-4-5": (0.80, 4.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-7": (15.00, 75.00),
}

class CostExceeded(Exception): ...

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

    def _to_anthropic_tools(self):
        return [
            {"name": t.name, "description": t.description, "input_schema": t.input_schema}
            for t in self.tools
        ]

    def _execute_tool(self, name: str, input_data: dict) -> str:
        if name not in self._tool_by_name:
            return f"ERROR: unknown tool {name}"
        try:
            return str(self._tool_by_name[name].fn(**input_data))
        except Exception as e:
            return f"ERROR: {type(e).__name__}: {e}"

    def _add_cost(self, result: RunResult, usage):
        p_in, p_out = _PRICE_TABLE.get(self.model, (1.0, 5.0))
        result.usage.input += usage.input_tokens
        result.usage.output += usage.output_tokens
        result.cost = (
            result.usage.input * p_in + result.usage.output * p_out
        ) / 1_000_000
        if result.cost > self.cost_cap_usd:
            raise CostExceeded(f"${result.cost:.4f} > ${self.cost_cap_usd}")

    def run(self, user_message: str) -> RunResult:
        result = RunResult(answer="")
        messages = [{"role": "user", "content": user_message}]

        for _ in range(self.max_iter):
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                system=self.system or None,
                tools=self._to_anthropic_tools(),
                messages=messages,
            )
            self._add_cost(result, resp.usage)
            result.steps.append(Step("llm_call", {
                "stop": resp.stop_reason,
                "in_tok": resp.usage.input_tokens,
                "out_tok": resp.usage.output_tokens,
            }))
            messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                final = next(
                    (b.text for b in resp.content if b.type == "text"),
                    "",
                )
                result.answer = final
                result.steps.append(Step("final", final))
                return result

            # gather tool_uses + execute (parallel)
            tool_uses = [b for b in resp.content if b.type == "tool_use"]
            for b in tool_uses:
                result.steps.append(Step("tool_call", {"name": b.name, "input": b.input}))

            tool_results = []
            for b in tool_uses:
                r = self._execute_tool(b.name, b.input)
                result.steps.append(Step("tool_result", {"id": b.id, "out": r}))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": r,
                })
            messages.append({"role": "user", "content": tool_results})

        result.answer = "(reached max_iter without final answer)"
        return result
```

完整 ~150 行（含 imports）。

---

## 4. 用起來

`run_agent.py`:

```python
from agentz_mini import Agent, tool

@tool
def get_weather(city: str) -> str:
    """Return current weather for the given city."""
    fake = {"Taipei": "26°C 晴", "Tokyo": "18°C 雨", "Singapore": "31°C 雷陣雨"}
    return fake.get(city, f"unknown city: {city}")

@tool
def calc(expr: str) -> str:
    """Calculate a simple arithmetic expression."""
    import ast
    return str(eval(compile(ast.parse(expr, mode="eval"), "<expr>", "eval")))

agent = Agent(
    model="claude-haiku-4-5",
    tools=[get_weather, calc],
    system="用繁中回應。",
    max_iter=8,
    cost_cap_usd=0.10,
)

result = agent.run("比較台北跟東京現在天氣，並算 26-18 是多少。")
print(f"=== Answer ===\n{result.answer}\n")
print(f"Steps: {len(result.steps)}, in={result.usage.input}, out={result.usage.output}, cost=${result.cost:.4f}")
for s in result.steps:
    print(f"  {s.kind}: {s.payload}")
```

跑：`uv run run_agent.py`

---

## 5. 加 Replay 支援

紀錄 `result.steps` 進 JSON 後可以**重現**整次 run：

```python
import json

# 紀錄
with open("run_001.json", "w") as f:
    json.dump([{"kind": s.kind, "payload": s.payload} for s in result.steps], f, indent=2, ensure_ascii=False, default=str)

# 回放：讀 JSON、逐步 print（不再 call LLM）
def replay(path):
    with open(path) as f:
        steps = json.load(f)
    for s in steps:
        print(f"[{s['kind']}] {s['payload']}")
```

這就是 V3 / LangGraph 的 replay 機制最簡版。**production 級**會加 hash / 簽章防竄改 + 結構化儲存到 DB。Ch 15 case study 看完整版。

---

## 6. 對齊 ai-dict 名詞

本章相關 ai-dict 詞條（[繁中版](https://ai-dict.gh.miniasp.com/)）：
- **Section 5 — Handoffs**：trace / state transfer / checkpoint

---

## 7. 動手練習

### 練習 12.1：跟著章節寫完 agentz_mini.py

照 §3 寫完整個 framework。`uv run run_agent.py` 跑得起來。

**成功標準**：跑 3 個不同 task（天氣比較 / 算數 / 自選一個），三個都拿到合理答案。

### 練習 12.2：加 Reflection wrapper

在 agentz_mini.py 加 `agent.run_with_reflection(task, target_score=8)`，內部跑 act → critique → redo 直到分數夠或 max_iter。

**成功標準**：跑「寫一段 Python function 算 fibonacci」、reflection 確實 redo 提升品質。

### 練習 12.3：把 step trace 存 JSON + replay

跑一個 run 存成 `run_001.json`，寫 `replay.py` 讀回來逐步 print。

**成功標準**：JSON 可以 round-trip 不掉資訊。

---

## 8. 你做完這一章後 ✅

- [ ] 看懂 raw API → framework 的抽象提升路徑
- [ ] 寫完 `agentz_mini.py`（~150 行）能跑
- [ ] 用過 `@tool` decorator
- [ ] 跑過 3 個不同 task
- [ ] 加過 Reflection wrapper
- [ ] 會把 step trace 存 JSON / replay
- [ ] 看 framework source code 不再害怕

打勾 5 個以上，進 [Ch 13 — Memory & RAG](../ch13_memory_rag/)。

---

## 9. 補充閱讀

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- `shareAI-lab/learn-claude-code`（60K⭐）— 從 0 構建 nano claude-code-like agent harness（比這章規模大、可以當下一步）
- `datawhalechina/tiny-universe`（4.8K⭐）— 手寫 RAG / Agent / Eval 的「白盒子」
