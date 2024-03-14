<template>
  <el-element>
    <app-header></app-header>
    <div class="main">
      <div class="main-header">
        <p class="title">LOGO医疗保险欺诈预测系统</p>
        <router-link class="el-icon-close" to="/"></router-link>
      </div>
      <div class="container">
        <table id="predictTable" :data="predictData">
          <thead>
            <tr>
              <th>ID</th>
              <th>预测结果</th>
              <th>正向概率</th>
              <th>负向概率</th>
            </tr>
          </thead>
          <tbody id="predictList">
            <tr v-for="(item, index) in predictList.value" :key="index">
              <td>{{index}}</td>
              <td>{{ item.res}}</td>
              <td>{{ item['个人编码'] }}</td>
              <td>{{ item['负向概率'] }}</td>
            </tr>
          </tbody>
        </table>
        <div class="button-box">
          <button class="button" id="downloadButton" @click="downloadFile">下载结果</button>
          <router-link to="/predict/details" class="button" id="detailsButton">详细信息</router-link>
        </div>
        <div v-if="downloading" class="loading">正在下载...</div>
      </div>
    </div>
  </el-element>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      predictList: [],
      downloading: false,
    };
  },
  methods: {
    // 下载结果文件
    downloadFile() {
      this.downloading = true; // 设置下载状态为true
      axios({
        url: 'http://localhost:5000/download-file', // 后端提供的下载文件路由
        method: 'GET',
        responseType: 'blob', // 响应类型为二进制流
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'file.txt'); // 下载的文件名
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        this.downloading = false; // 下载完成后将下载状态设为false
      }).catch(error => {
        console.error('Error downloading file:', error);
        this.downloading = false; // 下载出错时也需要将下载状态设为false
      });
    },
    fetchData() { // 获取预测结果数据
      axios.post('http://127.0.0.1:5000/predict_view')
        .then(response => {
          this.predictList.value = response.data.first_eight_rows;
          console.log(this.predictList.value);
        })
        .catch(error => {
          console.log("Error fetching data:", error);
        });
    },
  },
  mounted() {
    this.fetchData(); // 获取数据
  },
};
</script>

<style scoped>
.loading {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
}
</style>
