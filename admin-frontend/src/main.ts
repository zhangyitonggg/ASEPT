import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VuetifyDialog from 'vuetify-dialog'

Vue.config.productionTip = false
import VueParticles from 'vue-particles'
Vue.use(VueParticles)
new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
