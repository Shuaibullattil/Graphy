import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Global configuration
app.config.globalProperties.$config = {
  apiBaseUrl: import.meta.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'
}

app.mount('#app')
