# Security Policy

AgentZ 是 AI Agent 教學內容專案（**非生產服務**）。但我們很在意「教材本身」與「starter code 範例」的安全性，因為錯誤的範例可能讓讀者誤學成壞 pattern。

## 哪些算「安全議題」

- 教程裡示範了**不安全的範例**（例：把 API key 寫進 git / 對 user input 不做 sanitize / SQL injection 容易踩到的寫法）
- 範例 code **能造成讀者本機危害**（例：執行任意 shell / 對 `/` 做 `rm -rf` 沒 guard / 下載第三方 binary 不驗證 sha256）
- 範例引用的**外部連結指到惡意網站**（例：fake API gateway / typosquat package）
- 章節推薦了**已知有漏洞的第三方 package**（例：CVE 已公告但我們沒更新）
- 教程**洩漏其他人的個資 / token / 任何 secrets**（不論來源）

## 怎麼回報

- 公開回報（不會立即造成損害）：開 [Issue](https://github.com/symbiosis11503/agent-z/issues) 加 `security` label
- 敏感回報（私下優先）：email **symbiosis11503@gmail.com** — title 加 `[Security]` prefix

**承諾**：
- 5 個工作天內回覆
- 確認後 14 天內修復（嚴重案件加速）
- 經回報者同意，會在 [CHANGELOG.md](./CHANGELOG.md) 致謝

## 哪些**不算**安全議題（請走別的管道）

- 教程內容寫得不夠詳細 → [Issue 內容建議](https://github.com/symbiosis11503/agent-z/issues/new?template=content_request.md)
- starter code 跑不起來 → [Issue bug](https://github.com/symbiosis11503/agent-z/issues/new?template=bug.md)
- 你想討論 agent / LLM 的安全議題本身（不是教程內的 bug） → [Discussions](https://github.com/symbiosis11503/agent-z/discussions)
- 第三方 service（Anthropic / OpenAI / GitHub）的安全議題 → 該 service 自己的 security 流程

## 我們**不會**做的事

- AgentZ 沒接受外部捐款或 bug bounty 經費
- 不保證教程在所有情境下都「最佳實作」，只保證**不教錯方向**
- 不主動掃描 `starter-code/` 的所有 dependency CVE（這是教學範例不是生產 lib）。但你回報我們會處理

---

維護：[Symbiosis (SBS)](https://github.com/symbiosis11503) — 也參考 [Code of Conduct](./CODE_OF_CONDUCT.md)
