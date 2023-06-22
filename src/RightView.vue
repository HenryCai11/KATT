<template>
  <div id="app">
    <!-- 右侧术语查看栏 -->
    <div id="term-table">
      <div v-for="item in keywordList" :key="item.uid">...{{item.former}}<b>{{ item.keyword }}</b>{{ item.latter }}...</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RightView",
  props: ['title'],
  data() {
    return {
      keywordList: []
    };
  },
  methods: {
  },
  mounted() {
    this.axios
      .get('/getwordwindow?title=' + this.title)
      .then(response => {
        Object.keys(response.data.winlist).forEach(key => {
          this.keywordList.push(response.data.winlist[key])
        })
      })
  }
};
</script>

<style scoped>
#term-table {
  width: 100%;
  height: 70vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
  overflow: scroll;
  word-wrap: normal;
}
</style>
<style>
/* 整体 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  /* -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  text-align: center;
  height: 100%;
}
.el-row {
  margin-top: 5vh;
  height: 70vh;
}
.el-col {
  border-radius: 4px;
}
</style>
