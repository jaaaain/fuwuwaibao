<template>
  <header>
    <el-header class="header">
      <router-link to="/" class="logo">logo</router-link>
      <ul class="navigation">
        <li :class="{ 'active': $route.path === '/' }"><router-link to="/">首页</router-link></li>
        <li :class="{ 'active': $route.path === '/predict/details' }"><router-link to="/predict/details">骗保详情</router-link></li>
        <li :class="{ 'active': $route.path === '/analise' }"><router-link to="/analise">数据分析</router-link></li>
        <li :class="{ 'active': $route.path === '/instruct' }"><router-link to="/instruct">使用说明</router-link></li>
      </ul>
    </el-header>
  </header>
</template>

<style>
.navigation a {
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.5);
}
.navigation>li {
    margin: 0 20px;
}
/* 添加下划线样式 */
.navigation li.active a{
  color: white;
  padding-bottom: 6px;
  border-bottom: 3px solid white;
}
</style>

<script>
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  components: {},
  props: {},
  data() {
    return {};
  },
  methods: {}, //方法集合
  mounted() { }, //生命周期 - 挂载完成
};
</script>
<style scoped></style>
