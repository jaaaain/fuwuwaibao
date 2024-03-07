<template>
  <el-container>
    <app-header></app-header>
    <el-main class="main-tital">
      <div class="tital">
        <div class="big_tital">
          <h1>医疗保险欺诈预测系统</h1>
        </div>
        <div class="small_tital">
          <p>基于机器学习的医疗保险欺诈预测系统</p>
        </div>
      </div>
      <form action="get/post">
        <ul class="button-box">
          <li><button class="button">下载模板</button></li>
          <li><router-link to="./upload" class="button">开始预测</router-link></li>
        </ul>
      </form>
    </el-main>
    <el-footer class="footer">
      <p>@2023-2024反诈小队</p>
    </el-footer>
  </el-container>
</template>

<script>
import axios from "axios";
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  components: {},
  props: {},
  data() {
    return {};
  },
  methods: {}, //方法集合
  mounted() {
    axios
      .get("https://mock.apifox.cn/m1/3128855-0-default/emp/list")
      .then((result) => {
        this.tableData = result.data.data;
      });
  }, //生命周期 - 挂载完成
};
</script>
<style scoped></style>
