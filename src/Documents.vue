<template>
  <div id="app">
    <!-- 中间文件上传区域 -->
    <div id="document-area">
      <!-- 文件上传 -->
      <el-upload
        class="upload-demo"
        action="https://jsonplaceholder.typicode.com/posts/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
        :limit="3"
        :on-exceed="handleExceed"
        :file-list="fileList"
        style="float:left; width: 100%;text-align:left"
      >
        <el-button slot="trigger" icon="el-icon-s-order" size="small" type="primary">上传文件</el-button>
        <!-- 文本上传 -->
        <el-button
          size="small"
          type="primary"
          icon="el-icon-upload el-icon--right"
          @click="dialogUploadVisible = true"
          style="margin-left:10px"
        >上传文本</el-button>
      </el-upload>
      <!-- 文本上传弹窗 -->
      <el-dialog title="文本上传" :visible.sync="dialogUploadVisible" :before-close="handleClose">
        标题：
        <el-input v-model="title" type="input" style="width: 300px; margin-bottom: 10px"></el-input>
        <br />
        <el-input
          type="textarea"
          v-model="text"
          :autosize="{minRows: 10, maxRows: 10}"
          placeholder="将文本粘贴至此处"
          @keyup.17.enter="UploadText"
        ></el-input>
        <el-button size="small" @click="UploadText">完成</el-button>
      </el-dialog>
      <!-- 文件展示列表 -->
      <div>
        <!-- <table id="doc-table">
          <thead>
            <tr>
              <th>文件名</th>
              <th>上传日期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>-->
      </div>
    </div>
  </div>
</template>

<script>
import "es6-promise/auto";

export default {
  name: "Documents",
  data() {
    return {
      bardata: "test",
      testModel: "",
      dialogUploadVisible: false,
      text: null,
      title: null,
      fileList: this.$store.state.fileList
    };
  },
  methods: {
    // 文本上传处理函数
    UploadText() {
      console.log(this.text);
      let _this = this;
      // GET请求后端数据
      this.axios
        .get("/add?title=" + this.title + "&text=" + this.text)
        .then(response => {
          _this.$store.state.fileList.push({
            name: _this.title,
            short_name: response.data.shortname
          });
          _this.title = null;
          _this.text = null;
        });
      this.dialogUploadVisible = false;
    },
    //
    //
    //
    // 文件上传处理函数
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    // 点击文件跳转
    handlePreview(file) {
      this.$emit("getStarted", "/translation/" + file.name);
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 3 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      );
    },
    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    // 关闭文本上传弹窗
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then(() => {
          done();
        })
        .catch(() => {});
    },
  }
};
</script>

<style scoped>
.el-row {
  margin-top: 5vh;
  height: 70vh;
}
#doc-table {
  width: 100%;
}
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
#document-area {
  width: 100%;
  height: 80vh;
  padding: 20px;
  overflow: auto;
  border-right: 2.8px rgb(225, 192, 255) solid;
  border-left: 2.8px rgb(225, 192, 255) solid;
}
.el-col {
  border-radius: 4px;
}
.nav-button {
  text-align: center;
  height: 3em;
  padding-top: 0.8em;
  margin-bottom: 1px;
  border-radius: 5px;
  width: 100%;
  color: #dbecff;
  background-color: rgb(8, 8, 109);
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
</style>
