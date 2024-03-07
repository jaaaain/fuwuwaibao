import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// 引入ElementUI组件
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "./assets/css/index.css";
import Header from "./components/AppHeader.vue"


Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.component("app-header",Header);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
