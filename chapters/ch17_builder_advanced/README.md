# Ch 17 — Builder 進階：Agentic-RL 入門

> **75-90 分鐘**。讀完你會懂：agentic-RL 是什麼、SFT / GRPO / PPO 怎麼用在 agent fine-tune、什麼時候訓 agent 比 prompt 更划算。
>
> 動手練習：跑 SFT pipeline fine-tune 一個小 model 做 function-calling、用 GRPO 加強。
>
> 前置：Builder 階段 Ch 9-15 全完，Python 基礎扎實。

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

---

## 2. 三個主要技術

| 技術 | 全名 | 性質 | 適用 |
|---|---|---|---|
| **SFT** | Supervised Fine-Tuning | 用 (prompt, expected output) pair fine-tune | 有大量人工標註資料 |
| **DPO** | Direct Preference Optimization | 用 (prompt, chosen, rejected) triplet | 有人工偏好資料 |
| **GRPO** | Group Relative Policy Optimization | RL，用 reward 不用 reference model（DeepSeek 2024 提出）| 沒大量標註、有自動 reward |
| **PPO** | Proximal Policy Optimization | 經典 RL | 有 reward function 但訓練成本高 |

2025-2026 流行：**SFT 暖身 → GRPO 強化**。

---

## 3. 什麼時候訓 agent 比 prompt 更划算？

### 該訓
- **小 model fine-tune 跑特定任務**（7B model 跑 function calling 比 prompting GPT-4 便宜 100x）
- **特定 domain 的 reasoning**（醫學 / 法律 / 程式碼）
- **prompt + RAG 已經調到極限但還是不夠好**
- **你的 inference scale 大到 fine-tune 的訓練成本能攤平**（每月 100M+ token）

### 不該訓
- **想省 prompt 工**（fine-tune 比 prompt 工大 10x）
- **任務還沒穩定**（每週改需求就重訓？崩潰）
- **沒 GPU 資源**（8x A100 / H100 一輪訓 8-24 hr）

---

## 4. SFT pipeline 概念

```
1. 收 (prompt, ideal output) pair — 通常 1K-10K 對才有效
2. 套 model（如 Llama-3.3-8B）
3. LoRA / QLoRA adapter fine-tune（不訓全參數，省 GPU）
4. eval 跑 benchmark 看效果
```

工具：
- **TRL**（HuggingFace transformers reinforcement learning）— SFT / DPO / PPO 全包
- **Unsloth**（Llama / Mistral 加速 fine-tune）
- **Axolotl**（高階配置 fine-tune framework）

跑得起來：Mac M3 24GB 可訓 7B QLoRA，Colab T4 可訓 3B。

---

## 5. GRPO 概念

`GRPO` = Group Relative Policy Optimization，DeepSeek-R1 2024 用的方法。

核心：不用 reference model 計算 advantage，**直接從一組 sample 算 relative advantage**。

```
1. 對同一個 prompt sample N 個 output（例 N=8）
2. 每個 output 給 reward（自動評：math 對不對 / code 跑不跑得起來 / agent 任務完不完成）
3. 算 group mean reward
4. 每個 output 的 advantage = reward - group_mean
5. policy gradient 更新
```

**為什麼 hot**：DeepSeek-R1 用這個方法、671B model **沒用 SFT** 直接 RL 就跑出 OpenAI o1 水平的 reasoning。

實作工具：`TRL` 從 v0.13 起有 `GRPOTrainer`。

---

## 6. Agentic-RL 真實 stack

```
1. 環境 (Environment): agent 要在哪跑？
   - tool sandbox (允許 call 哪些 API)
   - reward function (任務完成標準)
2. Policy: agent 本身（一個 LLM）
3. Rollout: agent 用 policy 跑任務、生 trajectory
4. Reward: 每個 trajectory 收尾算分
5. Update: policy gradient（GRPO / PPO）
```

訓 1 個小 agent: 8-24 hr / 8x A100。
訓 1 個有用的 agent: 一週 + 一堆嘗試。

---

## 7. 動手練習（可選，需 GPU）

### 練習 17.1：SFT Function-calling 小 model

用 `TRL` + Llama-3.3-8B-Instruct 用 Glaive function-calling dataset fine-tune。eval 在 BFCL benchmark。

**成功標準**：你的 fine-tuned model 在 BFCL 比 base model 高 10%+。

> 需要：> 24GB GPU（建議 Colab A100 / 你的 M3 Max）

### 練習 17.2：GRPO 跑一個 math task

用 `TRL.GRPOTrainer` + Qwen2.5-Math-1.5B 跑 GSM8K reasoning。

**成功標準**：跑得起來、reward 曲線往上。

### 練習 17.3：讀一篇 paper 寫 200 字心得

挑下面任一 paper 讀完寫筆記：
- DeepSeek-R1: https://arxiv.org/abs/2501.12948
- ReAct: https://arxiv.org/abs/2210.03629
- Reflexion: https://arxiv.org/abs/2303.11366

**成功標準**：你能跟人解釋這篇 paper 的 method + 重要性。

---

## 8. 你做完這一章後 ✅

- [ ] 知道 Agentic-RL 跟 traditional fine-tune 差別
- [ ] 知道 SFT / DPO / GRPO / PPO 性質
- [ ] 知道何時該訓 / 何時 prompt 就好
- [ ] 知道 TRL / Unsloth / Axolotl 三個工具
- [ ] 知道 GRPO 為什麼 2024-2025 變熱
- [ ] 至少跑完練習 17.3（讀 paper）

打勾 4 個以上，進 [Ch 18](../ch18_maker_educator/) 或開始你的 Capstone。

---

## 9. 補充閱讀

- [DeepSeek-R1 paper](https://arxiv.org/abs/2501.12948)
- [TRL 文件](https://huggingface.co/docs/trl)
- [Unsloth](https://github.com/unslothai/unsloth)
- [mlabonne/llm-course](https://github.com/mlabonne/llm-course)（79K⭐）— fine-tune / quant / RL 完整 Colab
- `datawhalechina/hello-agents` 第十一章 — Agentic-RL 中文
