<template>
    <el-element>
        <app-header></app-header>
        <div class="main">
            <div class="main-header">
                <p class="tital">LOGO医疗保险欺诈预测系统</p>
                <router-link class="el-icon-close" to="/"></router-link>
            </div>
        </div>
    </el-element>
</template>

<script>
// import axios from "axios";
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  data() {
    return {
      predictList: [],
    };
  },
  methods: { }, //方法集合
  mounted() { }, //生命周期 - 挂载完成
};
</script>
<style scoped></style>