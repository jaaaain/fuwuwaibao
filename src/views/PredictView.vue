<template>
  <el-element>
    <app-header></app-header>
    <div class="main">
      <div class="main-header">
        <p class="tital">LOGO医疗保险欺诈预测系统</p>
        <router-link class="el-icon-close" to="/"></router-link>
      </div>
      <div class="container">
        <p>上传成功，共 {{ predictList.length }} 条数据</p>
        <table id="predictTable" :data="predictData">
          <thead>
            <tr>
              <th>ID</th>
              <th>是否欺诈</th>
              <th>就诊次数</th>
              <th>统筹金</th>
            </tr>
          </thead>
          <tbody id="predictList">
            <tr v-for="(item, index) in filteredPredictList" :key="index">
              <td>{{ index }}</td>
              <td>{{ item['RES'] === 1 ? '是' : '否' }}</td>
              <td>{{ item['就诊次数_SUM']}}</td>
              <td>{{ item['本次审批金额_SUM'] }}</td>
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
    downloadFile(){
      this.downloading = true; // 设置下载状态为true
      axios({
        url: 'http://localhost:5000/download-file', // 后端提供的下载文件路由
        method: 'GET',
      }).then(response => {
        const coder = Uint8Array.from(atob(response.data.file_content), c => c.charCodeAt(0));
        const decoder = new TextDecoder('utf-8');
        const fileContent = decoder.decode(coder);
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
  },
  mounted() {
    axios.get('http://127.0.0.1:5000/result ')
      .then(response => {
        this.predictList = response.data.sum_result;
        console.log(this.predictList);
      })
      .catch(error => {
        console.log("Error fetching data:", error);
      });
  },
  computed: {
    filteredPredictList() {
      return this.predictList.slice(0, 6); // 返回前五个元素
    }
  }
};
</script>

<style scoped>
.loading {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
}
</style>
