import '@/index.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { plugin, defaultConfig, createInput } from '@formkit/vue'
import { genesisIcons } from '@formkit/icons'
import { rootClasses } from '../formkit.theme'
import { Input, Select } from './components/formkit'
import fetchInterceptor from './plugins/fetch-interceptor'

const app = createApp(App)

app.use(router)
app.use(fetchInterceptor)
app.use(
  plugin,
  defaultConfig({
    icons: {
      ...genesisIcons,
    },
    config: {
      rootClasses,
    },
    inputs: {
      text: createInput(Input, {
        props: ['placeholder'],
      }),
      email: createInput(Input, {
        props: ['placeholder'],
      }),
      password: createInput(Input, {
        props: ['placeholder'],
      }),
      select: createInput(Select, {
        props: ['placeholder', 'selectOptions', 'selectLabel'],
      }),
    },
  }),
)
app.mount('#app')
