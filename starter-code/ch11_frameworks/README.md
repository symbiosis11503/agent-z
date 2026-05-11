# Ch 11 — Framework 5 版本對照 starter

對應 [AgentZ Ch 11](../../chapters/ch11_frameworks/) 練習 11.1 / 11.2 / 11.3。

**同一個任務**「研究 X、用 search 工具找事實、輸出 200 字繁中摘要」在 5 種寫法下對照。

## 5 個檔案 5 種寫法

| 檔案 | Framework | 行數 | 風格 |
|---|---|---|---|
| `vanilla.py` | 無，純 Anthropic SDK | ~85 | 自己寫 ReAct loop、tool_use schema 手動 |
| `langgraph_version.py` | LangGraph | ~50 | `create_react_agent` 一行包好 |
| `crewai_version.py` | CrewAI | ~55 | Agent + Task + Crew role-based |
| `smolagents_version.py` | Smolagents (HF) | ~45 | CodeAct — LLM 寫 Python 當 action |
| `pydantic_ai_version.py` | Pydantic AI | ~55 | Type-safe `output_type=Pydantic model` |

## 跑

```bash
cd starter-code/ch11_frameworks
export ANTHROPIC_API_KEY="sk-ant-..."

# baseline 不裝 framework
uv run vanilla.py "vibe coding"

# 各家獨立裝（避免一次 1GB+）
uv pip install -e ".[langgraph]"   && uv run langgraph_version.py "react"
uv pip install -e ".[crewai]"      && uv run crewai_version.py "grpo"
uv pip install -e ".[smolagents]"  && uv run smolagents_version.py "vibe coding"
uv pip install -e ".[pydantic_ai]" && uv run pydantic_ai_version.py "react"
```

## 觀察重點

跑完 5 個版本你會發現:

| 維度 | vanilla | LangGraph | CrewAI | Smolagents | Pydantic AI |
|---|---|---|---|---|---|
| **code 量** | 多 | 少 | 中 | 少 | 中 |
| **dependency 重** | < 5MB | 200MB+ | 100MB+ | 50MB+ | 20MB |
| **適合單 agent** | ✅ | ✅ | ❌ verbose | ✅ | ✅ |
| **適合 multi-agent** | ❌ 自己包 | ✅ graph 強 | ✅ role 自然 | △ | ❌ |
| **結構化輸出** | △ 手 parse | △ | △ | △ | ✅ type-safe |
| **CodeAct 風格** | ❌ | ❌ | ❌ | ✅ 默認 | ❌ |
| **debug 透明度** | ✅ | △ | ❌ 黑盒 | △ | ✅ |

## 怎麼選？（AgentZ Ch 11 §4 決策樹複習）

```
單 agent + 簡單 ─────► vanilla 或 Pydantic AI
單 agent + 結構化輸出 ─► Pydantic AI
multi-agent + role ──► CrewAI
複雜 state machine ──► LangGraph
要 LLM 寫 code ─────► Smolagents
production governance ► vanilla + 自己加 audit/replay/cost cap (Ch 15 案例)
```

## 練習

- **11.1**：跑 vanilla.py + langgraph_version.py，比較 verbose output 差異
- **11.2**：把 5 個版本的 search() 都換成真的 Tavily / Serper API
- **11.3**：選一個 framework 改造成 multi-agent（Pipeline 模式 / 參考 ch14 starter）

## 成功標準

- 至少 2 個 framework 版本能跑、輸出合理摘要
- 你能說出「我選 X，原因是 Y」（不是「最多 star」這種理由）

## 注意

- 每家版本 API 都 evolve 中，這份是 2026-05 snapshot
- 跑不起來請看各家最新 docs，pyproject.toml 列的版本是當時驗證能跑的
- 5 個 framework 全裝會吃 400MB+ disk + 衝突可能性高，**逐家獨立裝最安全**
