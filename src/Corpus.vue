<template>
  <div id="app">
    <!-- 中间翻译部分 -->
    <div id="corpus-area">
      <div id="corpus-card-area">
        <corpus-card v-for="item in corpusList" :key="item.uid" :title="item.name" @gotoCorpusReview="getStartedCorpusReview"></corpus-card>
      </div>
    </div>
    <!-- 右侧术语查看栏 -->
    <!-- <div id="term-table"></div> -->
  </div>
</template>

<script>
import CorpusCard from "./components/CorpusCard.vue";
export default {
  name: "Corpus",
  components: {
    CorpusCard
  },
  data() {
    return {
      corpusList: this.$store.state.fileList
    };
  },
  methods: {
    getStartedCorpusReview(val) {
      this.$emit("getStarted", "/corpusreview/"+val);
    }
  },
  mounted() {}
};
</script>

<style scoped>
/* 语料查看区域（中间） */
#corpus-area {
  width: 100%;
  height: 80vh;
  padding: 20px;
  overflow: auto;
  border-right: 2.8px rgb(225, 192, 255) solid;
  border-left: 2.8px rgb(225, 192, 255) solid;
}
#corpus-table {
  width: 80%;
  height: 10vh;
  background-color: #dbecff;
  margin: 0 auto;
}
#corpus-card-area {
  width: 90%;
  height: 58vh;
  margin: 0 auto;
  margin-top: 5vh;
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
