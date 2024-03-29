<template>
  <el-container>
    <app-header></app-header>
    <div class="chart-container" ref="chart"></div>
  </el-container>

</template>
<script>
import * as echarts from 'echarts';
import axios from 'axios';

//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  components: {},
  props: {},
  data() {
    return {
      predictList: [],
      count0: 0,
      count1: 0
    };
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:5000/sum_show')
        .then(Response => {
          this.predictList = Response.data.sum_show;
          console.log(this.predictList);
          this.renderChart();
        })
        .catch(error => {
          console.log("error:", error);
        });
    },
    renderChart() {
      // 初始化 ECharts 实例
      const chartInstance = echarts.init(this.$refs.chart);
      // 计算 0 和 1 的数量
      this.count0 = this.predictList.filter(item => item.RES === 0).length;
      this.count1 = this.predictList.filter(item => item.RES === 1).length;
      console.log(this.count0);
      console.log(this.count1);
      // 设置图表配置
      const options = {
        title: {
          text: '骗保占比',
          x: 'center',
          textStyle: {
            fontSize: 18,
            fontWeight: 'bolder',
            color: 'white'
          },
        },
        color:['#ff7f50','#87cefa'],
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: this.count0, name: '非骗保' },
              { value: this.count1, name: '骗保' }
            ]
          },
          // {
          //   type: 'line',
          //   xAxisIndex: 0,
          //   yAxisIndex: 0,
          //   data: [1,2,3,4,5],
          // }
        ]
      };
      // 使用 chartInstance 渲染图表
      chartInstance.setOption(options); // 设置图表配置
    },
  },//方法集合
  mounted() {
    this.fetchData();
  },//生命周期 - 挂载完成
};
</script>
<style scoped>
.chart-container {
  position: absolute;
  top: 80px;
  color: white;
  width: 400px;
  height: 400px;
}
</style>