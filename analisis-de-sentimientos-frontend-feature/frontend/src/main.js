// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSimpleAlert from "vue-simple-alert";

Vue.use(VueSimpleAlert);
// Intalación de  BootstrapVue
Vue.use(BootstrapVue)
// Instalación de modulo de iconsBootstrap
Vue.use (BootstrapVueIcons)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
