<template>
  <div id="app">
    <!-- 主体部分 -->
    <el-row>
      <!-- 左侧导航栏 -->
      <el-col :span="3">
        <navigator :collapseVal="isCollapse" @startNavigate="gotoAnotherPage"></navigator>
      </el-col>
      <!-- 中间图标部分 -->
      <el-col :span="13" :offset="1" v-loading="loading">
        <transition name="right" mode="out-in">
          <router-view @getStarted="gotoAnotherPage"></router-view>
        </transition>
      </el-col>
      <!-- 右侧信息区域 -->
      <el-col :span="5" :offset="1" v-loading="loading">
        <transition name="right" mode="out-in">
          <router-view name="right"></router-view>
        </transition>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      path: this.$route.path,
      loading: false
    };
  },
  methods: {
    gotoAnotherPage(val) {
      let _this = this;
      this.loading = true;
      this.path = val;
      setTimeout(() => {
        _this.loading = false;
      }, 2000);
      this.$router.push({ path: val });
    },
    getFileList() {
      let _this = this;
      this.axios.get("/getfilelist").then(response => {
        Object.keys(response.data.filelist).forEach(key => {
          let input_data = response.data.filelist[key]
          let short_name = response.data.shortname[key]
          _this.$store.state.fileList.push({ name: input_data, short_name: short_name });
        });
      });
    }
  },
  computed: {
    isCollapse() {
      if (this.path != "/" && this.path != "/#/") {
        return "false";
      } else {
        return "true";
      }
    }
  },
  beforeMount() {
    this.getFileList()
  }
};
</script>

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
.right-enter {
  opacity: 0;
}
.right-enter-to {
  opacity: 1;
}
.right-enter-active {
  transition: 0.6s;
}
.right-leave {
  opacity: 1;
}
.right-leave-to {
  opacity: 0;
}
.right-leave-active {
  transition: 1.3s;
}
</style>
