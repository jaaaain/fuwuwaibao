<template>
  <el-container>
    <app-header></app-header>
    <div class="chart-container">
      <div class="column" v-for="(column, index) in chartColumns" :key="index">
        <div class="chart-box" v-for="(chart, idx) in column" :key="idx" :class="chart.class">
          <div :id="chart.id"></div>
        </div>
      </div>
    </div>
  </el-container>
</template>

<style scoped>
.chart-container {
  position: relative;
  top: 80px;
  margin: 0 5%;
  width: 90%;
  color: white;
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
}

.chart-box {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 10px;
  height: 350px; /* 默认高度 */
}

.chart-box6 {
  height: 250px; /* 降低高度 */
}

.chart-box4 {
  height: 450px; /* 特殊高度 */
}

#Chart1, #Chart2, #Chart3, #Chart4, #Chart5, #Chart6 {
  width: 100%;
  height: 100%;
}
</style>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  data() {
    return {
      sumList: [],
      lastFraudCount: parseInt(localStorage.getItem('lastFraudCount')) || 0, // 从 localStorage 初始化
      lastNonFraudCount: parseInt(localStorage.getItem('lastNonFraudCount')) || 0, // 从 localStorage 初始化
      lastTotalDrugCost: parseFloat(localStorage.getItem('lastTotalDrugCost')) || 0,
      lastTotalBedCost: parseFloat(localStorage.getItem('lastTotalBedCost')) || 0,
      lastTotalExamCost: parseFloat(localStorage.getItem('lastTotalExamCost')) || 0,
      lastTotalTreatmentCost: parseFloat(localStorage.getItem('lastTotalTreatmentCost')) || 0,
      lastRisk1Count: parseInt(localStorage.getItem('lastRisk1Count')) || 0, // 从 localStorage 初始化
      lastRisk2Count: parseInt(localStorage.getItem('lastRisk2Count')) || 0, // 从 localStorage 初始化
      lastRisk3Count: parseInt(localStorage.getItem('lastRisk3Count')) || 0, // 从 localStorage 初始化
      chartColumns: [
        [
          { id: 'Chart1', class: 'chart-box1' },
          { id: 'Chart3', class: 'chart-box3' }
        ],
        [
          { id: 'Chart6', class: 'chart-box6' },
          { id: 'Chart4', class: 'chart-box4' }
        ],
        [
          { id: 'Chart2', class: 'chart-box2' },
          { id: 'Chart5', class: 'chart-box5' }
        ]
      ]
    };
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:5000/sum_show')
        .then(response => {
          this.sumList = response.data.sum_show;
          this.renderCharts();
        })
        .catch(error => {
          console.log("error:", error);
        });
    },
    renderCharts() {
      const chartConfigs = [
        this.getChart1Options(),
        this.getChart2Options(),
        this.getChart3Options(),
        this.getChart4Options(),
        this.getChart5Options(),
        this.getChart6Options()
      ];

      chartConfigs.forEach((options, idx) => {
        this.renderChart(`Chart${idx + 1}`, options);
      });
    },
    renderChart(chartId, options) {
      const chartElement = document.getElementById(chartId);
      if (chartElement) {
        const chartInstance = echarts.init(chartElement);
        chartInstance.setOption(options);
      }
    },
    getChart1Options() {
      const count0 = this.sumList.filter(item => item.RES === 0).length;
      const count1 = this.sumList.filter(item => item.RES === 1).length;
      const total = count0 + count1;

      const nonFraudPercent = total !== 0 ? (count0 / total * 100).toFixed(2) : 0;
      const fraudPercent = total !== 0 ? (count1 / total * 100).toFixed(2) : 0;

      let fraudChange = '0%';
      let fraudArrow = '↑';

      const lastFraudPercent = parseFloat(localStorage.getItem('lastFraudPercent')) || 0;


      if (lastFraudPercent !== 0) {
        const fraudChangeRate = ((fraudPercent - lastFraudPercent) / lastFraudPercent * 100).toFixed(2);
        fraudChange = `${fraudChangeRate}%`;
        fraudArrow = fraudChangeRate >= 0 ? '↑' : '↓';
      }

      localStorage.setItem('lastFraudPercent', fraudPercent);
      localStorage.setItem('lastNonFraudPercent', nonFraudPercent);

      return {
        title: [
          {
            text: '骗保占比',
            x: 'center',
            textStyle: { fontSize: 18, color: 'white' }
          },
          {
            text: '骗保同比',
            left: '8%',
            top: '50%',
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 16, color: 'white' }
          },
          {
            text: `${fraudChange} ${fraudArrow}`,
            left: '8%',
            top: '60%',
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 16, color: 'white' }
          }
        ],
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        color: ['#ff7f50', '#87cefa'],
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: [
              { value: count0, name: '非骗保' },
              { value: count1, name: '骗保' }
            ],
            label: {
              textStyle: { color: '#aaa' },
              formatter: function (params) {
                return `${params.name}`;
              }
            }
          }
        ]
      };
    },
    getChart2Options() {
      const fraudData = this.sumList.filter(item => item.RES === 1);

      const totalDrugCost = (fraudData.reduce((sum, item) => sum + (item['药品费申报金额_SUM'] || 0), 0) / 10000).toFixed(0);
      const totalBedCost = (fraudData.reduce((sum, item) => sum + (item['床位费申报金额_SUM'] || 0), 0) / 10000).toFixed(0);
      const totalExamCost = (fraudData.reduce((sum, item) => sum + (item['检查费申报金额_SUM'] || 0), 0) / 10000).toFixed(0);
      const totalTreatmentCost = (fraudData.reduce((sum, item) => sum + (item['治疗费申报金额_SUM'] || 0), 0) / 10000).toFixed(0);

      const totalAmount = parseFloat(totalDrugCost) + parseFloat(totalBedCost) + parseFloat(totalExamCost) + parseFloat(totalTreatmentCost);

      const drugPercent = totalAmount !== 0 ? (totalDrugCost / totalAmount * 100).toFixed(2) : 0;
      const bedPercent = totalAmount !== 0 ? (totalBedCost / totalAmount * 100).toFixed(2) : 0;
      const examPercent = totalAmount !== 0 ? (totalExamCost / totalAmount * 100).toFixed(2) : 0;
      const treatmentPercent = totalAmount !== 0 ? (totalTreatmentCost / totalAmount * 100).toFixed(2) : 0;

      let drugChange = '0%';
      let bedChange = '0%';
      let examChange = '0%';
      let treatmentChange = '0%';
      let drugArrow = '↑';
      let bedArrow = '↑';
      let examArrow = '↑';
      let treatmentArrow = '↑';

      const lastDrugPercent = parseFloat(localStorage.getItem('lastDrugPercent')) || 0;
      const lastBedPercent = parseFloat(localStorage.getItem('lastBedPercent')) || 0;
      const lastExamPercent = parseFloat(localStorage.getItem('lastExamPercent')) || 0;
      const lastTreatmentPercent = parseFloat(localStorage.getItem('lastTreatmentPercent')) || 0;

      if (lastDrugPercent !== 0) {
        const drugChangeRate = ((drugPercent - lastDrugPercent) / lastDrugPercent * 100).toFixed(2);
        drugChange = `${drugChangeRate}%`;
        drugArrow = drugChangeRate >= 0 ? '↑' : '↓';
      }
      if (lastBedPercent !== 0) {
        const bedChangeRate = ((bedPercent - lastBedPercent) / lastBedPercent * 100).toFixed(2);
        bedChange = `${bedChangeRate}%`;
        bedArrow = bedChangeRate >= 0 ? '↑' : '↓';
      }
      if (lastExamPercent !== 0) {
        const examChangeRate = ((examPercent - lastExamPercent) / lastExamPercent * 100).toFixed(2);
        examChange = `${examChangeRate}%`;
        examArrow = examChangeRate >= 0 ? '↑' : '↓';
      }
      if (lastTreatmentPercent !== 0) {
        const treatmentChangeRate = ((treatmentPercent - lastTreatmentPercent) / lastTreatmentPercent * 100).toFixed(2);
        treatmentChange = `${treatmentChangeRate}%`;
        treatmentArrow = treatmentChangeRate >= 0 ? '↑' : '↓';
      }

      localStorage.setItem('lastDrugPercent', drugPercent);
      localStorage.setItem('lastBedPercent', bedPercent);
      localStorage.setItem('lastExamPercent', examPercent);
      localStorage.setItem('lastTreatmentPercent', treatmentPercent);

      const data = [
        { name: '药品费', value: totalDrugCost, change: drugChange, arrow: drugArrow },
        { name: '床位费', value: totalBedCost, change: bedChange, arrow: bedArrow },
        { name: '检查费', value: totalExamCost, change: examChange, arrow: examArrow },
        { name: '治疗费', value: totalTreatmentCost, change: treatmentChange, arrow: treatmentArrow }
      ];

      return {
        title: [
          {
            text: '欺诈费用分布',
            x: 'center',
            textStyle: { fontSize: 18, color: 'white' }
          },
        ],
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            const percentage = ((params.value / totalAmount) * 100).toFixed(2);
            return `${params.name}: ${params.value}万 (${percentage}%)`;
          },
          backgroundColor: 'rgba(50, 50, 50, 0.7)', // 背景颜色
          textStyle: { color: '#fff' }, // 文字颜色
          borderWidth: 1,
          borderColor: '#777'
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.name),
          axisLabel: { color: 'white' },
          axisLine: { lineStyle: { color: '#aaa' } }, // 坐标轴颜色
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          axisLabel: { color: 'white' },
          axisLine: { lineStyle: { color: '#aaa' } }, // 坐标轴颜色
          splitLine: {
            show: true,
            lineStyle: {
              color: '#666', // 调整颜色为更浅灰色以确保可见
              type: 'dashed', // 设置分割线为虚线
              width: 1 // 调整虚线的宽度
            }
          }
        },
        series: [
          {
            type: 'bar',
            data: data.map(item => parseFloat(item.value)),
            itemStyle: {
              color: function (params) {
                const colors = ['#ff7f50', '#87cefa', '#da70d6', '#32cd32'];
                return colors[params.dataIndex];
              },
              barBorderRadius: [3, 3, 0, 0], // 圆角
              shadowColor: 'rgba(0, 0, 0, 0.5)', // 阴影颜色
              shadowBlur: 10 // 阴影模糊
            },
            label: {
              show: true,
              position: 'top',
              formatter: function (params) {
                const item = data[params.dataIndex];
                return `${params.value}万\n${item.arrow} ${item.change}`;
              },
              color: 'white',
              textStyle: { fontSize: 14 }
            },
            emphasis: {
              itemStyle: {
                color: '#FFD700' // 高亮时的颜色
              }
            }
          }
        ],
        grid: {
          left: '3%',
          right: '3%',
          bottom: '3%',
          containLabel: true
        }
      };
    },
    getChart3Options() {
      const risk1 = this.sumList.filter(item => item.risk >= 0 && item.risk <= 0.3).length;
      const risk2 = this.sumList.filter(item => item.risk > 0.3 && item.risk <= 0.6).length;
      const risk3 = this.sumList.filter(item => item.risk > 0.6 && item.risk < 1).length;
      const total = risk1 + risk2 + risk3;

      const risk1Percent = total !== 0 ? (risk1 / total * 100).toFixed(2) : 0;
      const risk2Percent = total !== 0 ? (risk2 / total * 100).toFixed(2) : 0;
      const risk3Percent = total !== 0 ? (risk3 / total * 100).toFixed(2) : 0;

      // 初始化变化率和箭头
      let risk1Change = '0%';
      let risk2Change = '0%';
      let risk3Change = '0%';
      let risk1Arrow = '↑';
      let risk2Arrow = '↑';
      let risk3Arrow = '↑';

      // 计算变化率
      const lastRisk1Percent = parseFloat(localStorage.getItem('lastRisk1Percent')) || 0;
      const lastRisk2Percent = parseFloat(localStorage.getItem('lastRisk2Percent')) || 0;
      const lastRisk3Percent = parseFloat(localStorage.getItem('lastRisk3Percent')) || 0;

      if (lastRisk1Percent !== 0) {
        const risk1ChangeRate = ((risk1Percent - lastRisk1Percent) / lastRisk1Percent * 100).toFixed(2);
        risk1Change = `${risk1ChangeRate}%`;
        risk1Arrow = risk1ChangeRate >= 0 ? '↑' : '↓';
      }
      if (lastRisk2Percent !== 0) {
        const risk2ChangeRate = ((risk2Percent - lastRisk2Percent) / lastRisk2Percent * 100).toFixed(2);
        risk2Change = `${risk2ChangeRate}%`;
        risk2Arrow = risk2ChangeRate >= 0 ? '↑' : '↓';
      }
      if (lastRisk3Percent !== 0) {
        const risk3ChangeRate = ((risk3Percent - lastRisk3Percent) / lastRisk3Percent * 100).toFixed(2);
        risk3Change = `${risk3ChangeRate}%`;
        risk3Arrow = risk3ChangeRate >= 0 ? '↑' : '↓';
      }

      // 更新上一次的百分比
      localStorage.setItem('lastRisk1Percent', risk1Percent);
      localStorage.setItem('lastRisk2Percent', risk2Percent);
      localStorage.setItem('lastRisk3Percent', risk3Percent);

      return {
        title: [
          {
            text: '医保欺诈风险占比',
            x: 'center',
            textStyle: { fontSize: 18, color: 'white' }
          },
          {
            text: '低风险同比',
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '30%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          },
          {
            text: `${risk1Change} ${risk1Arrow}`,
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '35%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          },
          {
            text: '中风险同比',
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '50%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          },
          {
            text: `${risk2Change} ${risk2Arrow}`,
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '55%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          },
          {
            text: '高风险同比',
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '70%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          },
          {
            text: `${risk3Change} ${risk3Arrow}`,
            left: '8%',  // 调整文本相对于图表的水平位置
            top: '75%',  // 调整文本相对于图表的垂直位置
            textAlign: 'center',
            textVerticalAlign: 'middle',
            textStyle: { fontSize: 14, color: 'white' }
          }
        ],
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            return `${params.name}: ${params.value} (${params.percent}%) `;
          }
        },
        color: ['#ff7f50', '#87cefa', 'purple'],
        series: [
          {
            type: 'pie',
            radius: ['50%', '70%'],
            data: [
              { value: risk1, name: '低风险' },
              { value: risk2, name: '中风险' },
              { value: risk3, name: '高风险' }
            ],
            label: {
              textStyle: { color: '#aaa' },
              formatter: function (params) {
                return `${params.name}`;
              }
            }
          }
        ]
      };
    },
    getChart4Options() {
      const fraudData = this.sumList.filter(item => item.RES === 1);
      const ranges = [
        { name: '0000~5000', min: 0, max: 5000 },
        { name: '5000~10000', min: 5000, max: 10000 },
        { name: '10000~15000', min: 10000, max: 15000 },
        { name: '15000~20000', min: 15000, max: 20000 },
        { name: '20000~', min: 20000, max: Infinity }
      ];
      const counts = ranges.map(range =>
        fraudData.filter(item => item['本次审批金额_SUM'] >= range.min && item['本次审批金额_SUM'] < range.max).length
      );

      const totalAmount = fraudData.reduce((sum, item) => sum + item['本次审批金额_SUM'], 0).toFixed(0);

      return {
        title: {
          text: '欺诈金额分布',
          x: 'center',
          textStyle: { fontSize: 18, color: 'white' }
        },
        tooltip: {
           trigger: 'item',
              formatter(params) {
                let result = '';
                if (params.name) {
                  result += `${params.name}<br/>`;
                }
                for (let i = 0; i < params.value.length; i++) {
                  result += `${ranges[i].name}数量：${params.value[i]}<br/>`;
                }
                result += `欺诈金额总和：${totalAmount}元`;
                return result;
              }
            },
        radar: {
          indicator: ranges.map(range => ({ name: range.name, max: Math.max(...counts) })),
          center: ['50%', '50%'],
          radius: '60%',
          name: {
            textStyle: { color: '#aaa' }
          }
        },
        series: [{
          type: 'radar',
          data: [
            { value: counts }
          ]
        }]
      };
    },
    getChart5Options() {
      const topFive = this.sumList.slice(0, 5);

      return {
        title: {
          text: '骗保TOP5',
          x: 'center',
          textStyle: { fontSize: 18, color: 'white' }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter(params) {
            let result = `${params[0].name}<br/>`;
            result += `${params[0].value.toFixed(2)}元`;
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
          data: ['5', '4', '3', '2', '1'],
          axisLine: { show: false },
          axisLabel: { color: 'white' }
        },
        xAxis: {
          type: 'value',
          axisLine: { show: false },
          axisLabel: { show: false },
          splitLine: { show: false }
        },
        series: [{
          type: 'bar',
          barWidth: '30',
          radius: '50%',
          data: [
            topFive[1]['本次审批金额_SUM'],
            topFive[3]['本次审批金额_SUM'],
            topFive[4]['本次审批金额_SUM'],
            topFive[0]['本次审批金额_SUM'],
            topFive[2]['本次审批金额_SUM']
          ],
          itemStyle: {
            color(params) {
              const colorList = [
                ['#009c41', '#b2dcb6'],
                ['#7da47c', '#62bd69'],
                ['#476f4d', '#e8f9df'],
                ['#4a6c4c', '#c6cc54'],
                ['#365c3b', '#abd0a7'],
              ];
              const colorItem = colorList[params.dataIndex];
              return new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: colorItem[0] },
                { offset: 1, color: colorItem[1] }
              ], false);
            },
            barBorderRadius: [0, 13, 13, 0],
          },
          label: {
            show: true,
            position: 'inside',
            formatter: function (params) {
              return `${params.value.toFixed(2)}元`;
            },
            textStyle: { color: '#444', fontSize: 15 }
          }
        }]
      };
    },
    getChart6Options() {
      const totalRecords = this.sumList.length;
      const totalFraudRecords = this.sumList.filter(item => item.RES === 1).length;
      const totalFraudAmount = this.sumList
        .filter(item => item.RES === 1)
        .reduce((sum, item) => sum + item['本次审批金额_SUM'], 0)
        .toFixed(0);

      const totalAmount = this.sumList
        .reduce((sum, item) => sum + item['本次审批金额_SUM'], 0)
        .toFixed(0);

      // 计算欺诈记录和欺诈金额的比例
      const fraudRecordsPercentage = ((totalFraudRecords / totalRecords) * 100).toFixed(2);
      const fraudAmountPercentage = ((totalFraudAmount / totalAmount) * 100).toFixed(2);

      return {
        title: {
          text: '总欺诈记录与金额',
          x: 'center',
          textStyle: { fontSize: 18, color: 'white' }
        },
        tooltip: {
          formatter: function (params) {
            if (params.seriesName === '欺诈记录总数') {
              return `${params.seriesName}<br/>数量: ${totalFraudRecords}`;
            } else {
              return `${params.seriesName}<br/>金额: ${totalFraudAmount} 元`;
            }
          }
        },
        series: [
          {
            name: '欺诈记录总数',
            type: 'gauge',
            center: ['25%', '55%'],
            radius: '50%',
            min: 0,
            max: 100,  // 百分比最大值
            splitNumber: 10,
            axisLine: {
              lineStyle: {
                color: [[0.2, '#ff4500'], [0.8, '#87cefa'], [1, '#32cd32']],
                width: 10
              }
            },
            pointer: {
              width: 5
            },
            detail: {
              formatter: function () {
                return `${totalFraudRecords} 条`;
              },
              offsetCenter: [0, '80%'], // 调整文字向下移动
              textStyle: {
                color: 'white',
                fontSize: 20
              }
            },
            data: [{ value: fraudRecordsPercentage, name: '欺诈记录' }]
          },
          {
            name: '欺诈金额总数',
            type: 'gauge',
            center: ['75%', '55%'],
            radius: '50%',
            min: 0,
            max: 100,  // 百分比最大值
            splitNumber: 10,
            axisLine: {
              lineStyle: {
                color: [[0.2, '#ff4500'], [0.8, '#87cefa'], [1, '#32cd32']],
                width: 10
              }
            },
            pointer: {
              width: 5
            },
            detail: {
              formatter: function () {
                return `${totalFraudAmount} 元`;
              },
              offsetCenter: [0, '80%'], // 调整文字向下移动
              textStyle: {
                color: 'white',
                fontSize: 20
              }
            },
            data: [{ value: fraudAmountPercentage, name: '欺诈金额' }]
          }
        ]
      };
    }


  },
  mounted() {
    this.fetchData();
  },
};
</script>
