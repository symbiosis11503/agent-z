# Ch 17 — Builder 進階：Agentic-RL 入門

> **90-120 分鐘**。讀完你會懂：agentic-RL 是什麼、SFT / DPO / GRPO / PPO 怎麼用在 agent fine-tune、什麼時候訓 agent 比 prompt 更划算、TRL/Unsloth/Axolotl 三大 framework 差異、本地 vs cloud 訓練成本對照、常見地雷。
>
> 動手練習：跑 SFT pipeline fine-tune 一個小 model 做 function-calling、用 GRPO 加強、跑 DeepSeek-R1 復現迷你版。
>
> 前置：Builder 階段 [Ch 9](../ch09_function_calling/)-[Ch 15](../ch15_deploy_audit_replay/) 全完，Python 基礎扎實。

> ⚠️ **這章 advanced**——多數人不需要走到這。**如果你的 agent prompt + RAG + framework 都打不過 GPT-4 級**，不要往這走。先優化前面層。

---

## 1. 什麼是 Agentic-RL？

傳統 LLM fine-tune 是 supervised：給「input → output」pair。

**Agentic-RL** 不一樣：你只給「target」（任務目標），agent 自己跑很多次嘗試，**只用「成不成功」這個 sparse reward** 學習怎麼做對。

範例：
- 給「訂下週去東京的便宜機票」這個任務 1000 次
- 每次 agent 自己嘗試一個 tool sequence
- 用「最後是否真的訂到票 / 訂到的票是不是真的便宜」當 reward
- gradient 更新 agent policy
- 收斂後 agent 學會「先查日期 → 再比價 → 再選最便宜 → 再訂」的策略

**對比 SFT**：SFT 需要你寫好「正確答案」（trajectory 範本）；Agentic-RL 只要寫好「怎麼判定成功」的 reward function。後者門檻看似低、實際更難 — reward hacking、sparse signal 都是大坑。

---

## 2. 三大主要技術 + 兩個衍生

| 技術 | 全名 | 性質 | 適用 | 訓練成本 |
|---|---|---|---|---|
| **SFT** | Supervised Fine-Tuning | 用 (prompt, expected output) pair fine-tune | 有大量人工標註資料 | ★ 最低 |
| **DPO** | Direct Preference Optimization | 用 (prompt, chosen, rejected) triplet | 有人工偏好資料、不想設計 reward fn | ★★ |
| **GRPO** | Group Relative Policy Optimization | RL，用 reward 不用 reference model（DeepSeek 2024 提出） | 沒大量標註、有自動 reward | ★★★ |
| **PPO** | Proximal Policy Optimization | 經典 RL | 有 reward function 但訓練成本高 | ★★★★ |
| **KTO** | Kahneman-Tversky Optimization | 用 binary label（好/壞）不要 pair | 只能標 like/dislike 的場景 | ★★ |

**2025-2026 主流路線**：
1. **SFT 暖身**（cold-start，2-5K 樣本）→ **GRPO 強化**（用 RM 或 verifier 給 reward）
2. **DPO** 替代 RLHF 成為偏好對齊的 default
3. **OpenAI o1 / DeepSeek-R1** 證明 RL 能誘發 long-CoT reasoning，不再需要海量 SFT

---

## 3. 什麼時候訓 agent 比 prompt 更划算？

### 該訓
- **小 model fine-tune 跑特定任務**（7B model 跑 function calling 比 prompting GPT-4 便宜 100x）
- **特定 domain 的 reasoning**（醫學 / 法律 / 程式碼）
- **prompt + RAG 已經調到極限但還是不夠好**
- **inference scale 大到 fine-tune 成本能攤平**（每月 100M+ token）
- **隱私 / on-prem 部署需求** — 不能傳 prompt 給雲端 API
- **行為一致性要求高** — 同 prompt 100 次要 100% 結果一致

### 不該訓
- **想省 prompt 工**（fine-tune 比 prompt 工大 10x）
- **任務還沒穩定**（每週改需求就重訓？崩潰）
- **沒 GPU 資源**（8x A100 / H100 一輪訓 8-24 hr）
- **資料量 < 1K**（樣本太少 fine-tune 效果差，prompt + few-shot 還比較好）
- **多任務 generalist** — 訓 1 個 fine-tuned model 通常變專科、失通用

### 決策決策樹

```
有 GPU 預算嗎? ─ No ──► 用大 model API + prompt + RAG
       │
       Yes
       │
資料 > 1K 樣本嗎? ─ No ──► 用 prompt + few-shot
       │
       Yes
       │
任務 well-defined 嗎? ─ No ──► 先把 spec 寫清楚
       │
       Yes
       │
prompt + RAG 已調極限嗎? ─ No ──► 繼續調 prompt
       │
       Yes
       │
       ▼
   可以 fine-tune
```

---

## 4. SFT pipeline — 真實 code

> 💡 **想知道 Llama / Qwen / DeepSeek 等開源 model 怎麼本地跑或申請 cloud API**？翻 [LLM / API 申請 — 本地 / 主權 / 中文圈](https://symbiosis11503.github.io/agent-z/llm-providers/local-sovereign) — 含 Ollama / TAIDE / Qwen-GLM-Yi 三類詳細申請流程。

```python
# pip install trl transformers datasets peft bitsandbytes accelerate
from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from datasets import load_dataset
import torch

# 1. Load model + tokenizer (4-bit quant + LoRA = 跑在 24GB GPU)
model_id = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    load_in_4bit=True,  # QLoRA 省 VRAM
    device_map="auto",
)

# 2. Load dataset (function-calling 範例: glaiveai/glaive-function-calling-v2)
dataset = load_dataset("glaiveai/glaive-function-calling-v2", split="train[:5000]")

# 3. LoRA config (只訓 adapter, 不動 base model)
peft_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none", task_type="CAUSAL_LM",
)

# 4. Trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    peft_config=peft_config,
    args=SFTConfig(
        output_dir="./llama-3.2-3b-fc",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=50,
        save_steps=500,
        warmup_ratio=0.1,
        max_seq_length=2048,
    ),
)

trainer.train()
trainer.save_model("./llama-3.2-3b-fc-final")
```

**真實 cost**（2026-05）：
- Mac M3 Max 64GB：3B QLoRA, 5K 樣本 ~ 4-6 hr
- 1× A100 80GB（Colab Pro+ / runpod $1.5/hr）：3B QLoRA ~ 1-2 hr
- 1× H100 80GB（runpod $3/hr）：7B QLoRA ~ 1 hr
- 8× A100：30B QLoRA ~ 4 hr，70B QLoRA ~ 8-12 hr

---

## 5. GRPO 真實 code

`GRPO` = Group Relative Policy Optimization，DeepSeek-R1 2024 用的方法。

**核心**：不用 reference model 計算 advantage，**直接從一組 sample 算 relative advantage**。

```python
# pip install trl>=0.13
from trl import GRPOConfig, GRPOTrainer
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset

# 1. Reward function — math task: 答對 = 1, 答錯 = 0
def reward_correct(completions, **kwargs):
    rewards = []
    for c in completions:
        text = c[0]["content"] if isinstance(c, list) else c
        # 用 regex 抽答案 + 對比 ground truth
        answer = extract_boxed_answer(text)
        gt = kwargs["answer"]
        rewards.append(1.0 if answer == gt else 0.0)
    return rewards

# 2. Reward function — format compliance: 必須含 <think> + <answer>
def reward_format(completions, **kwargs):
    rewards = []
    for c in completions:
        text = c[0]["content"] if isinstance(c, list) else c
        has_think = "<think>" in text and "</think>" in text
        has_answer = "<answer>" in text and "</answer>" in text
        rewards.append(0.5 if (has_think and has_answer) else 0.0)
    return rewards

# 3. Load math dataset
dataset = load_dataset("openai/gsm8k", "main", split="train[:2000]")

# 4. Train
trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-Math-1.5B-Instruct",
    reward_funcs=[reward_correct, reward_format],
    train_dataset=dataset,
    args=GRPOConfig(
        output_dir="./qwen-math-grpo",
        learning_rate=5e-6,
        num_generations=8,       # 每個 prompt sample 8 次（group size）
        max_completion_length=512,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=8,
        num_train_epochs=1,
        bf16=True,
        logging_steps=10,
    ),
)
trainer.train()
```

**為什麼 hot**：
- DeepSeek-R1 用這個方法、671B model **沒用 SFT** 直接 RL 就跑出 OpenAI o1 水平的 reasoning
- DeepSeek-R1-Distill-Qwen-7B 用 GRPO + verifier reward，做出 7B 級 reasoning model 直逼 GPT-4o
- 2025-2026 開源圈被「複現 R1」浪潮席捲

---

## 6. 三大 fine-tune framework 對照

| Framework | 強項 | 限制 | 適合 |
|---|---|---|---|
| **TRL**（HuggingFace） | 官方、SFT/DPO/GRPO/PPO 全包、活躍 | 設定多、學曲線陡 | 嚴肅 production |
| **Unsloth** | Llama / Mistral / Qwen 加速 2x、省 VRAM 50% | model 範圍小、商用授權需 check | Mac / 單卡訓練 |
| **Axolotl** | YAML 配置、社群多預設 | 客製 callback 麻煩 | 標準流程批量訓練 |

**Unsloth 範例**（最快上手）：

```python
# pip install unsloth
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length=2048, dtype=None, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
# 接 TRL SFTTrainer 跟前面一樣
```

---

## 7. Agentic-RL 真實 stack

```
┌─ Environment ──────────────────────────┐
│  - Tool sandbox (allowed APIs)         │
│  - Reward function (task completion)   │
│  - Episode terminator (max steps)      │
└────────────────────────────────────────┘
            ▲                  │
            │ trajectory       │ observation
            │                  ▼
┌─ Policy ────────────────────────────────┐
│  - LLM (Llama-3 / Qwen / DeepSeek)     │
│  - Generates: thought + tool_call      │
└─────────────────────────────────────────┘
            ▲                  │
            │ gradient update  │ action
            │                  ▼
┌─ Optimizer (GRPO / PPO) ────────────────┐
│  - 收 reward → 算 advantage             │
│  - Update policy via gradient           │
└─────────────────────────────────────────┘
```

**訓 1 個小 agent**: 8-24 hr / 8x A100。
**訓 1 個有用的 agent**: 一週 + 一堆嘗試。

### Reward function 設計（**最容易踩坑的地方**）

| Reward 類型 | 例子 | 風險 |
|---|---|---|
| **Outcome-based** | 任務完成 = 1, 失敗 = 0 | 太 sparse，初期梯度都接近 0 |
| **Process-based** | 每步 tool 用對 = +0.1 | reward hacking — agent 學會狂 call 工具刷分 |
| **Verifier-based** | 用另一個 model 評分 | verifier 自己 hallucinate，gradient noisy |
| **Mixed** | outcome 為主 + format 為輔 | **建議起手**，平衡 sparse 跟 dense |

**反例**（reward hacking）：訓客服 agent 給 reward「conversation 結束時 user 沒抱怨」→ agent 學會講很客氣的場面話、不解決問題只敷衍。

---

## 8. 常見地雷（**讀過比沒讀過省一週訓練**）

| 地雷 | 症狀 | 解法 |
|---|---|---|
| **GPU OOM** | CUDA out of memory | 開 4-bit + LoRA + 降 batch size / max_seq |
| **gradient 全 0** | loss 不降、reward 全部一樣 | reward function 加 dense signal (format 等) |
| **reward hacking** | metric 飆升但實際變爛 | 加 eval 跑真實任務 + human spot-check |
| **overfit** | train loss ↓ eval loss ↑ | 加 early stop / 減 epoch / 加 regularization |
| **catastrophic forgetting** | fine-tune 後通用能力大降 | LoRA 替全參數 + KL penalty + retain set |
| **資料污染** | dataset 含 eval set | 訓前 grep eval prompts 從 train set 移除 |
| **chat template 錯** | 訓完 inference 像沒訓 | 確認 train + inference 用同 chat_template |
| **eval 用一次性 seed** | 結果跟同事不對 | eval 用 temperature=0 + 固定 seed + 多次平均 |
| **prompt 跟 production 不一致** | 上線比 eval 爛 | 訓資料的 prompt 結構 = production prompt 結構 |

---

## 9. Real case：DeepSeek-R1 復現浪潮

DeepSeek-R1 2025-01 發 paper 後，開源圈兩個月內出了 5+ 個復現專案：

| 專案 | 規模 | 重點 |
|---|---|---|
| [open-r1](https://github.com/huggingface/open-r1) | HF 官方 | 完整 pipeline + 公開 dataset |
| [TinyZero](https://github.com/Jiayi-Pan/TinyZero) | < $30 訓練成本 | 3B model 做 Countdown task |
| [simpleRL-reason](https://github.com/hkust-nlp/simpleRL-reason) | 7B Qwen | 最簡 GRPO recipe |
| [logic-rl](https://github.com/Unakar/Logic-RL) | 7B | 邏輯 task verifier-based reward |
| [DeepSeek-R1-Distill](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B) | 1.5B-70B | SFT distill 版本 |

**啟發**：
1. GRPO + verifiable task（math/code）= 強 reasoning
2. **不需要 671B**，7B 也能跑出 long-CoT
3. cold-start SFT (2K-5K 樣本) → GRPO 是新 default

---

## 10. 動手練習（可選，需 GPU）

### 練習 17.1：SFT Function-calling 小 model

用 `TRL` + Llama-3.2-3B-Instruct + Glaive function-calling dataset fine-tune。eval 在 BFCL benchmark。
**成功標準**：fine-tuned model 在 BFCL 比 base model 高 10%+。

> 需要：> 24GB GPU（建議 Colab A100 / Mac M3 Max / runpod）

### 練習 17.2：GRPO 跑一個 math task

用 `TRL.GRPOTrainer` + Qwen2.5-Math-1.5B 跑 GSM8K reasoning。
**成功標準**：跑得起來、reward 曲線往上、final accuracy > base + 5%。

### 練習 17.3：讀一篇 paper 寫 200 字心得

挑下面任一 paper 讀完寫筆記：
- [DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [Reflexion](https://arxiv.org/abs/2303.11366)
- [Tülu 3](https://arxiv.org/abs/2411.15124) — Ai2 post-training recipe 全公開

**成功標準**：你能跟人解釋這篇 paper 的 method + 重要性。

### 練習 17.4 (bonus)：迷你 R1 復現

跟 [TinyZero](https://github.com/Jiayi-Pan/TinyZero) 跑 Countdown task（給 3-4 個數字湊出 target）。
**成功標準**：3B model GRPO 訓完跑 Countdown accuracy > 80%。

---

## 11. 你做完這一章後 ✅

- [ ] 知道 Agentic-RL 跟 traditional fine-tune 差別
- [ ] 知道 SFT / DPO / GRPO / PPO / KTO 性質
- [ ] 知道何時該訓 / 何時 prompt 就好（決策樹）
- [ ] 知道 TRL / Unsloth / Axolotl 三個工具差異
- [ ] 知道 GRPO 為什麼 2024-2025 變熱
- [ ] 知道 9 個常見地雷（OOM / reward hacking / chat template ...）
- [ ] 至少跑完練習 17.3（讀 paper）+ bonus 17.1 或 17.4

打勾 5 個以上，進 [Ch 18](../ch18_maker_educator/) 或開始你的 Capstone。

---

## 11b. 在這頁練 reward function 設計

給 LLM 一個 agent 任務，看它能不能寫出 reward function：

<LLMTryout
  title="Ch 17 in-page tryout — reward function 設計"
  defaultSystem="你是 agentic-RL 教練。看使用者描述的 agent 任務，輸出 (1) 適合的 reward function 設計（outcome / process / verifier / mixed） (2) 至少 1 個 reward hacking 風險警告 (3) suggested verifier 怎寫。回繁中 + Python pseudo-code。"
  defaultPrompt="我要訓一個 agent 去訂便宜機票。怎麼設 reward？" />

---

## 12. 補充閱讀

- [DeepSeek-R1 paper](https://arxiv.org/abs/2501.12948) — 必讀
- [Tülu 3 paper](https://arxiv.org/abs/2411.15124) — Ai2 完整 post-training recipe 公開
- [TRL 文件](https://huggingface.co/docs/trl)
- [Unsloth](https://github.com/unslothai/unsloth)
- [Axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- [open-r1](https://github.com/huggingface/open-r1) — HF 官方 R1 復現
- [TinyZero](https://github.com/Jiayi-Pan/TinyZero) — < $30 復現 R1 minimal
- [mlabonne/llm-course](https://github.com/mlabonne/llm-course)（79K⭐）— fine-tune / quant / RL 完整 Colab
- `datawhalechina/hello-agents` 第十一章 — Agentic-RL 中文
- [Hugging Face Reasoning Course](https://huggingface.co/learn/reasoning-course) — 互動式 R1 復現
- [verifiers library](https://github.com/willccbb/verifiers) — GRPO reward function 框架
