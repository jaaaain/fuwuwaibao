<template>
    <div class="block">
        <table id="preTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>个人支付</th>
                    <th>欺诈金额</th>
                    <th>欺诈程度</th>
                </tr>
            </thead>
            <tbody id="pre-predictList">
                <tr v-for="(item, index) in displayedPredList" :key="index">
                    <td>{{index}}</td>
                    <td>{{ item['个人账户金额_SUM'] }}</td>
                    <td>{{ item['统筹支付金额_SUM'] }}</td>
                    <td>{{ getLevel(item['统筹支付金额_SUM']) }}</td>
                </tr>
            </tbody>
        </table>
        <el-pagination layout="prev, pager, next" :page-size="pageSize" :total=filteredItems.length
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
    name: 'prePredictView',
    components: {},
    props: ["searchKeyword"],
    data() {
        return {
            predictList: [],
            pageSize: 6,
            currentPage: 1
        };
    },
    methods: {
        handleCurrentChange(val) {
            this.currentPage = val;
        },
        getLevel(acount) {
            if (acount >= 0 && acount <= 5000) {
                return '低金额';
            } else if (acount > 5000 && acount < 10000) {
                return '中风险';
            } else {
                return '高风险';
            }
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
        prePredictList() {
            return this.predictList.filter(item => item.RES === 1);
        },
        // 计算当前页需要展示的数据
        displayedPredList() {
            const startIndex = (this.currentPage - 1) * this.pageSize;
            return this.filteredItems.slice(startIndex, startIndex + this.pageSize);
        },
        filteredItems() {
            return this.prePredictList.filter((item) => {
                return String(item["个人编码"]).includes(this.searchKeyword.trim());
            });
        },
    }
};
</script>