import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from "./store"
// import withTokenAxios from '@/axios/withTokenAxios';
import Vue3Storage from "vue3-storage"

import { library } from '@fortawesome/fontawesome-svg-core'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
/* import specific icons */
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons';
import easySpinner from 'vue-easy-spinner';


/* add icons to the library */
library.add(faUserSecret,fas,fab)

 axios.defaults.baseURL =  import.meta.env.VITE_APP_API
const app = createApp(App)
app.config.globalProperties.axios = axios

app.use(store)
app.use(easySpinner, {
    prefix: 'easy',
  })
app.use(Vue3Storage, { namespace:'pro_", storage: StorageType.Local'})
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router).mount('#app')