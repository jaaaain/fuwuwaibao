<template>
  <el-container>
    <app-header></app-header>
    <div class="chart-container">
      <div class="chart" id="Chart1"></div>
      <div class="chart" id="Chart2"></div>
      <div class="chart" id="Chart3"></div>
    </div>
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
      sumList: [],
      count0: 0,
      count1: 0
    };
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:5000/sum_show')
            .then(Response => {
                this.sumList = Response.data.sum_show;
                console.log(this.sumList);
                this.renderChart();
            })
            .catch(error => {
                console.log("error:", error);
            });

    },
    renderChart() {
      this.handleChart1();
      this.handleChart2();
      this.handleChart3();
    },
    handleChart1() {
      // 初始化 ECharts 实例
      const chartInstance = echarts.init(document.getElementById("Chart1"));
      // 计算 0 和 1 的数量
      this.count0 = this.sumList.filter(item => item.RES === 0).length;
      this.count1 = this.sumList.filter(item => item.RES === 1).length;
      console.log(this.count0);
      console.log(this.count1);
      // 设置图表配置
      const options = {
        title: {
          text: '骗保占比',
          x: 'center',
          textStyle: {
            fontSize: 18,
            color: 'white'
          },
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'  // 提示框内容格式
        },
        color: ['#ff7f50', '#87cefa'],
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: this.count0, name: '非骗保' },
              { value: this.count1, name: '骗保' }
            ]
          }
        ]
      };
      // 使用 chartInstance 渲染图表
      chartInstance.setOption(options); // 设置图表配置
    },
    handleChart2() {
      var myChart = echarts.init(document.getElementById("Chart2"));
      // 定义一个对象，用于存储各种大小数据的数量统计
      // 统计审批金额在1000到2000之间的数据数量
      this.count00000to10000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 0 && item['本次审批金额_SUM'] < 10000).length;
      this.count10000to20000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 10000 && item['本次审批金额_SUM'] < 20000).length;
      this.count20000to30000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 20000 && item['本次审批金额_SUM'] < 30000).length;
      this.count30000to = this.sumList.filter(item => item['本次审批金额_SUM'] >= 30000).length;
      var option = {
        title: {
          text: '审批金额分析',
          textStyle: {
            fontSize: 18,
            color: 'white'
          },
          padding: [10, 0, 100, 100]  //设置标题位置，用padding属性来定位
        },
        legend: {  //配置图例
          type: 'scroll',
          top: '1%',
          textStyle: {
            color: 'white',
          },
          data: [
            {
              name: '数量',
              icon: 'circle',  //图例样式
            }
          ],
        },
        tooltip: {  //提示框
          trigger: 'item',  //设置数据项图形触发
          axisPointer: {  //设置指示样式
            type: 'shadow',
            axis: 'auto',
          },
          padding: 5,
          textStyle: {  //设置提示框内容样式
            color: "green",
          },
        },
        xAxis: {
          offset: 10,
          name: '数值',
          nameGap: 15,
          type: 'category',  // 指定 x 轴的类型为类目型
          axisLabel: {
            interval: 0,  // 强制显示所有标签
            rotate: 30     // 旋转角度
          },
          data: ['0~10000', '10000~20000', '20000~30000', '30000~']
        },
        yAxis: {  //y轴
          type: 'value',
          offset: 1,  //偏移
          name: '数量',
          nameGap: 15,  //名称与轴线的距离
          axisLine: {
            show: true,
            symbol: ['none', 'arrow'],  //显示箭头
            symbolSize: [8, 8],  //箭头大小
            symbolOffset: [0, 7],  //箭头位置
          },
          splitLine: {  //分隔线
            lineStyle: {
              color: '#666',
              type: 'dashed',  //类型
            },
          },
        },
        series: [{
          type: 'bar',
          legendHoverLink: true,  //设置系列是否启用图例hover时的联动高亮
          label: {  //文本标签
            show: false,
          },
          itemStyle: {
            color: 'green',
            barBorderRadius: [5, 5, 0, 0],
          },
          barWidth: '10',  //宽度
          barCategoryGap: '20%',  //间距
          data: [this.count00000to10000,this.count10000to20000,this.count20000to30000,this.count30000to]
        }]
      };
      myChart.setOption(option);
    },
    handleChart3() {

    },
  },//方法集合
  mounted() {
    this.fetchData();
  },//生命周期 - 挂载完成
};
</script>
<style scoped>
.chart-container {
  position: relative;
  top: 80px;
  margin: 0 5%;
  width: 100%;
  height: 100%;
  color: white;
  display: flex;
  justify-content: space-between;
}

.chart {
  width: 33%;
  height: 500px;
}
</style>