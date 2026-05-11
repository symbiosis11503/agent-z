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
    ['meta', { property: 'og:image', content: 'https://symbiosis11503.github.io/agent-z/logo.svg' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'keywords', content: 'AI Agent, Claude Code, MCP, AgentZ, 繁體中文, AI 學習, LLM, ReAct, RAG, multi-agent, agentic-RL, TAIDE' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/agent-z/logo.svg' }],
  ],

  transformPageData(pageData) {
    const base = 'https://symbiosis11503.github.io/agent-z/'
    const defaultTitle = 'AgentZ — 從零到 AI Agent 構建者'
    const defaultDesc = '繁中 first-class、vendor-neutral、Claude Code 生態深入的 AI Agent 學習系統'

    let rel = pageData.relativePath.replace(/\.md$/, '')
    rel = rel.replace(/^\.\.\//, '')
    rel = rel.replace(/\/README$/, '/')
    if (rel === 'index') rel = ''
    if (rel.endsWith('/index')) rel = rel.slice(0, -'index'.length)
    const canonicalURL = base + rel

    const pageTitle = pageData.frontmatter.title
      ? `${pageData.frontmatter.title} · AgentZ`
      : (pageData.title ? `${pageData.title} · AgentZ` : defaultTitle)
    const pageDesc = pageData.frontmatter.description || pageData.description || defaultDesc

    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push(
      ['link', { rel: 'canonical', href: canonicalURL }],
      ['meta', { property: 'og:url', content: canonicalURL }],
      ['meta', { property: 'og:title', content: pageTitle }],
      ['meta', { property: 'og:description', content: pageDesc }],
      ['meta', { name: 'twitter:title', content: pageTitle }],
      ['meta', { name: 'twitter:description', content: pageDesc }],
    )

    // JSON-LD on home page: Course schema for SEO rich results / Knowledge Graph
    if (rel === '') {
      const ldCourse = {
        '@context': 'https://schema.org',
        '@type': 'Course',
        name: 'AgentZ — 從零到 AI Agent 構建者',
        description: defaultDesc,
        url: base,
        provider: {
          '@type': 'Organization',
          name: 'Symbiosis (SBS)',
          url: 'https://github.com/symbiosis11503/agent-z',
        },
        inLanguage: 'zh-TW',
        learningResourceType: 'Curriculum',
        educationalLevel: 'Beginner to Advanced',
        teaches: 'AI Agent / LLM / Claude Code / MCP / RAG / multi-agent / Agentic-RL',
        license: 'https://opensource.org/licenses/MIT',
        hasCourseInstance: {
          '@type': 'CourseInstance',
          courseMode: 'Online',
          courseWorkload: 'P60H', // approx 60 hours
        },
      }
      pageData.frontmatter.head.push(
        ['script', { type: 'application/ld+json' }, JSON.stringify(ldCourse)],
      )
    } else {
      // BreadcrumbList JSON-LD for non-home pages — Google SERP rich breadcrumbs
      const segments = rel.replace(/\/$/, '').split('/').filter(Boolean)
      const items = [{ '@type': 'ListItem', position: 1, name: 'AgentZ', item: base }]
      let acc = ''
      segments.forEach((seg, i) => {
        acc += (acc ? '/' : '') + seg
        items.push({
          '@type': 'ListItem',
          position: i + 2,
          name: decodeURIComponent(seg).replace(/-/g, ' '),
          item: base + acc + (rel.endsWith('/') && i === segments.length - 1 ? '/' : ''),
        })
      })
      const ldBreadcrumbs = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: items,
      }
      pageData.frontmatter.head.push(
        ['script', { type: 'application/ld+json' }, JSON.stringify(ldBreadcrumbs)],
      )
    }
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'AgentZ',

    nav: [
      { text: '首頁', link: '/' },
      { text: '5 分鐘 Quick Win', link: '/quickwin' },
      { text: '課程地圖', link: '/roadmap' },
      { text: '章節', link: '/chapters/ch-1_zero_basics/' },
      {
        text: '工具箱',
        items: [
          { text: '速查卡 總覽', link: '/cheatsheet' },
          { text: '— CLI / Git', link: '/cheatsheet/cli' },
          { text: '— SDK', link: '/cheatsheet/sdk' },
          { text: '— Pricing', link: '/cheatsheet/pricing' },
          { text: '— Patterns', link: '/cheatsheet/patterns' },
          { text: '— MCP / Skills', link: '/cheatsheet/mcp' },
          { text: '— Governance', link: '/cheatsheet/governance' },
          { text: '故障排除', link: '/troubleshooting' },
          { text: '名詞表 總覽', link: '/glossary' },
          { text: '— 基礎 (LLM/Prompt)', link: '/glossary/foundation' },
          { text: '— Agent + CLI / Claude Code', link: '/glossary/agent' },
          { text: '— 實務 (Memory/RAG)', link: '/glossary/practice' },
          { text: '— Production', link: '/glossary/production' },
          { text: '— 台灣 AI / pair', link: '/glossary/taiwan-misc' },
          { text: 'LLM / API 申請 總覽', link: '/llm-providers' },
          { text: '— 商業 API (Claude/GPT/Gemini)', link: '/llm-providers/commercial' },
          { text: '— 開源/聚合 (Groq/DeepSeek/Mistral/OpenRouter/Grok)', link: '/llm-providers/opensource-aggregator' },
          { text: '— 本地/主權 (Ollama/TAIDE/Qwen)', link: '/llm-providers/local-sovereign' },
          { text: 'FAQ', link: '/faq' },
          { text: '跟其他教程比較', link: '/compare' },
        ],
      },
      {
        text: '進度 & 社群',
        items: [
          { text: '進度檢核', link: '/progress' },
          { text: 'Capstone Gallery', link: '/capstone' },
          { text: '更新紀錄', link: '/whatsnew' },
          { text: '關於 AgentZ', link: '/about' },
        ],
      },
      { text: 'GitHub', link: 'https://github.com/symbiosis11503/agent-z' },
    ],

    sidebar: {
      '/cheatsheet/': [
        {
          text: '速查卡 6 個分頁',
          collapsed: false,
          items: [
            { text: '🏠 總覽 / 索引', link: '/cheatsheet' },
            { text: '📟 CLI / Git', link: '/cheatsheet/cli' },
            { text: '🧪 SDK', link: '/cheatsheet/sdk' },
            { text: '💰 Pricing', link: '/cheatsheet/pricing' },
            { text: '🔁 Patterns', link: '/cheatsheet/patterns' },
            { text: '🧩 MCP / Skills', link: '/cheatsheet/mcp' },
            { text: '🛡 Governance', link: '/cheatsheet/governance' },
          ],
        },
        {
          text: '列印',
          collapsed: false,
          items: [
            { text: '📄 全本一頁 (A4 印)', link: '/cheatsheet/all' },
          ],
        },
      ],
      '/glossary/': [
        {
          text: '名詞表 5 個分類',
          collapsed: false,
          items: [
            { text: '🏠 總覽 / 索引', link: '/glossary' },
            { text: '🧠 基礎 (LLM/Prompt)', link: '/glossary/foundation' },
            { text: '🤖 Agent + CLI / Claude Code', link: '/glossary/agent' },
            { text: '🛠 實務 (Memory/RAG)', link: '/glossary/practice' },
            { text: '🛡 Production', link: '/glossary/production' },
            { text: '🇹🇼 台灣 AI / pair', link: '/glossary/taiwan-misc' },
          ],
        },
        {
          text: 'Ctrl-F 搜尋',
          collapsed: false,
          items: [
            { text: '📄 全本一頁', link: '/glossary/all' },
          ],
        },
      ],
      '/llm-providers/': [
        {
          text: 'LLM / API 申請 3 個分類',
          collapsed: false,
          items: [
            { text: '🏠 總覽 / 比較表', link: '/llm-providers' },
            { text: '💳 商業 API (Claude/GPT/Gemini)', link: '/llm-providers/commercial' },
            { text: '⚡ 開源/聚合/速度/便宜', link: '/llm-providers/opensource-aggregator' },
            { text: '🏠 本地/主權/中文圈', link: '/llm-providers/local-sovereign' },
          ],
        },
        {
          text: 'Ctrl-F 搜尋',
          collapsed: false,
          items: [
            { text: '📄 全本一頁', link: '/llm-providers/all' },
          ],
        },
      ],
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
