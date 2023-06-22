<template>
  <div id="app">
    <div class="corpus-button" @click="gotoCorpusReviewButton(title)">{{ title }}</div>
  </div>
</template>

<script>
export default {
  name: "CorpusCard",
  props: ["title"],
  data() {
    return {};
  },
  methods: {
    gotoCorpusReviewButton(val) {
      this.$emit("gotoCorpusReview", val);
    }
  }
};
</script>

<style scoped>
#app {
  width: 200px;
  height: 200px;
  background-color: #fff;
  display: flex;
  border: 3px solid rgba(48, 48, 167, 0.3);
  border-radius: 5px;
  justify-content: center;
  align-items: center;
  float: left;
  margin-right: 33px;
  margin-bottom: 10px;
  transition: background-color 0.5s 0.1s;
}
.corpus-button {
  cursor: pointer;
}
#app:hover {
  background-color: lightblue;
}
</style>
