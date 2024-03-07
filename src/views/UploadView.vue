<template>
  <el-container>
    <app-header></app-header>
    <div class="main">
      <div class="main-header">
        <p class="tital">LOGO医疗保险欺诈预测系统</p>
        <router-link class="el-icon-close" to="/"></router-link>
      </div>
      <div class="container">
        <table id="fileTable" :data="tableData">
          <thead>
            <tr>
              <th>文件名称</th>
              <th>文件类型</th>
              <th>文件大小</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody id="fileList">
            <tr v-for="(file, index) in fileList" :key="index">
              <td>{{ file.name }}</td>
              <td>{{ file.type }}</td>
              <td>{{ file.size }}</td>
              <td><button @click="deleteFile(index)">删除</button></td>
            </tr>
          </tbody>
        </table>
        <div class="button-box">
          <input type="file" @change="handleFileUpload" id="fileInput" />
          <label for="fileInput" class="button" id="button3">选择文件</label>
          <button @click="uploadFiles" class="button" id="button4">开始上传</button>
        </div>
      </div>
    </div>
  </el-container>
</template>

<script>
import axios from "axios";
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  data() {
    return {
      fileList: [],
    };
  },
  methods: {
    // 文件上传处理方法
    handleFileUpload(event) {
      const files = event.target.files;
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        // 上传成功后添加文件信息到表格数据中
        const fileInfo = {
          name: file.name,
          type: file.type,
          size: file.size,
        };
        this.fileList.push(fileInfo);
      }
    },
    // 删除文件
    deleteFile(index) {
      this.fileList.splice(index, 1);
    },
    // 上传文件
    uploadFiles() {
      if (this.fileList.length == 0) {
        alert("文件为空，请选择要上传的文件");
      } else {
        const formData = new FormData();
        let flag = true;
        for (let i = 0; i < this.fileList.length; i++) {
          const file = this.fileList[i];
          if (file.type != 'text/csv') {
            flag = false;
            alert("文件类型错误，请重新选择文件");
            break;
          } else {
            formData.append('files', file);
            console.log(formData);
          }
        }
        if (flag) {
          // 发送文件上传请求
          axios.post('/data', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }).then(response => {
            console.log('文件上传成功' + response);
          }).catch(error => {
            console.error('文件上传失败：', error);
          })

        }
      }

    }
  }, //方法集合
  mounted() { }, //生命周期 - 挂载完成
};
</script>

<style scoped></style>
