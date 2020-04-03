import Vue from 'vue'
import store from './store.js'
import App from './App.vue'

import echarts from 'echarts'
import 'echarts-wordcloud'
Vue.prototype.$echarts = echarts

import 'element-ui/lib/theme-chalk/index.css';
import 'maptalks/dist/maptalks.css';
import ElementUI from 'element-ui';
Vue.use(ElementUI);


import LightTimeline from 'vue-light-timeline';
Vue.use(LightTimeline);

import router from './router.js';
Vue.config.productionTip = false
new Vue({
  el: '#app',
  router,
store,
  render(h){
    return h(App);
  }
})