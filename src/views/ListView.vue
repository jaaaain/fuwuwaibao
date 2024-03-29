<template>
    <div>
        <app-header></app-header>
        <div class="main-list">
            <div class="list-container">
                <el-card class="box-card" v-for="(item, index) in displayedItems" :key="index">
                    <div slot="header" class="clearfix">
                        <span>{{ item['个人编码'] }}</span>
                        <router-link to="/item" style="float: right; padding: 3px 0; color: #4caf50;">查看详情</router-link>
                    </div>
                    <div>{{ item }}</div>
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
::v-deep .el-pagination{
    position: fixed;
    bottom: 0;
    right: 80px;
    margin: 10px auto;
}
.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both
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
    background-color: transparent;
    color: white;
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
            predictList: [],
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
        }
    },//方法集合
    mounted() {
        axios.get('http://127.0.0.1:5000/sum_show')
            .then(Response => {
                this.predictList = Response.data.sum_show;
                console.log(this.predictList);
            })
            .catch(error => {
                console.log("error:", error);
            });
    },
    computed: {
        filteredItems() {
            return this.predictList.filter((item) => {
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