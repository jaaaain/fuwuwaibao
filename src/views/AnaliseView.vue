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

.chart-box6{
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
      chartColumns: [
        [
          {id: 'Chart1', class: 'chart-box1'},
          {id: 'Chart3', class: 'chart-box3'}
        ],
        [
          {id: 'Chart6', class: 'chart-box6'},
          {id: 'Chart4', class: 'chart-box4'}
        ],
        [
          {id: 'Chart2', class: 'chart-box2'},
          {id: 'Chart5', class: 'chart-box5'}
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
      const chartInstance = echarts.init(document.getElementById(chartId));
      chartInstance.setOption(options);
    },
    getChart1Options() {
      const count0 = this.sumList.filter(item => item.RES === 0).length;
      const count1 = this.sumList.filter(item => item.RES === 1).length;

      return {
        title: {
          text: '骗保占比',
          x: 'center',
          textStyle: {fontSize: 18, color: 'white'},
        },
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
              {value: count0, name: '非骗保'},
              {value: count1, name: '骗保'}
            ],
            label: {textStyle: {color: '#aaa'}}
          }
        ]
      };
    },
    getChart2Options() {
      const count00000to10000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 0 && item['本次审批金额_SUM'] < 10000).length;
      const count10000to20000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 10000 && item['本次审批金额_SUM'] < 20000).length;
      const count20000to30000 = this.sumList.filter(item => item['本次审批金额_SUM'] >= 20000 && item['本次审批金额_SUM'] < 30000).length;
      const count30000to = this.sumList.filter(item => item['本次审批金额_SUM'] >= 30000).length;

      return {
        title: {
          text: '审批金额分析',
          x: 'center',
          textStyle: {fontSize: 18, color: 'white'},
        },
        legend: {
          type: 'scroll',
          top: '1%',
          textStyle: {color: 'white'},
          data: [{name: '数量', icon: 'circle'}]
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {type: 'shadow', axis: 'auto'},
          padding: 5,
          textStyle: {color: "green"},
        },
        xAxis: {
          offset: 10,
          name: '数值',
          nameGap: 15,
          type: 'category',
          axisLabel: {interval: 0, rotate: 30},
          data: ['0~10000', '10000~20000', '20000~30000', '30000~']
        },
        yAxis: {
          type: 'value',
          offset: 1,
          name: '数量',
          nameGap: 15,
          axisLine: {
            show: true,
            symbol: ['none', 'arrow'],
            symbolSize: [8, 8],
            symbolOffset: [0, 7],
          },
          splitLine: {
            lineStyle: {color: '#666', type: 'dashed'},
          },
        },
        series: [{
          type: 'bar',
          legendHoverLink: true,
          label: {show: false},
          itemStyle: {color: 'green', barBorderRadius: [5, 5, 0, 0]},
          barWidth: '30',
          barCategoryGap: '20%',
          data: [count00000to10000, count10000to20000, count20000to30000, count30000to]
        }]
      };
    },
    getChart3Options() {
      const risk1 = this.sumList.filter(item => item.risk >= 0 && item.risk <= 0.3).length;
      const risk2 = this.sumList.filter(item => item.risk > 0.3 && item.risk <= 0.6).length;
      const risk3 = this.sumList.filter(item => item.risk > 0.6 && item.risk < 1).length;

      return {
        title: {
          text: '医保欺诈风险占比',
          x: 'center',
          textStyle: {fontSize: 18, color: 'white'},
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        color: ['#ff7f50', '#87cefa', 'purple'],
        series: [
          {
            type: 'pie',
            radius: ['50%', '70%'],
            data: [
              {value: risk1, name: '低风险'},
              {value: risk2, name: '中风险'},
              {value: risk3, name: '高风险'}
            ],
            label: {textStyle: {color: '#aaa'}}
          }
        ]
      };
    },
    getChart4Options() {
      const fraudData = this.sumList.filter(item => item.RES === 1);
      const count00000to5000 = fraudData.filter(item => item['本次审批金额_SUM'] >= 0 && item['本次审批金额_SUM'] < 5000).length;
      const count5000to10000 = fraudData.filter(item => item['本次审批金额_SUM'] >= 5000 && item['本次审批金额_SUM'] < 15000).length;
      const count10000to15000 = fraudData.filter(item => item['本次审批金额_SUM'] >= 10000 && item['本次审批金额_SUM'] < 15000).length;
      const count15000to20000 = fraudData.filter(item => item['本次审批金额_SUM'] >= 15000 && item['本次审批金额_SUM'] < 20000).length;
      const count20000to = fraudData.filter(item => item['本次审批金额_SUM'] >= 20000).length;

      return {
        title: {
          text: '欺诈金额展示',
          x: 'center',
          textStyle: {fontSize: 18, color: 'white'},
        },
        tooltip: {
          trigger: 'item',
          formatter(params) {
            let totalAmount = 0;
            fraudData.forEach(item => {
              totalAmount += item['本次审批金额_SUM'];
            });
            totalAmount = totalAmount.toFixed(0);
            let result = `${params.name}<br/>`;
            for (let i = 0; i < params.value.length; i++) {
              result += `维度${i + 1}数量：${params.value[i]}<br/>`;
            }
            result += `欺诈金额总和：${totalAmount}元`;
            return result;
          }
        },
        radar: {
          indicator: [
            {name: '0000~'},
            {name: '5000~'},
            {name: '10000~'},
            {name: '15000~'},
            {name: '20000~'}
          ],
          center: ['50%', '50%'],
          radius: '60%',
          name: {
            textStyle: {color: '#aaa'}
          }
        },
        series: [{
          type: 'radar',
          data: [
            {value: [count00000to5000, count5000to10000, count10000to15000, count15000to20000, count20000to]}
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
          textStyle: {fontSize: 18, color: 'white'}
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {type: 'shadow'},
          formatter(params) {
            let result = `${params[0].name}<br/>`;
            result += params[0].value.toFixed(2);
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
          axisLine: {show: false},
          axisLabel: {color: 'white'}
        },
        xAxis: {
          type: 'value',
          axisLine: {show: false},
          axisLabel: {show: false},
          splitLine: {show: false}
        },
        series: [{
          type: 'bar',
          barWidth: '30',
          radius: '50%',
          data: [topFive[1]['本次审批金额_SUM'], topFive[3]['本次审批金额_SUM'], topFive[4]['本次审批金额_SUM'], topFive[0]['本次审批金额_SUM'], topFive[2]['本次审批金额_SUM']],
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
                {offset: 0, color: colorItem[0]},
                {offset: 1, color: colorItem[1]}
              ], false);
            },
            barBorderRadius: [0, 13, 13, 0],
          },
          label: {
            show: true,
            position: 'inside',
            textStyle: {color: '#444', fontSize: 15}
          }
        }]
      };
    },
    getChart6Options() {
      const totalFraudRecords = this.sumList.filter(item => item.RES === 1).length;
      let totalFraudAmount = 0;
      this.sumList.forEach(item => {
        if (item.RES === 1) {
          totalFraudAmount += item['本次审批金额_SUM'];
        }
      });
      totalFraudAmount = totalFraudAmount.toFixed(0);

      return {
        title: {
          text: '总共的欺诈记录和金额',
          x: 'center',
          textStyle: {fontSize: 18, color: 'white'}
        },
        tooltip: {
          formatter: '{a} <br/>{b} : {c}'
        },
        series: [
          {
            name: '欺诈记录总数',
            type: 'gauge',
            center: ['25%', '55%'],
            radius: '50%',
            min: 0,
            max: 1000,  // 可以根据实际数据调整最大值
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
              formatter: '{value}',
              textStyle: {
                color: 'white',
                fontSize: 20
              }
            },
            data: [{value: totalFraudRecords, name: '欺诈记录'}]
          },
          {
            name: '欺诈金额总数',
            type: 'gauge',
            center: ['75%', '55%'],
            radius: '50%',
            min: 0,
            max: 1000000,  // 可以根据实际数据调整最大值
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
              formatter: '{value} 元',
              textStyle: {
                color: 'white',
                fontSize: 20
              }
            },
            data: [{value: totalFraudAmount, name: '欺诈金额'}]
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
