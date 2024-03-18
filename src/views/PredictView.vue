<template>
    <el-element>
        <app-header></app-header>
        <div class="main">
            <div class="main-header">
                <p class="tital">LOGO医疗保险欺诈预测系统</p>
                <router-link class="el-icon-close" to="/"></router-link>
            </div>
            <div class="container">
                <p>文件上传成功 ~ ，共 {{ predictList.length }} 条医保数据</p>
                <table id="predictTable">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>预测结果</th>
                            <th>正向概率</th>
                            <th>负向概率</th>
                        </tr>
                    </thead>
                    <tbody id="predictList">
                        <tr v-for="(file, index) in filteredPredictList" :key="index">
                            <td>{{ file.id }}</td>
                            <td>{{ file.pred }}</td>
                            <td>{{ file.pos_rate }}</td>
                            <td>{{ file.neg_rate }}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="button-box">
                    <button class="button" id="button3" @click="downloadFiles">下载结果</button>
                    <router-link to="/predict/details" class="button" id="button4">详细信息</router-link>
                </div>
            </div>
        </div>
    </el-element>
</template>

<script>
import axios from 'axios';

export default {
    //引入的组件注入到对象中才能使用
    data() {
        return {
            predictList: [],
        };
    },
    methods: {
        // 下载结果
        downloadFiles() { }
    }, //方法集合
    mounted() { // 显示数据
        axios.get('http://127.0.0.1:8081/result')
            .then(Response => {
                this.predictList = Response.data;
                console.log(this.predictList);
            })
            .catch(error => {
                console.log("error:", error);
            });
    }, //生命周期 - 挂载完成
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
