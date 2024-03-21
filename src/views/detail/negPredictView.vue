<template>
    <div class="block">
        <table id="negTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>风险预期</th>
                    <th>风险等级</th>
                </tr>
            </thead>
            <tbody id="neg-predictList">
                <tr v-for="(item, index) in displayedPredList" :key="index">
                      <td>{{index}}</td>
                      <td>{{ item.RES}}</td>
                      <td>{{ item['个人编码'] }}</td>
                </tr>
            </tbody>
        </table>
        <el-pagination layout="prev, pager, next" :page-size="pageSize" :total=negPredictList.length
            @current-change="handleCurrentChange">
        </el-pagination>
    </div>
</template>

<style scoped>
/* 设置分页器按钮的颜色 */
::v-deep .el-pagination .btn-prev,
::v-deep .el-pagination .btn-next,
::v-deep .el-pagination .number:not(.active) {
    color: white;
    background-color: transparent;
}

/* 设置当前页码按钮的颜色 */
::v-deep .el-pagination .number.active {
    color: greenyellow;
    background-color: transparent;
}
</style>
<script>
import axios from 'axios';
//这里导入其他文件
export default {
    //引入的组件注入到对象中才能使用
    name: 'negPredictView',
    components: {},
    props: {},
    data() {
        return {
            predictList: [],
            searchKeyword: '',
            pageSize: 6,
            currentPage: 1
        };
    },
    methods: {
        handleCurrentChange(val) {
            this.currentPage = val;
        }
    },//方法集合
    mounted() {
        axios.get('http://127.0.0.1:5000/result')
            .then(Response => {
                this.predictList = Response.data.sum_result;
                console.log(this.predictList);
            })
            .catch(error => {
                console.log("error:", error);
            });
    },//生命周期 - 挂载完成
    computed: {
        negPredictList() {
            return this.predictList.filter(item => item.RES === 0);
        },
        // 计算当前页需要展示的数据
        displayedPredList() {
            const startIndex = (this.currentPage - 1) * this.pageSize;
            return this.negPredictList.slice(startIndex, startIndex + this.pageSize);
        }
    }
};
</script>
<style scoped></style>