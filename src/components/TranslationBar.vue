<template>
  <div class="translation-box">
    <div
      class="translation-content"
      contenteditable="true"
      v-html="translationContent"
      @input="contentChange"
    ></div>
  </div>
</template>

<script>
export default {
  name: "TranslationBar",
  props: ['content'],
  data() {
    return {
      translationContent: this.content,
    }
  },
  methods: {
    contentChange() {

    }
  },

}
</script>

<style scoped>
  .translation-content {
    box-sizing: border-box;/*使padding设置后不溢出*/
    min-height: 50px;
    width: 100%;
    /* resize: none; */
    font: normal 500 16px/1.5em Georgia, serif;
    padding: 0.5em;
    border: 3px solid rgba(48, 48, 167, 0.3);
    background: rgba(255, 255, 255, 1);
    outline: none;/*获取焦点后的边框 */
    border-radius: 8px;/*文本框的棱角 */
    z-index: 3;

    overflow-x: hidden;
    transition: border 0.5s 0.1s;/*边框颜色渐变 */
  }
  .translation-content:hover {
    border: 3px solid rgba(48, 48, 167, 0.7)
  }
  .translation-content:focus {
    border: 3px solid rgba(48, 48, 167, 1);
  }
  .translation-box {
    position: relative;
    text-align: left;
  }


</style>
