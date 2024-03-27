<template>
    <div>
        <app-header></app-header>
        <div class="main-list">
            <div class="list-container">
                <el-card class="box-card" v-for="(item, index) in displayedPredList" :key="index">
                    <div slot="header" class="clearfix">
                        <span>{{ item['个人编码'] }}</span>
                        <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
                        {{ index }}
                    </div>

                    <!-- <div v-for="o in 4" :key="o" class="text item">
                {{ '列表内容 ' + o }}
            </div> -->
                </el-card>
            </div>
            <div class="select">

                <el-input placeholder="请输入内容" v-model="searchKeyword" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search"></el-button>
                </el-input>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* .text {
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
} */
.main-list {
    display: flex;
    margin: 0 10%;
}
.list-container {
    position: relative;
    top: 80px;
}

.box-card {
    float: left;
    width: 90%;
    height: 150px;
    display: block;
    margin: 10px auto;
    background-color: transparent;
    color: white;
}

.select {
    float: right;
    position: relative;
    top: 80px;
    width: 30%;
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
            pageSize: 6,
            currentPage: 1,
            select: ''
        };
    },
    methods: {

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
    },//生命周期 - 挂载完成
    computed: {
        itemList() {
            return this.predictList;
        },
        // 计算当前页需要展示的数据
        displayedPredList() {
            const startIndex = (this.currentPage - 1) * this.pageSize;
            return this.itemList.slice(startIndex, startIndex + this.pageSize);
        }
    }
};
</script>