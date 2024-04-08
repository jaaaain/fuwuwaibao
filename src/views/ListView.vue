<template>
    <div>
        <app-header></app-header>
        <div class="main-list">
            <div class="list-container">
                <el-card class="box-card" v-for="(item, index) in displayedItems" :key="index"
                    @click.native="toItemDetail(item)">
                    <img
                        src="https://gd-hbimg.huaban.com/e40d922474425c9ffae8f36e2f2495078ea6905b13c2-okJiuY_fw1200webp">
                    <div class="item">
                        <div class="label">参保个体 {{ item['个人编码'] }}</div>
                        <span class="data">本次审批金额: {{ item['本次审批金额_SUM'] }} 元</span>
                        <span class="data">是否挂号: {{ item['是否挂号'] === 1 ? '是' : '否' }}</span>
                        <br />
                        <span class="data">是否民政救助: {{ item['BZ_民政救助'] === 1 ? '是' : '否' }}</span>
                        <span class="data">是否城乡优抚: {{ item['BZ_城乡优抚'] === 1 ? '是' : '否' }}</span>
                        <br>
                        <span class="data">月就诊次数: {{ item['月就诊次数_MAX'] }} 次</span>
                    </div>
                </el-card>
            </div>
            <div class="select">
                <el-input placeholder="请输入搜索编码" v-model="search" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
                </el-input>
            </div>

        </div>
        <el-pagination small layout="prev, pager, next" :page-size="pageSize" :total=filteredItems.length
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

::v-deep .el-pagination {
    position: fixed;
    bottom: 0;
    right: 80px;
    margin: 10px auto;
}

.text {
    font-size: 14px;
}

.item {
    display: block;
}

.item .label {
    font-size: large;
    padding-bottom: 9px;
}

.item .data {
    font-size: small;
    padding: 0 30px 8px 10px;
    display: inline-block;
}

.el-card__body img {
    height: 110px;
    margin-right: 21px;
    opacity: 0.4;
    /* float: left; */
}

/* ==================== */
.main-list {
    display: flex;
    margin: 0 10%;
}

.list-container {
    position: relative;
    top: 80px;
    width: 80%;
}

.box-card {
    float: left;
    width: 80%;
    height: 150px;
    display: block;
    margin: 10px auto;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: none;
}

::v-deep .el-card__body {
    display: flex;
}

.select {
    position: absolute;
    top: 80px;
    right: 100px;
    width: 25%;
    min-width: 180px;
    height: 150px;
    display: block;
    margin: 10px auto;
}
</style>
<script>
import axios from 'axios';
//这里导入其他文件
export default {
    //引入的组件注入到对象中才能使用
    components: {},
    props: {},
    data() {
        return {
            sumList: [],
            searchKeyword: '',
            pageSize: 15,
            currentPage: 1,
            search: '',
        };
    },
    methods: {
        handleSearch() {
            this.searchKeyword = this.search;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        },
        toItemDetail(item) {
            const personalCode = item['个人编码'];
            // 根据个人编码获取特定数据，这里假设从 sumList 中获取
            const specificData = this.sumList.find(data => data['个人编码'] === personalCode);
            // 存储特定数据到本地存储
            localStorage.setItem('specificData', JSON.stringify(specificData));
            // 导航到新路由
            this.$router.push(`list/item/${personalCode}`);
        },
    },//方法集合
    mounted() {
        axios.get('http://127.0.0.1:5000/sum_show')
            .then(Response => {
                this.sumList = Response.data.sum_show;
                console.log(this.sumList);
            })
            .catch(error => {
                console.log("error:", error);
            });
    },
    computed: {
        filteredItems() {
            return this.sumList.filter((item) => {
                return String(item["个人编码"]).includes(this.searchKeyword.trim());
            });

        },
        // 计算当前页需要展示的数据
        displayedItems() {
            const startIndex = (this.currentPage - 1) * this.pageSize;
            return this.filteredItems.slice(startIndex, startIndex + this.pageSize);
        },
    }
};
</script>