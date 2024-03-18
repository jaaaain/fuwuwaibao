import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () =>
      import('../views/HomeView.vue'),
  },
  {
    path: "/list",
    redirect: "/predict/details"
  },
  {
    path: "/predict/details",
    name: "detail",
    component: () =>
      import('../views/DetailView.vue'),
  },
  {
    path: "/analise",
    name: "analise",
    component: () =>
      import('../views/AnaliseView.vue'),
  },
  {
    path: "/instruct",
    name: "instruct",
    component: () =>
      import('../views/InstView.vue'),
  },
  {
    path: "/upload",
    name: "upload",
    component: () =>
      import('../views/UploadView.vue'),
  },
  {
    path: "/predict",
    name: "predict",
    component: () =>
      import('../views/PredictView.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
