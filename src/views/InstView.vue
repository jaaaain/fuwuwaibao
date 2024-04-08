<template>
  <div>
    <app-header></app-header>
    <!-- 显示使用说明 -->
    <div class="usage-instructions">
      <h2>使用说明</h2>
      <p>一.医保数据预测下载：</p>
      <ol>
        <li>1.下载模版文件，将特征导入对应的列，注意文件编码维持utf-8</li>
        <li>2.点击开始预测，选择导入好的文件，会显示如果选择错误会有相应提示</li>
        <li>3.点击开始上传，等待上传成功后显示预览界面</li>
        <li>4.此时可以选择下载结果或者进入详情界面查看所有数据</li>
      </ol>
      <p>二.医保数据分析统计：</p>
      <ol>
        <li>1.点击医保列表，会展示所有上传的数据，再点击单个数据，可以查看数据详情</li>
        <li>2.点击数据分析，会展示数据分析图表，显示所有数据的分析和统计</li>
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  props: {},
  data() {
    return {};
  },
  methods: {},
  mounted() {},
};
</script>

<style scoped>
/* 样式可以根据您的需求进行自定义 */
.usage-instructions {
  margin: 60px auto; /* 设置上下间距为60px，左右自动居中 */
  margin-left: 100px; /* 向左移动内容 */
  margin-top: 100px; /* 向下移动内容 */
}
.usage-instructions h2 {
  font-size: 28px; /* 标题字体大小增大 */
  margin-bottom: 70px; /* 标题与内容之间的间距增大 */
  color: white;
}
.usage-instructions p,
.usage-instructions ol {
  font-size: 18px; /* 正文字体大小增大 */
  margin-bottom: 50px; /* 正文与列表之间的间距增大 */
  color: white;
}
.usage-instructions li {
  display: block; /* 每个列表项单独成行 */
  margin-bottom: 20px; /* 列表项之间的间距增大 */
  color: white;
}
</style>
