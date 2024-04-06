<template>
  <el-container>
    <app-header></app-header>
    <div class="chart-container">
      <div class="chart" id="Chart1" style="position: absolute; top: 20px; left: 20px;"></div>
      <div class="chart" id="Chart2" style="position: absolute; top: 20px; right: 20px;"></div>
      <div class="chart" id="Chart3" style="position: absolute; top: 500px; left: 20px;"></div>
      <div class="chart" id="Chart5" style="position: absolute; top: 500px; right: 20px;"></div>
      <div class="chart" id="Chart4" style="position: absolute; top: 250px; left: 50%; transform: translate(-50%, -50%);"></div>
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
      this.handleChart4();
      this.handleChart5();
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
      // 初始化 ECharts 实例
      const chartInstance = echarts.init(document.getElementById("Chart3"));
      // 计算 低中高风险 的数量
      this.risk1 = this.sumList.filter(item => item.risk >= 0  && item.risk<=0.3).length;
      this.risk2 = this.sumList.filter(item => item.risk >0.3  && item.risk<=0.6).length;
      this.risk3 = this.sumList.filter(item => item.risk >0.6  && item.risk<1).length;
      console.log(this.risk1);
      console.log(this.risk2);
      // 设置图表配置
      const options = {
        title: {
          text: '医保欺诈风险占比',
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
        color: ['#ff7f50', '#87cefa', 'purple'],
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: this.risk1, name: '低风险' },
              { value: this.risk2, name: '中风险' },
              { value: this.risk3, name: '高风险' }
            ]
          }
        ]
      };
      // 使用 chartInstance 渲染图表
      chartInstance.setOption(options); // 设置图表配置

    },
    handleChart4() {
      // 初始化 ECharts 实例
      console.log('读取成功');
      const chartInstance = echarts.init(document.getElementById("Chart4"));
      // 计算欺诈成功的数量
      this.FraudData = this.sumList.filter(item => item.RES === 1);
      console.log(this.FraudData);
      this.count00000to5000 = this.FraudData.filter(item => item['本次审批金额_SUM'] >= 0 && item['本次审批金额_SUM'] < 5000).length;
      this.count5000to10000 = this.FraudData.filter(item => item['本次审批金额_SUM'] >= 5000 && item['本次审批金额_SUM'] < 15000).length;
      this.count10000to15000 = this.FraudData.filter(item => item['本次审批金额_SUM'] >= 10000 && item['本次审批金额_SUM'] < 15000).length;
      this.count15000to20000 = this.FraudData.filter(item => item['本次审批金额_SUM'] >= 15000 && item['本次审批金额_SUM'] < 20000).length;
      this.count20000to = this.FraudData.filter(item => item['本次审批金额_SUM'] >= 20000).length;
      // 在格式化函数外部定义一个变量来存储 this.FraudData
      let fraudData = this.FraudData;
      // 设置图表配置
      const options = {
        title: {
          text: '欺诈金额展示', // 根据需要更改标题
          textStyle: {
            fontSize: 18,
            color: 'white'
          }
        },
        tooltip: {
          trigger: 'item', // 设置触发方式为 item
          formatter: function (params) {
            let totalAmount = 0; // 初始化总金额为 0
            // 在格式化函数内部引用 fraudData 变量
            fraudData.forEach(item => {
              totalAmount += item['本次审批金额_SUM']; // 累加审批金额
            });
            totalAmount = totalAmount.toFixed(0);
            let result = params.name; // 显示维度名称
            for (let i = 0; i < params.value.length; i++) {
              result += '维度' + (i + 1) + '数量：' + params.value[i] + '<br/>'; // 显示当前维度的数量
            }
            result += '欺诈金额总和：' + totalAmount; // 显示欺诈金额的数量总和
            return result;
          }
        },
        radar: {
          indicator: [
            { name: '0000~' },
            { name: '5000~' },
            { name: '10000~' },
            { name: '15000~' },
            { name: '20000~' }
          ],
          center: ['50%', '50%'],
          radius: '60%',
          name: {
            textStyle: {
              color: 'white'
            }
          }
        },
        series: [{
          type: 'radar',
          data: [
          { value: [this.count00000to5000, this.count5000to10000 , this.count10000to15000, this.count15000to20000, this.count20000to] } // 这里是一个对象，包含了五个维度的数据
        ]
        }]
      };
      // 使用 chartInstance 渲染图表
      chartInstance.setOption(options); // 设置图表配置

    },
      handleChart5() {
      // 初始化 ECharts 实例
      console.log('读取成功');
      const chartInstance = echarts.init(document.getElementById("Chart5"));
      this.amountmax = this.sumList.reduce((max, item) => {
        // 检查当前项目的审批金额是否大于已知的最大值
        if (item['本次审批金额_SUM'] > max) {
          return item['本次审批金额_SUM']; // 如果是，则返回当前项目的审批金额作为新的最大值
        } else {
          return max; // 如果不是，则保持已知的最大值不变
        }
      }, 0); // 初始值设为 0
      this.daymax = this.sumList.reduce((max, item) => {
        // 检查当前项目的审批金额是否大于已知的最大值
        if (item['就诊次数_SUM'] > max) {
          return item['就诊次数_SUM']; // 如果是，则返回当前项目的审批金额作为新的最大值
        } else {
          return max; // 如果不是，则保持已知的最大值不变
        }
      }, 0); // 初始值设为 0
      // 计算欺诈成功的数据
      this.FraudData = this.sumList.filter(item => item.RES === 1);
      console.log(this.FraudData);
      this.fraudmax = this.FraudData.reduce((max, item) => {
        // 检查当前项目的审批金额是否大于已知的最大值
        if (item['本次审批金额_SUM'] > max) {
          return item['本次审批金额_SUM']; // 如果是，则返回当前项目的审批金额作为新的最大值
        } else {
          return max; // 如果不是，则保持已知的最大值不变
        }
      }, 0); // 初始值设为 0
      // 在格式化函数外部定义一个变量来存储 this.FraudData
      // 设置图表配置
      const options = {
        title: {
          text: '最大值展示', // 根据需要更改标题
          textStyle: {
            fontSize: 18,
            color: 'white'
          }
        },
        tooltip: {
          trigger: 'axis', // 设置触发方式为 axis
          axisPointer: {
            type: 'shadow' // 设置坐标轴指示器类型为阴影
          },
          formatter: function (params) {
            let result = params[0].name + '<br/>'; // 显示维度名称
            result += params[0].value.toFixed(2); // 显示欺诈金额的数量
            return result;
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: {
          type: 'category',
          data: ['最大统筹金', '最大就诊天数', '最大欺诈金额'], // 设置 y 轴数据
          axisLine: {
            lineStyle: {
              color: 'white' // 设置 y 轴颜色为白色
            }
          },
          axisLabel: {
            color: 'white' // 设置 y 轴标签颜色为白色
          }
        },
        xAxis: {
          type: 'value', // 设置 x 轴类型为数值型
          axisLine: {
            show: false // 隐藏 x 轴线
          },
          axisLabel: {
            show: false // 隐藏 x 轴标签
          },
          splitLine: {
            show: false // 隐藏 x 轴分隔线
          }
        },
        series: [{
          type: 'bar',
          data: [this.amountmax, this.daymax, this.fraudmax], // 设置柱状图数据
          itemStyle: {
            color: '#2ecc71' // 设置柱状图颜色为绿色
          }
        }]
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