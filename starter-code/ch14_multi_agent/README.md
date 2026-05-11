# Ch 14 — Multi-Agent 三種架構 starter

對應 [AgentZ Ch 14](../../chapters/ch14_multi_agent/) 練習 14.1 / 14.2 / 14.3。

每個檔案是一種架構的完整跑得起來實作（不是骨架），給你 copy-paste 改成自己的版本。

## 跑

```bash
cd starter-code/ch14_multi_agent
uv sync
export ANTHROPIC_API_KEY="sk-ant-..."

# 14.1 — Pipeline: research → write → review 序列
uv run pipeline.py "用繁中介紹 vibe coding 給工程師"

# 14.2 — Supervisor: 主管派工
uv run supervisor.py "幫我寫一份關於 ReAct paper 的繁中筆記，含批判"

# 14.3 — Blackboard: 共享 workspace 多 agent 自由參與
uv run blackboard.py "用繁中介紹 GRPO 給已會 RL 的人"
```

## 三種架構的精神

| 架構 | 控制 | 適合 | 範例 |
|---|---|---|---|
| **Pipeline** | 硬流程 A→B→C | 流程明確、每階段 well-defined | research → write → review |
| **Supervisor** | 主管動態決定 | 流程 partly defined、需要動態派工 | 客服分類 → 派專科 worker |
| **Blackboard** | 沒有主管、共享狀態 | 開放性、研究型、創作 | 多視角整合 / brainstorm |

## 練習

- **14.1**: 跑 `pipeline.py`，把 reviewer verdict 改成 enum `pass/revise/fail` 並輸出 JSON
- **14.2**: 跑 `supervisor.py`，加第 4 個 worker `editor`（潤稿），讓 supervisor 學會在 critic 後派 editor
- **14.3**: 跑 `blackboard.py`，把固定順序改成「每輪隨機洗牌 4 個 agent」，看結果有沒有變

## 成功標準

- 三個都能跑、不會炸 (set ANTHROPIC_API_KEY)
- Pipeline 看到 3 段輸出（research / draft / review）
- Supervisor 看到 supervisor 派 worker 至少 2 次
- Blackboard 看到至少 2 個 agent 寫東西（不全部 pass）

## 成本估算

每次跑大約：
- Pipeline: ~5K tokens, Haiku $0.01 + Sonnet $0.02 = ~$0.03
- Supervisor: ~8K tokens, Sonnet ~$0.03
- Blackboard: 16-32 worker calls × Haiku ~ $0.05

跑壞時注意：supervisor.py / blackboard.py 都有 max_steps / max_rounds 上限，不會無限燒。
