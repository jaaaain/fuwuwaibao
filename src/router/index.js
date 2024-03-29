import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/predict/details",
    name: "detail",
    component: () => import("../views/DetailView.vue"),
  },
  {
    path: "/analise",
    name: "analise",
    component: () => import("../views/AnaliseView.vue"), // 数据分析
  },
  {
    path: "/instruct",
    name: "instruct",
    component: () => import("../views/InstView.vue"), // 说明
  },
  {
    path: "/upload",
    name: "upload",
    component: () => import("../views/UploadView.vue"),
  },
  {
    path: "/predict",
    name: "predict",
    component: () => import("../views/PredictView.vue"),
  },
  {
    path: "/list",
    name: "list",
    component: () => import("../views/ListView.vue"),
  },
  {
    path: "/item",
    name: "item",
    component: () => import("../views/ItemView.vue"),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
