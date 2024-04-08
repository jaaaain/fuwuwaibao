<template>
  <div>
    <app-header></app-header>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/list' }">医保列表</el-breadcrumb-item>
      <el-breadcrumb-item>参保人员 {{ personalCode }}</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="item-container">
      <div class="data-container">
        <div class="item-data">
          <img src="https://gd-hbimg.huaban.com/e40d922474425c9ffae8f36e2f2495078ea6905b13c2-okJiuY_fw1200webp">
          <div class="item">
            <div class="label">参保个体 {{ itemData['个人编码'] }}</div>
            <span class="data">本次审批金额: {{ itemData['本次审批金额_SUM'] }} 元</span>
            <span class="data">是否挂号: {{ itemData['是否挂号'] === 1 ? '是' : '否' }}</span>
            <br>
            <span class="data">是否民政救助: {{ itemData['BZ_民政救助'] === 1 ? '是' : '否' }}</span>
            <span class="data">是否城乡优抚: {{ itemData['BZ_城乡优抚'] === 1 ? '是' : '否' }}</span>
            <br>
            <span class="data">月就诊次数: {{ itemData['月就诊次数_MAX'] }} 次</span>

          </div>
        </div>
        <div class="item-data">
          <span class="data">月就诊天数MAX: {{ itemData['月就诊天数_MAX'] }}</span>
          <span class="data">月就诊天数AVG: {{ itemData['月就诊天数_AVG'] }}</span>
          <br><br>
          <span class="data">月就诊医院数MAX: {{ itemData['月就诊医院数_MAX'] }}</span>
          <span class="data">月就诊医院数AVG: {{ itemData['月就诊医院数_AVG'] }}</span>
          <br><br>
          <span class="data">月就诊次数MAX: {{ itemData['月就诊次数_MAX'] }}</span>
          <span class="data">月就诊次数AVG: {{ itemData['月就诊次数_AVG'] }}</span>
        </div>
      </div>
      <div class="data-container">
        <div class="item-data item-table">
          <div class="chart" id="Chart1"></div>
        </div>
        <div class="item-data item-table">
          <div class="chart" id="Chart2"></div>
        </div>
      </div>

    </div>
  </div>
</template>
<style scoped>
.el-breadcrumb {
  padding: 0 10%;
  position: relative;
  top: 80px;
}

.el-breadcrumb ::v-deep .el-breadcrumb__inner.is-link:hover {
  color: #0fae14;
}

.el-breadcrumb ::v-deep .el-breadcrumb__inner {
  color: #5abd62;
  font-weight: 800;
}

.el-breadcrumb__item:last-child ::v-deep .el-breadcrumb__inner {
  color: #0fae14;
  font-weight: 400;
}

.item-container {
  position: relative;
  top: 80px;
  margin: 0 5%;
}

.data-container {
  margin: 20px;
  display: flex;
}

.item-data {
  display: inline-block;
  justify-content: space-between;
  width: 100%;
  height: 146px;
  margin: 10px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 4px;
}

.item-table {
  height: 340px;
}

.item .label {
  font-size: large;
  padding-bottom: 15px;
}

.item-data .item {
  display: inline;
  float: left;
}

.data {
  font-size: small;
  padding: 0 30px 15px 30px;
  display: inline-block;
}

.item-data img {
  /* display: inline; */
  float: left;
  height: 140px;
  margin: 0 50px 0 10px;
  opacity: 0.4;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
<script>
import * as echarts from 'echarts';
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  components: {},
  data() {
    return {
      itemData: {},
      personalCode: 0,
    };
  },
  methods: {
    fetchData() {
      this.personalCode = this.$route.params.personalCode;
      // 根据个人编码从 sessionStorage 中获取对应的数据
      const specificData = JSON.parse(localStorage.getItem('specificData')) || [];
      console.log(specificData)
      this.itemData =specificData
      console.log(this.itemData)
      this.renderChart();
    },
    renderChart() {
      this.handleChart1();
      this.handleChart2();
    },
    handleChart1() {
      var myChart = echarts.init(document.getElementById("Chart1"));
      var option = {
        title: {
          text: '费用支付占比',
          textStyle: {
            fontSize: 18,
            color: 'white'
          },
          padding: [3, 0, 100, 15]  //设置标题位置，用padding属性来定位
        },
        animation: true, // 动态渲染
        graphic: [{
          type: 'text',
          left: '8%',
          top: '15%',
          style: {
            text: '药品费', // 批注文字内容
            fontSize: 20, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '8%',
          top: '50%',
          style: {
            text: '检查费', // 批注文字内容
            fontSize: 20, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
          {
          type: 'text',
          left: '8%',
          top: '85%',
          style: {
            text: '治疗费', // 批注文字内容
            fontSize: 20, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '25%',
          top: '15%',
          style: {
            text: '在总金额中占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '25%',
          top: '50%',
          style: {
            text: '在总金额中占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '25%',
          top: '85%',
          style: {
            text: '在总金额中占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '60%',
          top: '15%',
          style: {
            text: '个人支付占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '60%',
          top: '50%',
          style: {
            text: '个人支付占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        },
        {
          type: 'text',
          left: '60%',
          top: '85%',
          style: {
            text: '个人支付占比：', // 批注文字内容
            fontSize: 14, // 批注文字大小
            fill: 'white' // 批注文字颜色
          }
        }],
        series: [{
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['50%', '15%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['药品在总金额中的占比'] // 数值
          }]
        },
        {
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['83%', '15%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['个人支付的药品占比']// 数值调用
          }]
        },
        {
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['50%', '50%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['检查总费用在总金额占比'] // 数值
          }]
        },
        {
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['83%', '50%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['个人支付检查费用占比'] // 数值
          }]
        },
        {
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['50%', '85%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['治疗费用在总金额占比']// 数值
          }]
        },
        {
          type: 'gauge', // 仪表盘图
          startAngle: 90,
          endAngle: -270,
          min: 0,
          max: 1,
          radius: '28%',
          center: ['83%', '85%'],
          progress: { // 进度环
            roundCap: 'true',
            show: 'true',
            width: 13,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [{ //进度环的渐变色
                  offset: 0, color: '#2ce385' // 0% 处的颜色
                }, {
                  offset: 1, color: '#0fae14' // 100% 处的颜色
                }]
              }
            }
          },
          axisLine: { // 背景环
            roundCap: 'true',
            lineStyle: {
              width: 13,
              color: [[0, '#CCEFDD'], [1, '#CCEFDD']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          detail: {
            color: 'white',
            fontSize: 15,
            offsetCenter: [0, '10%'],
            formatter: function (value) {
              return (value * 100).toFixed(1) + '%';
            }
          },
          data: [{
            value: this.itemData['个人支付治疗费用占比']// 数值

          }]
        }]
      }
      myChart.setOption(option);
    },
    handleChart2() {
      var myChart = echarts.init(document.getElementById("Chart2"));
      var option = {
        title: {
          text: '医疗费用统计',
          textStyle: {
            fontSize: 18,
            color: 'white'
          },
          padding: [3, 0, 100, 15]  //设置标题位置，用padding属性来定位
        },
        legend: {  //配置图例
          type: 'scroll',
          top: '1%',
          textStyle: {
            color: 'white',
          },
          data: ['发生金额', '自费金额', '申报金额'],
        },
        tooltip: {  //提示框
          trigger: 'item',  //设置数据项图形触发
          axisPointer: {  //设置指示样式
            type: 'shadow',
            axis: 'auto',
          },
          padding: 5,
          textStyle: {  //设置提示框内容样式
            color: "grey",
          },
        },
        xAxis: {  //x轴
          offset: 10,  //偏移
          name: '费用类型',
          nameGap: 15,  //名称与轴线的距离
          data: ['药品费',
            '检查费',
            '治疗费',
            '床位费']
        },
        yAxis: {  //y轴
          type: 'value',
          name: '费用',
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
          name: '发生金额',
          type: 'bar',
          legendHoverLink: true,  //设置系列是否启用图例hover时的联动高亮
          label: {  //文本标签
            show: false,
          },
          barWidth: '20',  //宽度
          barCategoryGap: '20%',  //间距
          data: [this.itemData['药品费发生金额_SUM'], this.itemData['检查费发生金额_SUM'], this.itemData['治疗费发生金额_SUM'], this.itemData['床位费发生金额_SUM']],
          itemStyle: {
            color: 'green',
            barBorderRadius: [5, 5, 0, 0],
          },
        },
        {
          name: '自费金额',
          type: 'bar',
          legendHoverLink: true,  //设置系列是否启用图例hover时的联动高亮
          label: {  //文本标签
            show: false,
          },
          barWidth: '20',  //宽度
          barCategoryGap: '20%',  //间距
          data: [this.itemData['药品费自费金额_SUM'], this.itemData['检查费自费金额_SUM'], this.itemData['治疗费自费金额_SUM'], this.itemData['床位费自费金额_SUM']],
          itemStyle: {
            color: '#5abd62',
            barBorderRadius: [5, 5, 0, 0],
          },
        },
        {
          name: '申报金额',
          type: 'bar',
          legendHoverLink: true,  //设置系列是否启用图例hover时的联动高亮
          label: {  //文本标签
            show: false,
          },
          barWidth: '20',  //宽度
          barCategoryGap: '20%',  //间距
          data: [this.itemData['药品费申报金额_SUM'], this.itemData['检查费申报金额_SUM'], this.itemData['治疗费申报金额_SUM'], this.itemData['床位费申报金额_SUM']],
          itemStyle: {
            color: '#0fae14',
            barBorderRadius: [5, 5, 0, 0],
          },
        }]
      };
      myChart.setOption(option);
    },
  },//方法集合
  mounted() {
    this.fetchData();
  },//生命周期 - 挂载完成
};
</script>