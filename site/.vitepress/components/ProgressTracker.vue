<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const STORAGE_KEY = 'agentz-progress-v1'

const allChapters = [
  { id: 'ch-1', title: 'Ch-1 零基礎全景', stage: '前言' },
  { id: 'ch00', title: 'Ch 0 把工具裝好', stage: '前言' },
  { id: 'ch01', title: 'Ch 1 LLM 是什麼', stage: 'Watcher' },
  { id: 'ch02', title: 'Ch 2 Prompt 設計', stage: 'Watcher' },
  { id: 'ch03', title: 'Ch 3 什麼是 Agent', stage: 'Watcher' },
  { id: 'ch04', title: 'Ch 4 CLI Agent 入門', stage: 'Operator' },
  { id: 'ch05', title: 'Ch 5 CLI Workflow', stage: 'Operator' },
  { id: 'ch06', title: 'Ch 6 MCP', stage: 'Operator' },
  { id: 'ch07', title: 'Ch 7 Skills / Plugins', stage: 'Operator' },
  { id: 'ch08', title: 'Ch 8 Cost / 介入', stage: 'Operator' },
  { id: 'ch09', title: 'Ch 9 Function calling', stage: 'Builder' },
  { id: 'ch10', title: 'Ch 10 ReAct 範式', stage: 'Builder' },
  { id: 'ch11', title: 'Ch 11 框架比較', stage: 'Builder' },
  { id: 'ch12', title: 'Ch 12 自寫 mini framework', stage: 'Builder' },
  { id: 'ch13', title: 'Ch 13 Memory & RAG', stage: 'Builder' },
  { id: 'ch14', title: 'Ch 14 Multi-agent', stage: 'Builder' },
  { id: 'ch15', title: 'Ch 15 Deploy / Audit (V3 case)', stage: 'Builder' },
  { id: 'ch16', title: 'Ch 16 Researcher', stage: '進階' },
  { id: 'ch17', title: 'Ch 17 Builder 進階', stage: '進階' },
  { id: 'ch18', title: 'Ch 18 Maker / Educator', stage: '進階' },
]

const checked = ref<Record<string, boolean>>({})

onMounted(() => {
  try {
    checked.value = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
  } catch { checked.value = {} }
})

function toggle(id: string) {
  checked.value = { ...checked.value, [id]: !checked.value[id] }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(checked.value))
}

function reset() {
  if (!confirm('確定清除所有進度？')) return
  checked.value = {}
  localStorage.removeItem(STORAGE_KEY)
}

const doneCount = computed(() => Object.values(checked.value).filter(Boolean).length)
const totalCount = computed(() => allChapters.length)
const pct = computed(() => Math.round((doneCount.value / totalCount.value) * 100))
</script>

<template>
  <div class="agentz-progress">
    <h4>📊 你的學習進度（存在你瀏覽器，不上傳）</h4>
    <div class="bar"><div class="bar-fill" :style="{ width: pct + '%' }"></div></div>
    <div class="stats">
      <span>{{ doneCount }} / {{ totalCount }} 章完成（{{ pct }}%）</span>
      <button @click="reset" style="font-size: 0.75rem; padding: 0.2rem 0.6rem; background: transparent; color: var(--vp-c-text-2); border: 1px solid var(--vp-c-divider); border-radius: 4px; cursor: pointer;">清除</button>
    </div>

    <div style="margin-top: 1.2rem;">
      <details v-for="stage in ['前言', 'Watcher', 'Operator', 'Builder', '進階']" :key="stage" :open="stage === 'Watcher' || stage === 'Operator'">
        <summary style="cursor: pointer; padding: 0.4rem 0; font-weight: 600; color: var(--vp-c-text-1);">
          {{ stage }}
          <span style="margin-left: 0.5rem; font-size: 0.8rem; color: var(--vp-c-text-2); font-weight: normal;">
            ({{ allChapters.filter(c => c.stage === stage && checked[c.id]).length }} / {{ allChapters.filter(c => c.stage === stage).length }})
          </span>
        </summary>
        <ul style="list-style: none; padding-left: 1rem;">
          <li v-for="c in allChapters.filter(c => c.stage === stage)" :key="c.id" style="padding: 0.25rem 0;">
            <label style="cursor: pointer; user-select: none;">
              <input type="checkbox" :checked="checked[c.id]" @change="toggle(c.id)" />
              <span :style="{ textDecoration: checked[c.id] ? 'line-through' : 'none', color: checked[c.id] ? 'var(--vp-c-text-3)' : 'var(--vp-c-text-1)' }">
                {{ c.title }}
              </span>
            </label>
          </li>
        </ul>
      </details>
    </div>
  </div>
</template>
