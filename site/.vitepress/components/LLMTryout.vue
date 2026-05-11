<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  defaultPrompt?: string
  defaultSystem?: string
  title?: string
}>()

type Provider = 'anthropic' | 'openrouter' | 'groq' | 'openai'

const provider = ref<Provider>('anthropic')
const apiKey = ref('')
const systemPrompt = ref(props.defaultSystem ?? '')
const userPrompt = ref(props.defaultPrompt ?? '用繁中三句話解釋什麼是 AI Agent。')
const output = ref('')
const loading = ref(false)
const meta = ref('')

const modelByProvider: Record<Provider, string> = {
  anthropic: 'claude-haiku-4-5',
  openrouter: 'anthropic/claude-3.5-haiku',
  groq: 'llama-3.3-70b-versatile',
  openai: 'gpt-4o-mini',
}

const placeholderByProvider: Record<Provider, string> = {
  anthropic: 'sk-ant-...',
  openrouter: 'sk-or-v1-...',
  groq: 'gsk_...',
  openai: 'sk-...',
}

const keyEnvName = computed(() => ({
  anthropic: 'ANTHROPIC_API_KEY',
  openrouter: 'OPENROUTER_API_KEY',
  groq: 'GROQ_API_KEY',
  openai: 'OPENAI_API_KEY',
}[provider.value]))

async function run() {
  if (!apiKey.value.trim()) {
    output.value = '請先貼上 ' + keyEnvName.value + '（不會被傳到任何伺服器，只走你瀏覽器直接打到 vendor）'
    return
  }
  loading.value = true
  output.value = ''
  meta.value = ''
  const t0 = performance.now()
  try {
    let text = ''
    let inTok = 0, outTok = 0
    if (provider.value === 'anthropic') {
      const resp = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey.value.trim(),
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: JSON.stringify({
          model: modelByProvider[provider.value],
          max_tokens: 500,
          system: systemPrompt.value || undefined,
          messages: [{ role: 'user', content: userPrompt.value }],
        }),
      })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${await resp.text()}`)
      const data = await resp.json()
      text = data.content?.[0]?.text ?? JSON.stringify(data)
      inTok = data.usage?.input_tokens ?? 0
      outTok = data.usage?.output_tokens ?? 0
    } else {
      const url = {
        openrouter: 'https://openrouter.ai/api/v1/chat/completions',
        groq: 'https://api.groq.com/openai/v1/chat/completions',
        openai: 'https://api.openai.com/v1/chat/completions',
      }[provider.value]
      const messages = []
      if (systemPrompt.value) messages.push({ role: 'system', content: systemPrompt.value })
      messages.push({ role: 'user', content: userPrompt.value })
      const resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey.value.trim()}`,
        },
        body: JSON.stringify({ model: modelByProvider[provider.value], messages, max_tokens: 500 }),
      })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${await resp.text()}`)
      const data = await resp.json()
      text = data.choices?.[0]?.message?.content ?? JSON.stringify(data)
      inTok = data.usage?.prompt_tokens ?? 0
      outTok = data.usage?.completion_tokens ?? 0
    }
    output.value = text
    const dt = ((performance.now() - t0) / 1000).toFixed(1)
    meta.value = `model: ${modelByProvider[provider.value]} · in=${inTok} · out=${outTok} · ${dt}s`
  } catch (e: any) {
    output.value = '❌ ' + (e?.message ?? String(e))
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="agentz-tryout">
    <h4>{{ title || '動手練習 — 即時試一下（瀏覽器直連 vendor，key 不經我們伺服器）' }}</h4>

    <div class="row">
      <label>Provider</label>
      <select v-model="provider">
        <option value="anthropic">Anthropic Claude (haiku-4-5)</option>
        <option value="openrouter">OpenRouter (claude-3.5-haiku 等)</option>
        <option value="groq">Groq Llama-3.3-70b (免費)</option>
        <option value="openai">OpenAI GPT-4o-mini</option>
      </select>
    </div>

    <div class="row">
      <label>API key</label>
      <input type="password" v-model="apiKey" :placeholder="placeholderByProvider[provider]" />
    </div>

    <div class="row" v-if="systemPrompt !== undefined">
      <label>System prompt</label>
      <textarea v-model="systemPrompt" rows="2" placeholder="(可選) 給 LLM 的角色 / 約束"></textarea>
    </div>

    <div class="row">
      <label>User prompt</label>
      <textarea v-model="userPrompt" rows="3"></textarea>
    </div>

    <button @click="run" :disabled="loading">
      {{ loading ? '跑中...' : '送出' }}
    </button>

    <div v-if="output" class="out">{{ output }}</div>
    <div v-if="meta" class="meta">{{ meta }}</div>
  </div>
</template>
