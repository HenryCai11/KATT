<template>
  <div id="app">
    <!-- 首页logo -->
    <div id="logo-area">
      <div id="home-logo"><h1><b>KATT</b></h1>——Knowledge-Assisted Translation Toolket</div>
      <div id="start-button">
        <el-button type="primary" round @click="startButton">开始体验</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  methods: {
    startButton() {
      this.$emit("getStarted", "/documents");
    }
  }
};
</script>

<style scoped>
/* 中间图标部分 */
#logo-area {
  width: 100%;
  height: 80vh;
  padding: 20px;
  overflow: auto;
}
#home-logo {
  width: 70%;
  height: 30%;
  font-size: 38px;
  margin: 0 auto;
  margin-left: 30vh;
  margin-top: 10vh;
}
#start-button {
  width: 10%;
  height: 7.5%;
  margin: 0 auto;
  margin-top: 50px;
  margin-left: 29.5vw;
  display: flex;
  align-items: center;
  justify-content: center;
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
