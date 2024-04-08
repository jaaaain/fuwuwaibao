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
                    <td>{{ item['个人编码'] }}</td>
                    <td>{{ riskPercentage(item['risk']) }}</td>
                    <td>{{ getRiskLevel(item['risk']) }}</td>
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
    name: 'negPredictView',
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
        riskPercentage(value) {
            if (typeof value !== 'number') {
                return '';
            }
            return (value * 100).toFixed(2) + '%';
        },
        getRiskLevel(risk) {
            if (risk >= 0 && risk <= 0.3) {
                return '低风险';
            } else if (risk > 0.3 && risk < 0.6) {
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
        negPredictList() {
            return this.predictList.filter(item => item.RES === 0);
        },
        // 计算当前页需要展示的数据
        displayedPredList() {
            const startIndex = (this.currentPage - 1) * this.pageSize;
            return this.filteredItems.slice(startIndex, startIndex + this.pageSize);
        },
        filteredItems() {
            // 根据参数进行过滤
            return this.negPredictList.filter((item) => {
                return String(item["个人编码"]).includes(this.searchKeyword.trim());
            });
        },
    }
};
</script>
<style scoped></style>