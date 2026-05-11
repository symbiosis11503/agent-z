---
title: Ch 0 — 把工具裝好
description: 從 Terminal 開起、裝 Python / git、申請 LLM API key、設環境變數、跑第一支 hello.py。10-15 分鐘真零基礎 setup。
---

# Ch 0 — 把工具裝好

> **30-45 分鐘**。本章結束你會跑出你的第一個「LLM Hello-World」（你打字 → LLM 回你 → 在 Terminal 看到回答）。
>
> 適合：完全沒打開過 Terminal、沒裝過 Python、沒用過 git、沒申請過 API key 的人。
>
> 不適合：已經會以上四件事且跑過 `import anthropic` 一次的人——直接跳 [Ch 1](../ch01_llm_basics/)。

---

## 0. 你現在的位置自我評估

讀 Ch-1 動手練習 -1.1 你寫下的 3 個答案，對照下表：

| 你的答案 | 從哪一節開始 |
|---|---|
| 「不會 code、沒用過 Terminal」 | 從 §1 開始（全章） |
| 「會一點 Python，但沒申請過 API key」 | 跳 §4（API key 申請） |
| 「會 Python 跟 git，沒接過 LLM API」 | 跳 §6（第一個 LLM Hello-World） |
| 「以上都會了」 | 跳 [Ch 1](../ch01_llm_basics/) |

---

## 1. 打開 Terminal（5 分鐘）

**Terminal** 是一個文字介面，讓你打指令叫電腦做事。你會在這本書裡常常用到。

### macOS
- 按 `Cmd + Space` → 輸入 `terminal` → Enter
- 出現黑底白字（或白底黑字）的視窗就是 Terminal

### Windows
- 按 `Win + X` → 選 **Windows Terminal**（Windows 11）或 **PowerShell**（Windows 10）
- 如果沒有 Windows Terminal，先去 Microsoft Store 搜尋安裝

### Linux
- 大概不用我教

### 試一下這個指令

打 `echo Hello` 然後按 Enter：

```
$ echo Hello
Hello
```

如果看到第二行印出 `Hello`，恭喜，Terminal 通了。

> 💡 **指令前面那個 `$` 是提示符號**，不用打。本書凡是 `$` 開頭的就是 Terminal 指令。

---

## 2. 裝 Python（10 分鐘）

我們會用 Python 寫 agent。**Python 3.10 或更新**的版本就行。

### macOS（推薦用 uv）

`uv` 是一個極快的 Python 安裝管理器，2024 年起變主流。

```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
$ source ~/.zshrc  # 或 ~/.bashrc，看你 shell
$ uv python install 3.12
$ uv python --version
```

如果不想用 uv，也可以直接：
```bash
$ brew install python@3.12
```

### Windows

到 https://www.python.org/downloads/ 下載 Python 3.12 installer，**安裝時記得勾「Add Python to PATH」**。

驗證：
```
> python --version
Python 3.12.x
```

### Linux
```bash
$ sudo apt install python3.12 python3.12-venv
```

---

## 3. 裝 git（5 分鐘）

`git` 是版本管理工具，agent 開發離不開它。

### macOS

```bash
$ git --version  # 多數 Mac 已內建
```

如果沒有：
```bash
$ xcode-select --install
```

### Windows

到 https://git-scm.com/download/win 下載 installer，全部 default 安裝。

驗證：
```bash
$ git --version
git version 2.x.x
```

### 第一次設定（必做）

```bash
$ git config --global user.name "Your Name"
$ git config --global user.email "you@example.com"
```

> 💡 那個 email 會出現在你之後 push 上 GitHub 的 commit，**不要用工作或隱私 email**，最好申請一個專用的 dev email。

---

## 4. 申請 API key（10-15 分鐘）

我們要用真的 LLM API 來練習。你需要至少**一家**的 API key。本書範例會用 Anthropic（Claude），但 OpenAI（GPT）也能 follow，後面章節會教其他家（Gemini / Groq / OpenRouter）。

> 💡 **想看完整 11 家 LLM 對照（含免費層 / 怎麼選 / curl 範例 / 費用）**？翻 [LLM / API 申請指南](https://symbiosis11503.github.io/agent-z/llm-providers)（分 3 分類頁面：[商業](https://symbiosis11503.github.io/agent-z/llm-providers/commercial) / [開源聚合](https://symbiosis11503.github.io/agent-z/llm-providers/opensource-aggregator) / [本地主權](https://symbiosis11503.github.io/agent-z/llm-providers/local-sovereign)）。

### 我推薦：Anthropic Claude（5 美金免費額度）

1. 去 https://console.anthropic.com/
2. 註冊帳號（Google / 電子郵件都行）
3. 進到 **API Keys** 頁面
4. 點 **Create Key** → 命名（例如 `agentz-learning`）→ 複製出來
5. **複製出來的那個 `sk-ant-...` 字串就是你的 API key**——存到密碼管理器，**不要貼到任何公開地方**

> ⚠️ **重要**：API key 等於你信用卡的 PIN——別人拿到就可以用你的額度跑 LLM。
> - 不要 commit 到 git
> - 不要貼 Discord / Slack / 公開 issue
> - 不要寫在 code 裡——用環境變數（後面教）

### 備選：OpenAI GPT

到 https://platform.openai.com/api-keys 一樣流程。OpenAI 沒有免費額度（至少 2026 年初還沒有），最低充 5 美金可以用很久。

### Anthropic / OpenAI 都不要也行：用 Groq（免費）

Groq 提供 Llama / Mixtral 系列 LLM 的**完全免費** API（有 rate limit）。
1. 去 https://console.groq.com/
2. 註冊
3. 拿 `gsk_...` key

本書範例會以 Anthropic 為主軸，但每個範例都會在 §章節末附 Groq / OpenAI 的等價寫法。

---

## 5. 把 API key 設成環境變數（5 分鐘）

不要把 API key 寫進 code。我們把它放在 shell 的**環境變數**裡，code 從環境變數讀。

### macOS / Linux

編輯你的 shell config：
```bash
$ nano ~/.zshrc   # zsh（macOS 預設）
# 或
$ nano ~/.bashrc  # bash
```

最下面加上：
```bash
export ANTHROPIC_API_KEY="sk-ant-...你的 key..."
export OPENAI_API_KEY="sk-...你的 key..."  # 如果有
export GROQ_API_KEY="gsk_...你的 key..."   # 如果有
```

存檔（`Ctrl + O` 然後 `Ctrl + X`），然後 source：
```bash
$ source ~/.zshrc
$ echo $ANTHROPIC_API_KEY  # 應該印出你的 key
```

### Windows（PowerShell）

```powershell
> [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

**關掉再重開 Terminal**，然後：
```powershell
> $env:ANTHROPIC_API_KEY
```

---

## 6. 你的第一個 LLM Hello-World（10 分鐘）

**目標**：你輸入「你好」，Claude 回你一句話，印在 Terminal。

### 建一個工作資料夾

```bash
$ mkdir agentz-learning
$ cd agentz-learning
```

### 用 uv 建虛擬環境

```bash
$ uv init
$ uv add anthropic
```

> 💡 **虛擬環境**：把這個專案的 python 套件跟其他專案隔開，避免互相打架。`uv init` 自動建好。

### 寫第一支 script

新增檔案 `hello.py`：

```python
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "你好，用繁體中文跟我問好，並推薦我學 AI Agent。"}
    ]
)

print(message.content[0].text)
```

### 跑！

```bash
$ uv run hello.py
```

你應該看到 Claude 用繁中跟你問好+推薦學 AI Agent 的一段回答。

恭喜——**你的第一個 LLM Hello-World 完成了**。截圖留著，這是你第一個 Watcher 階段 milestone evidence。

---

## 7. 跑不出來？常見錯誤排查

| 錯誤訊息 | 原因 | 怎麼修 |
|---|---|---|
| `ModuleNotFoundError: No module named 'anthropic'` | 沒裝 anthropic 套件 | `uv add anthropic` 再 `uv run hello.py` |
| `KeyError: 'ANTHROPIC_API_KEY'` | 環境變數沒設好 | 回 §5 確認，再開新 Terminal |
| `anthropic.AuthenticationError` | API key 是錯的 | 回 console 重 copy；注意首尾無空白 |
| `anthropic.NotFoundError: model: claude-haiku-4-5` | 模型名打錯/未啟用 | 換 `claude-haiku-4-5-20251001` 或 `claude-3-5-haiku-latest` |
| 命令 `uv` not found | uv 沒裝好 / shell 沒 source | 回 §2 |

---

## 8. 動手練習

### 練習 0.1：你的第一個 Hello-World
完成 §6 — 跑出 LLM 用繁中回你的問候。
**成功標準**：Terminal 看到 Claude 的回答。**儲存截圖**，本章 milestone evidence。

### 練習 0.2：問同樣問題、看兩家
複製 `hello.py` 為 `hello-openai.py`，改用 OpenAI（或 Groq，看你申請了哪個）的 API 問同樣問題。
**成功標準**：兩家答案在你 Terminal 並排比較。

> 💡 OpenAI 套件名是 `openai`，範例：
> ```python
> from openai import OpenAI
> client = OpenAI()
> resp = client.chat.completions.create(model="gpt-4o-mini", messages=[...])
> ```
> Groq 用 OpenAI 套件加 base_url 即可：
> ```python
> client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
> ```

### 練習 0.3：把作業上 git
```bash
$ cd agentz-learning
$ git init
$ echo ".env" > .gitignore
$ git add hello.py hello-openai.py
$ git commit -m "Ch 0 hello-world"
```
**成功標準**：`git log` 看得到你的第一個 commit。

---

## 9. 你做完這一章後 ✅

- [ ] Terminal 打開過、跑過 `echo Hello`
- [ ] Python 3.10+ 裝好，`python --version` 印出版本
- [ ] git 裝好，設過 user.name / user.email
- [ ] 申請過至少一家 LLM API key（Anthropic / OpenAI / Groq 任選）
- [ ] API key 放在環境變數，沒 hardcode 在 code
- [ ] 跑出練習 0.1 — 第一個 LLM Hello-World
- [ ] （加分）跑完 0.2 對比兩家
- [ ] （加分）作業進 git

打勾 6 個以上，進 [Ch 1 — LLM 是什麼](../ch01_llm_basics/)。

---

## 10. 補充：本章用到的工具總覽

| 工具 | 角色 | 後面還會用 |
|---|---|---|
| **Terminal** | 跑指令的介面 | 全書 |
| **Python 3.12** | 寫 agent 的程式語言 | 全書 |
| **uv** | Python 套件管理（裝/移除/版本鎖） | 全書 |
| **git** | 版本管理 | 全書 |
| **環境變數**（`ANTHROPIC_API_KEY` 等） | 安全存 API key | 全書 |
| **anthropic / openai / groq SDK** | 呼叫 LLM API | Ch 1 起 |

下一章 [Ch 1](../ch01_llm_basics/) 會把「LLM 是什麼」真正講清楚——你接下來會問的所有問題（token、context、cost、model 怎麼選）都會在 Ch 1 找到答案。
