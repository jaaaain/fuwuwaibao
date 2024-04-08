<template>
  <el-element>
    <app-header></app-header>
    <div class="main">
      <div class="main-header">
        <p class="tital">LOGO医疗保险欺诈预测系统</p>
        <router-link class="el-icon-close" to="/"></router-link>
      </div>
      <div class="container">
        <el-tabs v-model="activeName" @tab-click="handleClick" class="tabs">
          <el-tab-pane label="骗 保" name="first">
            <pre-predict-view :searchKeyword="searchKeyword"></pre-predict-view>
          </el-tab-pane>
          <el-tab-pane label="非骗保" name="second">
            <neg-predict-view :searchKeyword="searchKeyword"></neg-predict-view>
          </el-tab-pane>
        </el-tabs>
        <el-input placeholder="请输入内容" v-model="search" class="input-with-select">
          <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
        </el-input>
      </div>
    </div>
  </el-element>
</template>
<script>
import prePredictView from './detail/prePredictView.vue';
import negPredictView from './detail/negPredictView.vue';
//这里导入其他文件
export default {
  components: { prePredictView, negPredictView },
  //引入的组件注入到对象中才能使用
  data() {
    return {
      activeName: 'first',
      searchKeyword: '',
      search: '',
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    handleSearch() {
      this.searchKeyword = this.search;
      console.log(this.searchKeyword);
    }
  },//方法集合,
};
</script>
<style scoped>
/*去下划线 */
::v-deep .el-tabs__nav-wrap::after {
  position: static !important;
}

/* 下划线颜色 */
::v-deep .el-tabs__active-bar {
  background-color: greenyellow;
}

::v-deep .el-tabs__item {
  color: white;
  opacity: 0.5;
}

::v-deep .el-tabs__item:hover {
  color: rgb(57, 160, 57);
  cursor: pointer;
  opacity: 1;
}

::v-deep .el-tabs__item.is-active {
  color: greenyellow;
  opacity: 1;
}

::v-deep .el-tabs__nav-wrap {
  width: 40%;
}

.container {
  position: relative;
}

.input-with-select {
  position: absolute;
  top: 4px;
  right: 10px;
  width: 60%;

}

.el-select {
  width: 90px;
}
</style>