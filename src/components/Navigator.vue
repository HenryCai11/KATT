<template>
  <el-menu
    id="navigator"
    :collapse="isCollapse"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    class="el-menu-vertical-demo"
  >
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-document-copy"></i>
        <span slot="title">文档资源</span>
      </template>
      <el-menu-item-group>
        <span slot="title">文档</span>
        <el-menu-item v-for="item in $store.state.fileList" @click="gotoTranslation(item.name)" :key="item.uid">{{ item.short_name }}</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="2" @click="gotoCorpus">
      <i class="el-icon-chat-line-round"></i>
      <span slot="title">语料资源</span>
    </el-menu-item>
    <el-menu-item index="3" @click="gotoDocuments">
      <i class="el-icon-upload2"></i>
      <span slot="title">文档上传</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: "Navigator",
  props: ["collapseVal"],
  data() {
    return {};
  },
  computed: {
    isCollapse() {
      return this.collapseVal === "true" ? true : false;
    }
  },
  methods: {
    //跳转至Documents页
    gotoDocuments() {
      this.$emit('startNavigate', '/documents')
    },
    gotoCorpus() {
      this.$emit('startNavigate', '/corpus')
    },
    gotoTranslation(val) {
      this.$emit('startNavigate', '/translation/'+val)
    }
  }
};
</script>

<style scoped>
/* 左侧导航栏 */
.collapse {
  width: 201px;
}
#navigator {
  height: 70vh;
  text-align: left;
}
#term-table {
  width: 100%;
  height: 70vh;
  background-color: #dbecff;
  border-radius: 5px;
  border: 2.8px rgb(225, 192, 255) solid;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 201px;
}
.el-menu-item {
  word-wrap: break-word;
  max-height: 500px;
}
</style>
