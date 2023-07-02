import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './services/store'

import { BootstrapVue} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/main.css'

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app')

Vue.use(BootstrapVue);