<template>
  <div>
    <app-header></app-header>
    <div class="item-container">
      <div></div>
      <h2>参保个体详情</h2>
      <p>个人编码: {{ itemData['个人编码'] }}</p>
      <p>本次审批金额: {{ itemData['本次审批金额_SUM'] }} 元</p>
      <p>是否挂号: {{ itemData['是否挂号'] === 1 ? '是' : '否' }}</p>
      <p>是否民政救助: {{ itemData['BZ_民政救助'] === 1 ? '是' : '否' }}</p>
      <p>是否城乡优抚: {{ itemData['BZ_城乡优抚'] === 1 ? '是' : '否' }}</p>
      <p>月就诊次数: {{ itemData['月就诊次数_MAX'] }} 次</p>
    </div>
  </div>
</template>

<script>
//这里导入其他文件
export default {
  //引入的组件注入到对象中才能使用
  components: {},
  data() {
    return {
      itemData:{}
    };
  },
  methods: {
  },//方法集合
  mounted() {
    const personalCode = this.$route.params.personalCode;
    // 根据个人编码从 sessionStorage 中获取对应的数据
    const sumList = JSON.parse(sessionStorage.getItem('sumList')) || [];
    this.itemData = sumList.find(item => item['个人编码'] == personalCode) || {};
  },//生命周期 - 挂载完成
};
</script>
<style scoped></style>