# 名詞表

AgentZ 用詞 + 業界術語的繁中對照。每條 **4 欄**：專業介紹、白話解釋、應用範例、本書章節。

> 找不到的詞？[GitHub Issue](https://github.com/symbiosis11503/agent-z/issues) 告訴我們，補進來。

---

## 1. LLM 基礎

### 大型語言模型 / LLM (Large Language Model)
- **專業**：用 transformer 架構訓練的神經網路，目標是預測下一個 token 的條件機率分佈 $P(x_{t+1} | x_1, ..., x_t)$。參數量通常從數十億到上兆。
- **白話**：吃進文字、輸出最可能下一個字的機率機器。它不是「在思考」，是統計學意義上猜下一個字。
- **範例**：Claude / GPT-4 / Gemini / Llama 都是 LLM。當你問 ChatGPT「今天天氣」、它回答的本質是「人類在這種情境下會說什麼字最有可能」。
- **章節**：[Ch 1](./chapters/ch01_llm_basics/)

### Token / Token
- **專業**：LLM 的最小輸入單位，由 tokenizer 把字串切成的 sub-word 片段。中文約 1-2 字一個 token，英文約 4 字元一個。
- **白話**：LLM「看世界」的單位、也是收錢的單位。
- **範例**：「Hello world」= 3 token（`Hello`, ` world`, `!`）。「今天天氣真好」= 4-7 token。Anthropic Haiku 4.5 輸入 $0.80 / 百萬 token。
- **章節**：[Ch 1 §2](./chapters/ch01_llm_basics/#2-token-是什麼)

### 上下文視窗 / Context Window
- **專業**：LLM 一次推論能容納的最大 token 數。受 model 架構（attention pattern）跟 GPU 記憶體限制。
- **白話**：LLM 一次能讀的「最多多少字」。讀太多塞不下。
- **範例**：Claude 4.x 200K-1M token、GPT-4o 128K、Gemini 2.0 Flash 1M。200K token ≈ 一本中等小說。
- **章節**：[Ch 1 §3](./chapters/ch01_llm_basics/#3-context-window-llm-的-記憶-上限)

### 角色 / Role
- **專業**：API messages 陣列每則訊息的發話者標記：`system` / `user` / `assistant`（部分 model 多 `tool` / `function`）。
- **白話**：「這段話是誰講的？」系統 / 使用者 / LLM。
- **範例**：`[{role: "system", content: "你只回繁中"}, {role: "user", content: "Translate Hello"}, {role: "assistant", content: "你好"}]`。
- **章節**：[Ch 1 §4](./chapters/ch01_llm_basics/#4-role-system--user--assistant)

### 溫度 / Temperature
- **專業**：softmax 採樣機率分佈的溫度參數。溫度 0 = greedy（取最高機率）、溫度 > 1 = 越平坦（隨機）。
- **白話**：「LLM 答得有多隨興」的旋鈕。0 = 死板穩定、1 = 有創意。
- **範例**：寫合約 → 溫度 0；寫詩 → 溫度 0.8。agent 工具呼叫一定 0 或 0.1，要穩定。
- **章節**：[Ch 1 §5](./chapters/ch01_llm_basics/#5-temperature-隨機性旋鈕)

### 嵌入 / Embedding
- **專業**：把文字（or 圖 / 音）映射到固定維度的 dense vector（通常 384-3072 維），讓語意相近的東西在向量空間距離近。
- **白話**：把一段文字變成一串數字，讓電腦能算「兩段意思像不像」。
- **範例**：「貓」跟「狗」的 embedding 距離近、跟「火箭」的距離遠。RAG 全靠這個做 similarity search。
- **章節**：[Ch 13](./chapters/ch13_memory_rag/)

### 微調 / Fine-tuning
- **專業**：用 supervised / RL 訊號繼續訓練 base model 的部分或全部參數，讓它更適配特定 task / domain / 風格。
- **白話**：把現成 LLM 拿過來、餵它你自己的資料、讓它變成「你公司專用版」。
- **範例**：把 Llama-3 fine-tune 成法律 advisor、客服機器人、code reviewer。
- **章節**：[Ch 17](./chapters/ch17_builder_advanced/)

### 幻覺 / Hallucination
- **專業**：LLM 生成 plausible 但事實錯誤、無依據的內容。常見原因：訓練資料缺少、context 引導不足、temperature 高。
- **白話**：LLM 一本正經地胡說八道。
- **範例**：問「2026 年 5 月某某 paper 的作者」、它掰一個不存在的 paper 跟假作者，還給你假 DOI。Ch 16 §4 anti-hallucination 5 條規則就是治這個。
- **章節**：[Ch 16](./chapters/ch16_researcher/)

---

## 2. Prompt / Context 管理

### 提示 / Prompt
- **專業**：使用者 / 系統送給 LLM 的完整輸入文字（含 system / user / assistant 訊息 + tool 定義 + few-shot 範例）。
- **白話**：你跟 LLM 說的話。**不是 chat，是 specification**——你不寫清楚它就自己腦補。
- **範例**：「翻譯這段」=爛 prompt；「你是繁中翻譯助理。只翻譯不解釋。範例：Hello → 你好。請翻譯：Good morning」= 好 prompt。
- **章節**：[Ch 2](./chapters/ch02_prompt/)

### 系統提示 / System Prompt
- **專業**：放在 messages 陣列開頭的 `role: system` 訊息，定義 LLM 角色 / 約束 / 輸出格式。
- **白話**：給 LLM 的「使用說明書 + 性格設定」。每次對話開始它先讀。
- **範例**：`"你是繁中技術文件翻譯助理。只回繁中。不解釋技術名詞除非問你。輸出 markdown 格式。"`
- **章節**：[Ch 2 §2](./chapters/ch02_prompt/#2-system-prompt-的-4-個欄位)

### 少量範例 / Few-shot
- **專業**：在 prompt 中提供 1-N 個 input/output pair 示範，讓 LLM 從範例 in-context learn pattern。
- **白話**：給 LLM 看「我要的答案長這樣」的範本，比抽象描述有效 10x。
- **範例**：「分類情緒：『今天好開心』→ 正面 / 『下雨真煩』→ 負面 / 『等公車中』→ 中性 / 『加薪了！』→ ?」 LLM 看到範例知道輸出格式 + 標籤集合。
- **章節**：[Ch 2 §3](./chapters/ch02_prompt/#3-few-shot-vs-zero-shot)

### 思考鏈 / Chain-of-Thought (CoT)
- **專業**：透過 prompt 引導 LLM 在最終答案前先生成中間推理步驟。可顯式（`<thinking>`）或隱式（`Let's think step by step`）觸發。
- **白話**：要 LLM「先想再答」、想的過程印出來。算數 / 邏輯題效果顯著。
- **範例**：問「17 × 23」、加 "Let's think step by step" 前後答對率差 30%+。現代 reasoning model（o1 / R1 / Claude Sonnet）內建 CoT 不用你加。
- **章節**：[Ch 2 §4](./chapters/ch02_prompt/#4-chain-of-thought-cot)

### 結構化輸出 / Structured Output
- **專業**：透過 JSON mode / tool use schema / Pydantic AI 等機制，強制 LLM 輸出對齊指定 schema 的合法 JSON。
- **白話**：要 LLM 回答**只能是固定格式**，不能加廢話。下游程式好 parse。
- **範例**：要 LLM 翻譯回 `{"translated": "...", "confidence": 0.95}`、不要回「Sure, here's your translation: ...」。
- **章節**：[Ch 2 §5](./chapters/ch02_prompt/#5-結構化輸出要-json-就要對)

### 壓縮 / Compaction
- **專業**：長對話超過 context window 前，把舊 messages 摘要成短 summary 取代原文。trade off：壓縮失去細節 vs 不壓爆 context。
- **白話**：對話太長、把老的對話濃縮成「老闆說過喜歡咖啡，討論過 3 個方案」這種大綱。
- **範例**：Claude Code 內建 `/compact` 指令；自己寫 agent 在 messages.length > 20 時觸發 LLM 摘要 messages[:10]。
- **章節**：[Ch 13 §3](./chapters/ch13_memory_rag/#3-session-memory-累積--摘要)

### 提示快取 / Prompt Cache
- **專業**：在 messages / system / tools 上標 `cache_control: {type:"ephemeral"}`，相同 prefix 後續呼叫時 input cost 降至 1/10，cache TTL 1 小時（Anthropic）。
- **白話**：「同一段長 system prompt 不要每次都收滿費」。LLM 把它快取住、第二次起便宜 90%。
- **範例**：5K-token system prompt + 多輪對話：第一次寫入 1.25x cost、第二次起 0.1x cost。Ch 8 cost cap 配 cache 兩件事一起做。
- **章節**：[Ch 8 §4](./chapters/ch08_cost_observability/) + [速查卡](./cheatsheet#prompt-cache-省-90-cost)

---

## 3. Agent 機制

### 智能體 / Agent
- **專業**：LLM + 工具集 + 控制循環的系統。Agent 能根據目標自主決定下一步 action（call tool / 給回答 / 結束）。
- **白話**：會自己跑流程的 LLM。你給目標、它自己決定要查什麼 / 點什麼 / 做什麼步驟。
- **範例**：你說「幫我訂下週去東京的便宜機票」、agent 自己 search 機票網、比價、填表、回報。ChatGPT 只會建議你去哪查；agent 真的去查。
- **章節**：[Ch 3](./chapters/ch03_what_is_agent/)

### 工具呼叫 / Tool Use / Function Calling
- **專業**：LLM 在生成回應時，依 prompt 中提供的 tool schema，emit 一個 `tool_use` block（含 tool name + JSON input），由外部 agent harness 真實執行後把 result 塞回 messages，LLM 繼續推論。
- **白話**：LLM 不會真的點滑鼠、按按鈕。它寫「我想呼叫這個函式」的便條紙、外部程式幫它跑，把結果回去給它看。
- **範例**：你問「台北現在幾度」、LLM 回 `{"type":"tool_use","name":"get_weather","input":{"city":"Taipei"}}`、你的 agent 真的去打 weather API、把 26°C 回去、LLM 再回給你「台北 26°C」。
- **章節**：[Ch 3 §2](./chapters/ch03_what_is_agent/#2-tool-use-llm-怎麼呼叫工具)

### ReAct / ReAct (Reason + Act)
- **專業**：2022 年 Yao et al. 提出的 agent 循環模式。每一步 LLM 先 reason（用自然語言講「我下一步該做什麼」）再 act（call tool），observe 工具結果後再 reason 下一步。
- **白話**：agent 的「想一下 → 做 → 看結果 → 再想 → 再做」迴圈。是 2025 年多數 agent 的核心。
- **範例**：Claude Code / Codex / OpenCode 內部都是 ReAct 的變體 + 多 polish。
- **章節**：[Ch 3 §3](./chapters/ch03_what_is_agent/#3-react-reason--act-循環)

### 計畫先行 / Plan-and-Solve
- **專業**：把 agent 跑分兩階段——planner 先用 LLM 生出完整步驟、executor 再照 plan 一步步執行。
- **白話**：先列 to-do list、再照做。不是邊做邊想。
- **範例**：「研究 3 個 framework 寫比較表」——先 plan「1. 各自 google 2. 抓官網 3. 比較 4. 整合」、再執行。
- **章節**：[Ch 10 §3](./chapters/ch10_react_paradigms/#3-plan-and-solve)

### 反思 / Reflection (Reflexion)
- **專業**：agent 完成 task 後，self-critique 答案品質、不滿意就 redo。需要可驗證的 reward signal（test pass / 評分 / 比對）。
- **白話**：做完自己挑毛病、不滿意重做。多 LLM call 換高品質。
- **範例**：寫 code 後跑 test、test 失敗就根據 error message 改 code 再跑。
- **章節**：[Ch 10 §4](./chapters/ch10_react_paradigms/#4-reflection)

### 失控 / Runaway / Tool Loop
- **專業**：agent 因 reasoning bug 或 environment feedback 不穩，重複 call 同一個 tool 或無限擴張 scope，導致成本失控。
- **白話**：agent 跑著跑著瘋掉了：一直 retry / 一直改 / 一直跑 test，停不下來。
- **範例**：你說「修這個 bug」、它變「修 bug + 重構 module + 加 test + 寫 doc」——一個 task 燒 $20。Ch 8 §3 教 3 個 pattern 怎麼防。
- **章節**：[Ch 8 §3](./chapters/ch08_cost_observability/#3-三個常見-燒錢失敗模式)

### 停止原因 / stop_reason
- **專業**：Anthropic API response 的終止狀態欄位：`end_turn`（自然結束）/ `tool_use`（要 call tool）/ `max_tokens`（超 token limit）/ `stop_sequence`（撞 stop_sequences）/ `pause_turn`（長 server-tool 暫停）/ `refusal`（safety reject）。
- **白話**：LLM 為什麼停下來？分手對方說「我講完了」/「該你了去 call tool」/「字數爆了」/「碰到禁字」。寫 agent loop 必須對每種反應。
- **範例**：`if resp.stop_reason == "tool_use": run tool 然後 append tool_result; elif "end_turn": done; elif "max_tokens": 提示 user / 縮 prompt 重試`。
- **章節**：[Ch 9](./chapters/ch09_function_calling/) + [速查卡](./cheatsheet#anthropic-sdk-速查)

### 電腦使用 / Computer Use
- **專業**：2024-10 Anthropic 推出的 Claude 能力。Claude 透過 screenshot tool + mouse/keyboard tool 操作真實桌面 GUI（不是 API）。包在 `computer_20241022` tool type。
- **白話**：讓 Claude 真的看你螢幕、移動滑鼠、打字。可以填網頁表單、跑沒 API 的軟體。
- **範例**：Claude in Chrome / claude-in-chrome MCP / Anthropic computer-use demo container。要 sandbox 跑（不然它真的會點你的 email）。**Ch 18 Maker 路線會用到**。
- **章節**：[Ch 18](./chapters/ch18_maker_educator/)

### 子代理 / Subagent
- **專業**：透過 Task / Agent tool 由主 agent 啟動的隔離子 conversation。子 agent 有自己 context / system prompt / tool 集，跑完只回傳結果給主 agent，原始 trace 不污染主 context。
- **白話**：「派下去做的小弟」。主 agent 把「搜尋 codebase 30 個檔」這種大任務外包給 subagent、自己保持乾淨 context。
- **範例**：Claude Code 的 Task tool / Explore agent / Plan agent；自己寫 agent 用 sub-LLM 處理子任務。**節省 context 是 multi-agent 的入門用法**。
- **章節**：[Ch 14](./chapters/ch14_multi_agent/)

### 深度研究 / Deep Research
- **專業**：長 horizon agent，跨 10-50 個 web search / paper read / cross-reference 後產出研究報告。需要 cost cap + DOI 驗證 + reflection critique 防幻覺。
- **白話**：「丟一個問題、讓 agent 跑半小時、給我一份報告」的研究模式。ChatGPT / Claude / Gemini 都有 Deep Research mode。
- **範例**：OpenAI Deep Research、Gemini Deep Research、Claude Research、ChatGPT Atlas Agentic Search。AgentZ Ch 16 教你自己寫一個。
- **章節**：[Ch 16](./chapters/ch16_researcher/)

### 後台 / 排程代理 / Headless / Scheduled Agent
- **專業**：無人盯著、由 cron / launchd / systemd timer 觸發的 agent，跑完寫 log / 發通知。架構必含 cost cap、retry policy、failure alert。
- **白話**：「不開電腦也會自己跑的 agent」。例：每天早上 6:00 抓新聞重點寄你 mailbox。
- **範例**：morning briefing agent（Ch 18）、夜跑 deep research、定時 codebase audit。AFK 執行的具體實作形式。
- **章節**：[Ch 18 §3](./chapters/ch18_maker_educator/) + [Ch 8](./chapters/ch08_cost_observability/)

---

## 4. CLI Agent / Claude Code 生態系

### 命令列代理 / CLI Agent
- **專業**：以 Terminal / shell 為介面的 agent harness，內建 file read/write / Bash / Edit / Glob / Grep 等工具，啟動會載入 CLAUDE.md 等 config。
- **白話**：在你電腦 Terminal 跑、會做事的 agent 殼。打字跟它說「修這個 bug」、它真的去改你的程式碼。
- **範例**：Claude Code（`claude` 指令）、OpenAI Codex CLI、OpenCode、Gemini CLI 是 2026 Q1 四大主流。
- **章節**：[Ch 4](./chapters/ch04_cli_agents/)

### 模型上下文協議 / MCP (Model Context Protocol)
- **專業**：2024-11 Anthropic 提出的開放標準。透過 JSON-RPC（stdio / SSE 傳輸）讓 agent client 跟外部 server 對話，server 暴露 Tools / Resources / Prompts 三類能力。
- **白話**：「agent ↔ 工具」的共通語言。寫一次 MCP server，Claude Code / Codex / OpenCode 全都能接，不用為每家 agent 各寫一次。
- **範例**：裝 `notion-mcp-server` → 你的 Claude Code 立刻能讀寫 Notion；裝 `github-mcp-server` → 能 review PR / 開 issue。62-entry catalog 在 WenyuChiou repo。
- **章節**：[Ch 6](./chapters/ch06_mcp/)

### 技能 / Skill
- **專業**：給 LLM 的 markdown 文件（含 frontmatter description）+ 可選 reference files + 可選 scripts。LLM 看到觸發條件自動載入 SKILL.md 主體，按需展開 reference。
- **白話**：給 LLM 看的「規格書 / SOP / cheat sheet」。MCP 是「函式庫」，Skill 是「教戰手冊」。
- **範例**：寫一個 `email-customer` skill，含「寫客戶信的 5 步驟 SOP」+ tone-guide.md reference。下次你說「幫客戶 X 寫詢價信」、Claude Code 自動載入 skill 按 SOP 走。
- **章節**：[Ch 7](./chapters/ch07_skills_plugins/)

### 漸進式揭露 / Progressive Disclosure
- **專業**：Skill 設計 pattern。Level 1 frontmatter always-loaded（10 行）、Level 2 SKILL.md body 觸發後載入（< 500 行）、Level 3 reference/ subdir LLM 主動 fetch（細節 SOP / scripts）。
- **白話**：別把所有資料塞一份大文件給 LLM 看（耗 token + 失焦）。先給目錄、要用到細節再讀。
- **範例**：`email-customer/SKILL.md` 只列 5 步驟、tone 風格詳細寫在 `reference/tone-guide.md`、客戶寫信範本在 `reference/examples.md` — LLM 需要時才讀。
- **章節**：[Ch 7 §3](./chapters/ch07_skills_plugins/#3-progressive-disclosure-skill-的核心設計-pattern)

### 斜線指令 / Slash Command
- **專業**：Claude Code 中 `/<name>` 觸發的預存 prompt，存在 `.claude/commands/<name>.md`（專案級）或 `~/.claude/commands/`（全域）。可帶參數。
- **白話**：把常用的長 prompt 存檔、打 `/<名字>` 就觸發。省每次重打 + 確保格式一致。
- **範例**：`/commit` → 看 staged changes 寫 commit message 等你 confirm；`/translate-zh <text>` → 帶參數翻譯。
- **章節**：[Ch 5 §3](./chapters/ch05_cli_workflow/#3-slash-command-自製)

### 鉤子 / Hook
- **專業**：Claude Code settings.json 的 `hooks` 區塊，定義 PreToolUse / PostToolUse 等事件觸發時跑的 shell 指令。可攔截 / 修改 / 紀錄工具行為。
- **白話**：「agent 動之前 / 之後幫我跑這個」的自動化規則。
- **範例**：PostToolUse 配 `Write|Edit` → 自動 `npm run lint --fix`；PreToolUse 配 `Bash` → 看到 `rm -rf` 直接擋。
- **章節**：[Ch 5 §6](./chapters/ch05_cli_workflow/#6-hook-在工具呼叫前後跑你的-code)

### 插件 / Plugin
- **專業**：Claude Code 的擴充封裝單位。一個 plugin 可以同時帶 commands / agents / hooks / MCP server / skills，透過 marketplace.json 散發。比起單純 Skill / MCP，是更完整的「功能套件」。
- **白話**：「一包裝好的功能」。裝一個 plugin 等於同時加幾個 slash command、subagent、hook、MCP server。
- **範例**：`claude-config plugin install @anthropic/example-plugin`；公司內部 marketplace 散發部門通用工具集。
- **章節**：[Ch 7](./chapters/ch07_skills_plugins/)

### Agent SDK / Claude Agent SDK
- **專業**：Anthropic 官方的 Python / TypeScript SDK（npm `@anthropic-ai/claude-agent-sdk`），把 Claude Code 內部 agent loop 抽出來給開發者直接用：載 system prompt / 工具集 / hooks / subagent 等。
- **白話**：「把 Claude Code 變成你 app 的一部分」的 SDK。不只 API call，是完整 agent loop。
- **範例**：用 Agent SDK 寫一個只跑你公司 SOP 的內部 agent、嵌入 Slack bot 或 web app。
- **章節**：[Ch 12](./chapters/ch12_mini_framework/) + [Ch 18](./chapters/ch18_maker_educator/)

### MCP 範圍 / MCP Scope
- **專業**：Claude Code 註冊 MCP server 的層級，影響可見性：`user` 範圍寫到 `~/.config/claude/claude.json`（全域）/ `project` 範圍寫到 `.mcp.json`（per-repo）/ `local` 範圍寫到 `.claude/claude.json`（per-repo 隱私）。
- **白話**：「這個 MCP server 哪些 session 看得到」。個人工具放 user；公司 repo 共用放 project；不想 git commit 的私人 key 放 local。
- **範例**：`claude mcp add notion-mcp ... --scope user` vs `--scope project`；專案內 mcp.json 進 git，個人 key 用 user-scope。
- **章節**：[Ch 6](./chapters/ch06_mcp/)

---

## 5. Vibe Coding / 軟體開發新工作方式

> 2025-2026 工作流變遷：從「自己每行寫」到「跟 AI 對話讓它寫」。

### 氛圍編程 / Vibe Coding
- **專業**：Andrej Karpathy 2025 提出。開發者不直接編輯 code、僅透過對話 / 高層指令操控 AI agent；自己只 review diff / 改 prompt / 偶爾 nudge 方向；接受 LLM 偶爾「為什麼這樣寫」自己不完全懂。
- **白話**：「我給氛圍、AI 寫 code」。極限版：你連 syntax 都不太管、跟 AI 講「我想要這個感覺」、看結果不對就再 vibe 一次。
- **範例**：用 Cursor / Claude Code 開發網站 demo——你說「加一個 dark mode toggle 在右上角」、AI 自己寫 CSS + JS + 測試、你只看畫面對不對。**這本書 5/11 全 session 是 vibe coding 真實案例**（boss vibe、CC1 code、~1500 commit / day 量級）。
- **適用**：原型 / demo / 短期專案 / 沒人 review 也能 ship 的場景。**不適用**：核心 production system、安全敏感、需要長期維護。

### AI 結對程式設計 / AI Pair Programming
- **專業**：傳統 pair programming 一個 driver 一個 navigator；AI 版是 AI 當 navigator（給建議 / 抓 bug / catch 問題），你還是 driver 自己打字。
- **白話**：你寫一行、AI 在旁邊看、提示你「下一行可能要這樣」或「這邊有 bug」。
- **範例**：GitHub Copilot inline 自動完成、Cursor Tab。**vs Vibe Coding 的差別**：pair 你還在打字、vibe 你只下指令。
- **章節**：跨 Ch 4-5 提到

### 程式碼編輯代理 / Code-editing Agent
- **專業**：能自主多輪編輯 codebase 的 agent，不是 chat suggestion。會 plan + read multi-file + edit + run test + iterate。
- **白話**：「自己改 codebase 的 AI」——你說「修 bug #42」、它真的 git checkout / 改檔案 / commit。
- **範例**：Claude Code / Aider / OpenDevin / Cline。**vs CLI Agent**：CLI 是介面類別、code-editing 是工作類別，多數 CLI Agent 都是 code-editing agent。
- **章節**：[Ch 4](./chapters/ch04_cli_agents/)

### 規格驅動開發 / SDD (Spec-Driven Development)
- **專業**：先寫詳細 spec（input / output / 邊界條件 / 失敗模式）→ 給 agent 從 spec 生 code + test → 跑 test → 不對 reflection 改。spec 比 code 是 source of truth。
- **白話**：「先把要做什麼寫清楚、再讓 AI 做」。AI 容易在模糊 spec 上犯錯，spec 寫清楚錯就少。
- **範例**：Symbiosis SOP v0.1 的 17 步鏈條核心就是 SDD：Intake → Discovery → Spec → Truth Boundary → SDD → ...
- **章節**：[Ch 5](./chapters/ch05_cli_workflow/) + Helix V3 case study Ch 15

### 測試驅動開發 / TDD (Test-Driven Development)
- **專業**：紅綠重構 cycle：先寫 failing test（紅）→ 寫最少 code 讓 test 過（綠）→ refactor。
- **白話**：先寫「怎樣才算對」（test）、再寫「要怎麼做才對」（implementation）。
- **範例**：給 agent「修這個 bug」前先 `pytest` 看哪個 test 紅、再讓 agent 寫 code 讓那個 test 變綠。配 Hook 自動跑 test 效率高。
- **章節**：跨 Ch 12-15

### AFK 執行 / AFK (Away-From-Keyboard) Execution
- **專業**：agent 在沒有人盯著的時間執行任務（夜跑 / 後台 cron / 長時間 deep research）。需 cost cap + audit + graceful failure。
- **白話**：「你不在電腦前的時候、agent 自己做事」。早上回來看結果就好。
- **範例**：Ch 18 morning briefing agent；夜跑 deep research；長時間 codebase migration。
- **章節**：[Ch 8](./chapters/ch08_cost_observability/) + [Ch 18](./chapters/ch18_maker_educator/)

### 確認暫停 / Acceptance Gating
- **專業**：agent 在執行 high-impact action（寫檔 / push / 寄信 / 刪資料）前停下、要 human 按 Enter / 簽核才繼續。
- **白話**：「agent 動之前停下來等你說 OK」。預設保守、進階用戶可關。
- **範例**：Claude Code 預設 permission mode = ask。`/permission accept-all` 切全自動但要小心。
- **章節**：[Ch 4 §5](./chapters/ch04_cli_agents/#5-第一個真實-task)

### 委派 / Delegation
- **專業**：主 agent 把獨立 subtask 丟給 sub-agent / specialist agent 處理，結果回主 agent 不污染 context。可並行。
- **白話**：agent 也能「外包」——大事自己做、小事交給專門子 agent。
- **範例**：主 agent 收到「重構這個 module」、把「先掃全 codebase 找所有 import」delegate 給 search sub-agent。
- **章節**：[Ch 14](./chapters/ch14_multi_agent/)

---

## 6. Memory / RAG

### 會話記憶 / Session Memory
- **專業**：一次 agent / chat session 內累積的 messages 陣列。LLM 沒有跨 call 持久記憶，session memory 是 client 自己維護。
- **白話**：「這次對話內 agent 記得你說過的話」。對話結束就忘。
- **範例**：你在 ChatGPT 一個對話內說「我叫 Wei、住台北」、它記得。開新對話就忘。
- **章節**：[Ch 13 §3](./chapters/ch13_memory_rag/)

### 長期記憶 / Long-term Memory
- **專業**：跨 session persistent 的 user / world facts。實作可結構化（SQL key-value）或向量（過去對話 embed 進 vector store）。
- **白話**：「跨多次對話 agent 都記得的事」。
- **範例**：「使用者是 Wei、偏好繁中、住台北、用 Mac」這種事實寫進 SQLite。下次 agent 啟動 load 進 system prompt。
- **章節**：[Ch 13 §4](./chapters/ch13_memory_rag/#4-long-term-memory-結構化-vs-向量)

### 檢索增強生成 / RAG (Retrieval-Augmented Generation)
- **專業**：query → embedding → vector DB similarity search top-K chunks → 把 chunks 拼進 prompt → LLM 根據 chunks 回答。
- **白話**：LLM 不知道你公司的事——RAG 把你公司文件存起來、問問題時撈相關片段給 LLM 看。
- **範例**：你公司 SOP / 產品文件 / FAQ 切 chunk 進 Chroma；員工問「請假怎麼申請」、agent 撈 HR 政策 chunk + 回答。
- **章節**：[Ch 13 §5](./chapters/ch13_memory_rag/#5-rag-retrieval-augmented-generation)

### 上下文檢索 / Contextual Retrieval
- **專業**：Anthropic 2024 提出。embed 前先用 LLM 給每個 chunk 加 50-100 字「位置 + 主題」context，再 embed。提升 retrieval recall 35-49%。
- **白話**：「這 chunk 在文件中是哪段、講什麼」先寫清楚再存 vector DB。
- **範例**：原文 chunk「需診斷書。」加 context「假期政策第二條病假規定」→「[CTX: 假期政策第二條病假規定] 需診斷書。」再 embed。問「請病假要什麼」會 retrieve 到。
- **章節**：[Ch 13 §6](./chapters/ch13_memory_rag/#6-contextual-retrieval--anthropic-2024-的優化)

---

## 7. Multi-agent / Orchestration

### 多智能體 / Multi-agent
- **專業**：多個 agent 透過 shared state / handoff / blackboard 等機制協作完成單一任務。每 agent 可有不同 model / system prompt / tool set / 權限範圍。
- **白話**：多個專業 agent 分工合作、不是一個 agent 包山包海。
- **範例**：研究 agent 查資料 → 寫作 agent 寫 draft → review agent 改錯字 → 三人接力完成「寫一篇 paper 比較」。
- **章節**：[Ch 14](./chapters/ch14_multi_agent/)

### 流水線 / Pipeline
- **專業**：固定順序 A → B → C 的 multi-agent 編排，每階段輸出當下階段輸入，無 dynamic routing。
- **白話**：「先做 X、再做 Y、最後 Z」——固定流程，不會中途換方向。
- **範例**：research → write → review 三 agent 流水線。每段失敗整條失敗。
- **章節**：[Ch 14 §2.1](./chapters/ch14_multi_agent/#21-pipeline-流水線)

### 主管模式 / Supervisor
- **專業**：一個 supervisor agent 看任務 + 當前 state、回 JSON 決定派給哪個 worker、回收 worker 結果再決定下一步。
- **白話**：「老闆派工模式」——主管看情況決定誰做什麼。
- **範例**：HR agent + Sales agent + IT agent 三個 worker；supervisor 看到「客戶想知道 SLA」派 sales、「員工請假」派 HR。
- **章節**：[Ch 14 §2.2](./chapters/ch14_multi_agent/#22-supervisor-主管--部屬)

### 交接 / Handoff
- **專業**：agent 認為「這超出我能力」時、把任務 + context 轉給 specialist agent。最乾淨實作：把 handoff 當特殊 tool。
- **白話**：「這事我不會、轉給專家」。
- **範例**：通用 agent 對話到一半發現使用者問法律問題、call `handoff_to_legal_specialist(context)` 把對話交給法律 agent。
- **章節**：[Ch 14 §3](./chapters/ch14_multi_agent/#3-handoff-機制)

---

## 8. Production Governance

### 預算上限 / Budget Cap
- **專業**：在 agent run / day / user / org 層級設定累積 token spend 上限。超過 fail-closed（raise exception / stop run）。
- **白話**：「最多花 X 元」的硬規定。超過就停。
- **範例**：V3 三層 cap：`costBudgetUSDPerRun = 0.5` / `costBudgetUSDPerDay = 10`。Anthropic console 也有月帳號 cap 可設。
- **章節**：[Ch 8 §4.1](./chapters/ch08_cost_observability/#41-設-budget-cap)

### 介入 / Intervention / Abort
- **專業**：external signal 中止 in-progress agent run。實作：abort registry 標記 run_id、agent loop 在每個 LLM call / tool call 之間 / SSE 之間檢查 flag、撞到 raise / 結束。
- **白話**：agent 跑到一半你按「停」、它馬上停下。
- **範例**：Claude Code Ctrl+C、V3 POST `/runs/{id}/abort?reason=...`、UI「介入」chip。
- **章節**：[Ch 8 §4.3](./chapters/ch08_cost_observability/#43-強制中止-ctrlc--abort)

### 稽核 / Audit
- **專業**：每個 agent action（LLM call / tool call / state transition / cost event / abort）寫進 append-only event log。每筆 `audit_event_id` + ts + category + run_id + payload。
- **白話**：「agent 做了什麼、何時做的」全紀錄。出問題能查。
- **範例**：V3 PostgreSQL `audit_events` JSONB table、`category` enum (`llm_call` / `tool_call` / `run_aborted` / `cost_exceeded` / ...)。
- **章節**：[Ch 15 §3.1](./chapters/ch15_deploy_audit_replay/#31-audit-log)

### 回放 / Replay
- **專業**：紀錄每次 LLM call / tool call 完整 input + output + cost，事後可重現整個 run 或從某 step 分叉重跑（fork replay）。
- **白話**：「agent 那次跑的所有細節錄影下來、能倒帶看」。
- **範例**：V3 `replay_records` 表存每 step 的 input/output JSONB、cost_estimate / cost_observed。UI 列 trace、點某 step 看 raw、或「從這 step 改 prompt 再跑」。
- **章節**：[Ch 15 §3.2](./chapters/ch15_deploy_audit_replay/#32-replay)

### 護欄 / Guardrails
- **專業**：限制 agent 行為的硬約束。實作層次：filesystem path allow-list / MCP server scope / Hook PreToolUse blocking / model-level safety classifier。
- **白話**：「agent 不准做這些事」的圍欄。
- **範例**：filesystem MCP 只給 `/tmp/agentz` 路徑、Hook 擋住 `rm -rf` 指令、production secret 從不進 prompt。
- **章節**：[Ch 6 §8](./chapters/ch06_mcp/#8-mcp-server-的安全性)

---

## 9. 模型訓練 / Agentic-RL

### 監督式微調 / SFT (Supervised Fine-Tuning)
- **專業**：用人工標註的 `(prompt, ideal_output)` pair 跑 cross-entropy loss、更新 model 參數（全參數 / LoRA / QLoRA）。
- **白話**：「給範本、讓 model 學著像範本回答」。
- **範例**：1K 筆 function-calling 範例 fine-tune Llama-3-8B，得到 BFCL 比 base model 高 10% 的小 model。
- **章節**：[Ch 17 §2](./chapters/ch17_builder_advanced/)

### 群體相對策略優化 / GRPO (Group Relative Policy Optimization)
- **專業**：對同一 prompt sample N 個 output（N=8 常見），給每個算 reward，計算 group_mean reward，每個 output advantage = reward - group_mean，policy gradient 更新。不用 reference model。
- **白話**：「同一題出 8 個版本、看哪個對得分高、學那個方向」。
- **範例**：DeepSeek-R1 用 GRPO + 純 RL 跑出 OpenAI o1 水平的 reasoning model（沒 SFT 暖身、671B model）。
- **章節**：[Ch 17 §5](./chapters/ch17_builder_advanced/#5-grpo-概念)

### 智能體強化學習 / Agentic-RL
- **專業**：用 RL 訓 agent 跑多步 task。Reward 通常 sparse（任務完成 = 1、其他 = 0）、需 trajectory rollout + advantage estimation + policy update。
- **白話**：給 agent「成功就好、過程自由」的訓練——它自己摸索哪些 tool sequence 有效。
- **範例**：訓練「訂機票 agent」、reward 是「最後是否真的訂到 + 票多便宜」。模型自己摸出「先比價再訂」的策略。
- **章節**：[Ch 17](./chapters/ch17_builder_advanced/)

---

## 10. 台灣 AI / 主權方案

### TAIDE / TAIDE (Trustworthy AI Dialogue Engine)
- **專業**：國科會主導、中研院 + 台大 + 清大 + 交大 + 成大等學界合作開發的本土繁中 LLM。HuggingFace 開放下載 model weights，目前最新 Gemma-3-TAIDE-12b-Chat-2602 (12B params, 2025-02 發布)。
- **白話**：「台灣自己訓的繁中 LLM」。免費下載，自己架。
- **範例**：本地用 Ollama 跑 `ollama pull taide`（社群有 unofficial mirror）或從 HuggingFace 直接 load。配 vLLM 起 OpenAI-compat server、AgentZ / V3 都能接。
- **應用 AgentZ**：M3 Ultra 192GB + Ollama + TAIDE-12b 是「全主權」AgentZ 方案——0 雲端依賴。
- **沒有雲端 API**：要自架。HuggingFace Inference Endpoints 可付費租 GPU 跑。

### 國家主權 AI / Sovereign AI
- **專業**：國家 / 組織能自主控制 base model 訓練、推論硬體、資料管道、policy 規則的 AI 體系。對應 supply-chain risk 跟資料主權。
- **白話**：「不依賴美國雲端 / 中國雲端、自己能 train 跟 serve」的 AI。
- **範例**：TAIDE（台灣）、TII Falcon（UAE）、Mistral（法國）、DeepSeek（中國）、Bharat GPT（印度）都屬此類。
- **章節**：跨 Ch 1 + Ch 17

### 本地推論 / Local Inference
- **專業**：model + inference engine 跑在你掌控的硬體（個人機器 / 自己機房）、不經第三方雲。
- **白話**：「LLM 在我電腦跑、沒網路也能用、資料不出我手」。
- **範例**：Ollama (Mac/Linux 一行裝)、vLLM (GPU server)、MLX (Apple Silicon 加速)、llama.cpp (CPU 也能跑、量化 model)。
- **章節**：[Ch 1 §6 + Ch 17](./chapters/ch01_llm_basics/)

---

## 11. 常被混淆的 pair 對比

學習者最常搞混的 7 組對比。**「兩個都是 X，但...」** 一句話切清楚。

### MCP vs Skill
- **MCP** = agent ↔ 外部「函式庫 / API」的共通 protocol（執行能力）
- **Skill** = 給 LLM 看的「教戰手冊 / SOP」（指引 LLM 怎麼做）
- 一句話：**MCP 給工具、Skill 給說明書**。同一個任務可以兩個都用——MCP 提供「寄信」function、Skill 告訴 LLM「寄信前 5 步檢查」。

### Tool Use vs Function Calling
- **同一個東西的兩個名字**。Anthropic 文件用「tool use」、OpenAI 早期叫「function calling」、現在統一回「tools」。
- API 層面差異：Anthropic `tool_use` block / OpenAI `tool_calls` array — schema 不同但概念同。

### Agent vs Workflow
- **Workflow** = 你預先寫死的 step sequence（A → B → C），無分支決策
- **Agent** = LLM 自己決定下一步（A → ? → ?），自主路由
- 一句話：**Workflow 是火車軌道、Agent 是 GPS 導航**。Workflow 可預測但不靈活；Agent 靈活但要 cost cap / audit 護欄。

### ReAct vs Plan-and-Solve
- **ReAct** = 邊想邊做（每步 reason → act → observe → reason...），動態反應 environment
- **Plan-and-Solve** = 先想完 plan 再 execute（planner 列 5 步、executor 照跑）
- 哪個好？**短任務 / environment 變動大 → ReAct；步驟清楚 / 可預測 → Plan-and-Solve**。實務常混（Plan 主導 + 每步 ReAct 微調）。

### Fine-tuning vs RAG
- **Fine-tuning** = 改模型權重（讓 LLM「內化」某 domain）；成本高、需要 GPU / 訓練資料
- **RAG** = 不改模型，每次推論前撈相關資料塞 context（讓 LLM「查資料庫」）
- 哪個好？**事實 / 知識頻繁更新 → RAG；風格 / tone / 特定格式輸出 → Fine-tuning**。多數情境 RAG 先試（便宜 100x），不夠才 fine-tune。

### Subagent vs Multi-agent
- **Subagent** = 主 agent 派下去做子任務的隔離 agent（context 不共享，只回結果）
- **Multi-agent** = 多個 agent 各自有角色 / 工具集，協作完成任務（context 部分共享或 handoff）
- 一句話：**Subagent 是外包工讀生、Multi-agent 是團隊**。Subagent 是 Multi-agent 的最簡形式。

### CLI Agent vs Code-editing Agent
- **CLI Agent** = 「介面類別」（terminal 跑、shell-driven 的 agent）
- **Code-editing Agent** = 「工作類別」（會自主多輪改 codebase 的 agent）
- 多數 CLI Agent（Claude Code / Codex / OpenCode）都是 code-editing agent；但 code-editing 不一定是 CLI（Cursor / Cline 是 IDE-based）。

---

## 12. 外部權威詞典（不重複造輪）

- 🔗 **[ai-dict.gh.miniasp.com](https://ai-dict.gh.miniasp.com/)** — Matt Pocock AI Coding Dictionary 繁中（保哥技術社群翻譯）。7 sections: Models / Sessions+Context / Tools+Environments / Failure Modes / Handoffs / Memory+Guidance / Work Modes。本書每章末「補充閱讀」會對應到 ai-dict 對應 section。
- 🔗 **[WenyuChiou/awesome-agentic-ai-zh resources/glossary.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/glossary.md)** — 30+ 詞，每個 30-80 字解釋。
- 🔗 **[Anthropic Glossary](https://docs.anthropic.com/en/docs/about-claude/glossary)** — 官方英文 glossary，跟本書名詞 1-1 對齊。

## 為什麼這頁長這樣？

- **4-field 結構**——專業介紹（技術細節）/ 白話解釋（外行也懂）/ 應用範例（具體場景）/ 章節（深入）
- **跨章一致**——詞在哪一章 first introduced、其他章節用同樣詞
- **持續長**——你發現該收的詞[發 Issue](https://github.com/symbiosis11503/agent-z/issues) 給我們

---

> 「Don't build smarter LLMs—build smarter integrations.」  
> —AgentZ 默認哲學
