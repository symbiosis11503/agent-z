# 名詞表

AgentZ 不重複造輪——本頁專注「**用詞 + 一句話 + 在哪章**」三件事，深入定義引用外部權威。

## 用詞對齊

| 中文 | English | 一句話 | 詳見 |
|---|---|---|---|
| 大型語言模型 | LLM (Large Language Model) | 給文字、預測下一個 token | [Ch 1](./chapters/ch01_llm_basics/) |
| Token | Token | LLM 看世界的最小單位，按它算錢 | [Ch 1 §2](./chapters/ch01_llm_basics/#2-token-是什麼) |
| 上下文視窗 | Context Window | LLM 一次看得到的最多 token | [Ch 1 §3](./chapters/ch01_llm_basics/#3-context-window-llm-的「記憶」上限) |
| 角色 | Role | system / user / assistant 三種發話者 | [Ch 1 §4](./chapters/ch01_llm_basics/#4-role-system--user--assistant) |
| 溫度 | Temperature | 隨機性旋鈕（0=穩定，1=創意） | [Ch 1 §5](./chapters/ch01_llm_basics/#5-temperature-隨機性旋鈕) |
| 提示 | Prompt | 給 LLM 的完整 specification | [Ch 2](./chapters/ch02_prompt/) |
| 思考鏈 | Chain-of-Thought (CoT) | 讓 LLM「先想再答」的提示 pattern | [Ch 2 §4](./chapters/ch02_prompt/#4-chain-of-thought-cot) |
| 工具呼叫 | Tool Use / Function Calling | LLM 生成 JSON 表達「我想 call 這個工具」 | [Ch 3 §2](./chapters/ch03_what_is_agent/#2-tool-use-llm-怎麼呼叫工具) |
| 智能體 | Agent | LLM + 工具 + 「下一步做什麼」的循環 | [Ch 3 §1](./chapters/ch03_what_is_agent/#1-agent--llm--工具--循環) |
| ReAct | ReAct (Reason + Act) | Agent 的核心循環模式 | [Ch 3 §3](./chapters/ch03_what_is_agent/#3-react-reason--act-循環) |
| CLI Agent | CLI Agent | Terminal 介面、會做事的 agent 殼 | [Ch 4](./chapters/ch04_cli_agents/) |
| MCP | Model Context Protocol | 一個 server 寫一次、所有 agent 都能接 | [Ch 6](./chapters/ch06_mcp/) |
| Skill | Skill | 給 LLM 看的「規格書 + cheat sheet」 | [Ch 7](./chapters/ch07_skills_plugins/) |
| 漸進式揭露 | Progressive Disclosure | 只在需要時載入細節的 Skill 設計 pattern | [Ch 7 §3](./chapters/ch07_skills_plugins/#3-progressive-disclosure-skill-的核心設計-pattern) |
| 預算上限 | Budget Cap | 防止 agent 燒錢的硬上限 | [Ch 8](./chapters/ch08_cost_observability/) |
| 失控 | Runaway / Tool Loop | Agent 自己擴張 / 重複呼叫工具 | [Ch 8 §3](./chapters/ch08_cost_observability/#3-三個常見「燒錢失敗模式」) |
| 介入 | Intervention / Abort | 中止 agent 跑到一半 | [Ch 8 §4.3](./chapters/ch08_cost_observability/#43-強制中止-ctrlc--abort) |

## 外部權威詞典（不重複造輪）

- 🔗 [ai-dict.gh.miniasp.com](https://ai-dict.gh.miniasp.com/) — Matt Pocock AI Coding Dictionary 繁中版（保哥技術社群翻譯）
  - 7 sections: Models / Sessions+Context+Turns / Tools+Environments / Failure Modes / Handoffs / Memory+Guidance / Work Modes
  - **本書每章末「補充閱讀」會對應到 ai-dict 對應 section**
- 🔗 [WenyuChiou/awesome-agentic-ai-zh resources/glossary.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/glossary.md) — 30+ 詞，每個 30-80 字解釋

## 為什麼這頁這麼短？

因為**用詞穩定 + 跨章一致**比「我們也寫一本詞典」重要。AgentZ 的角色是 curriculum——把詞放在它出現的章節裡學，不是離開上下文查字典。
