import DefaultTheme from 'vitepress/theme'
import './custom.css'
import ProgressTracker from '../components/ProgressTracker.vue'
import LLMTryout from '../components/LLMTryout.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ProgressTracker', ProgressTracker)
    app.component('LLMTryout', LLMTryout)
  },
}
