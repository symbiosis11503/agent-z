import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-TW',
  title: 'AgentZ',
  description: '從零到 AI Agent 構建者 — 繁中 first-class、vendor-neutral、Claude Code 生態深入的 AI Agent 學習系統',
  base: '/agent-z/',
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,
  rewrites: {
    'chapters/:dir/README.md': 'chapters/:dir/index.md',
  },

  sitemap: {
    hostname: 'https://symbiosis11503.github.io/agent-z/',
  },

  head: [
    ['meta', { name: 'theme-color', content: '#5b21b6' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'AgentZ — 從零到 AI Agent 構建者' }],
    ['meta', { property: 'og:description', content: '繁中 first-class、vendor-neutral、Claude Code 生態深入的 AI Agent 學習系統' }],
    ['meta', { property: 'og:url', content: 'https://symbiosis11503.github.io/agent-z/' }],
    ['meta', { property: 'og:image', content: 'https://symbiosis11503.github.io/agent-z/logo.svg' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: 'AgentZ — 從零到 AI Agent 構建者' }],
    ['meta', { name: 'twitter:description', content: '繁中 first-class、vendor-neutral、Claude Code 生態深入的 AI Agent 學習系統' }],
    ['meta', { name: 'keywords', content: 'AI Agent, Claude Code, MCP, AgentZ, 繁體中文, AI 學習, LLM, ReAct, RAG, multi-agent, agentic-RL, TAIDE' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/agent-z/logo.svg' }],
    ['link', { rel: 'canonical', href: 'https://symbiosis11503.github.io/agent-z/' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'AgentZ',

    nav: [
      { text: '首頁', link: '/' },
      { text: '5 分鐘 Quick Win', link: '/quickwin' },
      { text: '課程地圖', link: '/roadmap' },
      { text: '章節', link: '/chapters/ch-1_zero_basics/' },
      { text: '進度檢核', link: '/progress' },
      { text: '名詞表', link: '/glossary' },
      { text: 'LLM / API', link: '/llm-providers' },
      { text: 'FAQ', link: '/faq' },
      { text: '關於', link: '/about' },
      { text: 'GitHub', link: 'https://github.com/symbiosis11503/agent-z' },
    ],

    sidebar: {
      '/chapters/': [
        {
          text: '前言（真零基礎 onramp）',
          collapsed: false,
          items: [
            { text: 'Ch-1 完全沒寫過 code 也能讀的 AI Agent 全景', link: '/chapters/ch-1_zero_basics/' },
            { text: 'Ch 0 把工具裝好', link: '/chapters/ch00_setup/' },
          ]
        },
        {
          text: 'Part 1 — Watcher（理解）',
          collapsed: false,
          items: [
            { text: 'Ch 1 LLM 是什麼', link: '/chapters/ch01_llm_basics/' },
            { text: 'Ch 2 Prompt 設計', link: '/chapters/ch02_prompt/' },
            { text: 'Ch 3 什麼是 Agent', link: '/chapters/ch03_what_is_agent/' },
          ]
        },
        {
          text: 'Part 2 — Operator（操作）',
          collapsed: false,
          items: [
            { text: 'Ch 4 CLI Agent 入門', link: '/chapters/ch04_cli_agents/' },
            { text: 'Ch 5 CLI Workflow', link: '/chapters/ch05_cli_workflow/' },
            { text: 'Ch 6 MCP (Model Context Protocol)', link: '/chapters/ch06_mcp/' },
            { text: 'Ch 7 Skills / Plugins / Marketplace', link: '/chapters/ch07_skills_plugins/' },
            { text: 'Ch 8 Cost 觀測 / 介入', link: '/chapters/ch08_cost_observability/' },
          ]
        },
        {
          text: 'Part 3 — Builder（構建）',
          collapsed: true,
          items: [
            { text: 'Ch 9 Function calling / Tool use', link: '/chapters/ch09_function_calling/' },
            { text: 'Ch 10 ReAct / 範式', link: '/chapters/ch10_react_paradigms/' },
            { text: 'Ch 11 框架比較', link: '/chapters/ch11_frameworks/' },
            { text: 'Ch 12 自寫 mini framework', link: '/chapters/ch12_mini_framework/' },
            { text: 'Ch 13 Memory & RAG', link: '/chapters/ch13_memory_rag/' },
            { text: 'Ch 14 Multi-agent', link: '/chapters/ch14_multi_agent/' },
            { text: 'Ch 15 Deploy + audit + replay + cost cap (V3 case study)', link: '/chapters/ch15_deploy_audit_replay/' },
          ]
        },
        {
          text: 'Part 4 — 進階分流',
          collapsed: true,
          items: [
            { text: 'Ch 16 Researcher 路線', link: '/chapters/ch16_researcher/' },
            { text: 'Ch 17 Builder 進階 (Agentic-RL)', link: '/chapters/ch17_builder_advanced/' },
            { text: 'Ch 18 Maker / Educator 路線', link: '/chapters/ch18_maker_educator/' },
          ]
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/symbiosis11503/agent-z' },
    ],

    footer: {
      message: 'MIT License — 章節內容跟 starter code 都可以 copy 進你自己的商業專案',
      copyright: '© 2026 Symbiosis (SBS) — AgentZ contributors',
    },

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜尋', buttonAriaLabel: '搜尋' },
              modal: {
                noResultsText: '沒有找到結果',
                resetButtonTitle: '清除',
                footer: {
                  selectText: '選擇',
                  navigateText: '切換',
                  closeText: '關閉',
                },
              },
            },
          },
        },
      },
    },

    docFooter: {
      prev: '上一章',
      next: '下一章',
    },

    editLink: {
      pattern: ({ filePath }) => {
        // chapters/ is a symlink to repo-root chapters — edit the real file, not the symlink
        if (filePath.startsWith('chapters/')) {
          return `https://github.com/symbiosis11503/agent-z/edit/main/${filePath}`
        }
        return `https://github.com/symbiosis11503/agent-z/edit/main/site/${filePath}`
      },
      text: '在 GitHub 編輯本頁',
    },

    outline: { label: '本頁目錄' },
    lastUpdatedText: '最後更新',
    darkModeSwitchLabel: '主題',
    lightModeSwitchTitle: '切換淺色',
    darkModeSwitchTitle: '切換深色',
    sidebarMenuLabel: '章節選單',
    returnToTopLabel: '回到頂端',
  },

  markdown: {
    lineNumbers: false,
    theme: { light: 'github-light', dark: 'github-dark-dimmed' },
  },
})
