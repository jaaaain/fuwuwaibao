<template>
  <header>
    <el-header class="header">
      <router-link to="/" class="logo">logo</router-link>
      <ul class="navigation">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/list">骗保详情</router-link></li>
        <li><router-link to="/analise">数据分析</router-link></li>
        <li><router-link to="/instruct">使用说明</router-link></li>
      </ul>
    </el-header>
  </header>
</template>

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
  mounted() {}, //生命周期 - 挂载完成
};
</script>
<style scoped></style>
