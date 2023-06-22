<template>
  <div id="app">
    <!-- 主体部分 -->
    <!-- 中间翻译部分 -->
    <div id="translation-area">
      <!-- 翻译框 -->
      <el-table :data="tableData" style="width: 100%">
        <!-- 原文呈现翻译 -->
        <el-table-column label="原文" prop="source" width="330"></el-table-column>
        <!-- 译文输入框 -->
        <el-table-column label="译文" prop="target" width="330">
          <template slot-scope="biling">
            <translation-bar :content="tableData[biling.$index].target"></translation-bar>
          </template>
        </el-table-column>
        <!-- 右侧操作按钮 -->
        <el-table-column label="操作" width="100" fixed="right">
          <template slot-scope="opr">
            <el-button type="text" size="small" icon="el-icon-caret-right" @click="autoFill(opr)"></el-button>
            <el-button type="text" size="small" icon="el-icon-check"></el-button>
            <el-button type="text" size="small" icon="el-icon-delete"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 右侧分析栏 -->
    <!-- <el-col :span="5" :offset="1">
        <div id="analysis-table"></div>
        <div id="analysis-graph"></div>
    </el-col>-->
  </div>
</template>

<script>
import TranslationBar from "./components/TranslationBar.vue";

export default {
  name: "Translation",
  props: ['title'],
  components: {
    TranslationBar
  },
  data() {
    return {
      tableData: [{source: this.title, target: ''}],
      bardata: "test",
      testModel: ""
    };
  },
  beforeMount() {
    let _this = this
    this.axios
    .get("/getsegments?title=" + this.title)
    .then(response => {
      let segTable = response.data;
      console.log(segTable)
      for (let key in segTable) {
        _this.tableData.push({source: segTable[key], target:''})
      }
    })
  },
  methods: {
    autoFill() {
      alert('test')
    }
  }
};
</script>

<style scoped>
#analysis-table {
  width: 100%;
  height: 38vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
}
#analysis-graph {
  width: 100%;
  margin-top: 2vh;
  height: 30vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
}
/* 翻译窗（中间） */
#translation-area {
  width: 100%;
  height: 80vh;
  padding: 20px;
  overflow: auto;
  border-right: 2.8px rgb(225, 192, 255) solid;
  border-left: 2.8px rgb(225, 192, 255) solid;
}
.el-table {
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
.el-col {
  border-radius: 4px;
}
.el-row {
  margin-top: 5vh;
  height: 70vh;
}
</style>
