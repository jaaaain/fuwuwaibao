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
      <div class="button-box">
        <li><button class="button" @click="DownLoadMode">下载模板</button></li>
        <li><router-link to="./upload" class="button">开始预测</router-link></li>
      </div>
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
    return {
      downloading: false,
    };
  },
  methods: {
    DownLoadMode(){
      this.downloading = true; // 设置下载状态为true
      axios({
        url: 'http://localhost:5000/download', // 后端提供的下载文件路由
        method: 'GET',
      }).then(response => {
        const fileContent = atob(response.data.file_content);
        console.log('解码后的文件内容：', fileContent); // 打印解码后的文件内容
        const fileName = response.data.file_name;
        const blob = new Blob([fileContent], { type: 'application/octet-stream' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        this.downloading = false; // 下载完成后将下载状态设为false
      }).catch(error => {
        console.error('Error downloading file:', error);
        this.downloading = false; // 下载出错时也需要将下载状态设为false
      });
    }
  }, //方法集合
  mounted() {}, //生命周期 - 挂载完成
};
</script>
<style scoped></style>
