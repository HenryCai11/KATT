import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import 'es6-promise/auto'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import Corpus from './Corpus.vue'
import CorpusReview from './CorpusReview.vue'
import RightView from './RightView.vue'
import Home from './Home.vue'
import Documents from './Documents.vue'
import RightDocuments from './RightDocuments.vue'
import RightCorpus from './RightCorpus.vue'
import RightTranslation from './RightTranslation.vue'
import Translation from './Translation.vue'
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'
// import CorpusReview from './CorpusReview.vue'

axios.defaults.baseURL = 'http://127.0.0.1:5000';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';

Vue.use(ElementUI)
Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueAxios, axios)

const requireComponent = require.context(
  // 其组件目录的相对路径
  './components',
  // 是否查询其子目录
  false,
  // 匹配基础组件文件名的正则表达式
  /[A-Z]\w+\.vue$/
)

requireComponent.keys().forEach(fileName => {
  // 获取组件配置
  const componentConfig = requireComponent(fileName)

  // 获取组件的 PascalCase 命名
  const componentName = upperFirst(
    camelCase(
      // 获取和目录深度无关的文件名
      fileName
      .split('/')
      .pop()
      .replace(/\.\w+$/, '')
    )
  )

  // 全局注册组件
  Vue.component(
    componentName,
    // 如果这个组件选项是通过 `export default` 导出的，
    // 那么就会优先使用 `.default`，
    // 否则回退到使用模块的根。
    componentConfig.default || componentConfig
  )
})



Vue.config.productionTip = false

const store = new Vuex.Store({
  state: {
    count: 0,
    fileList: []
  }
})

const router = new VueRouter({
  routes: [{
      path: '/',
      component: Home
    },
    {
      path: '/corpus',
      components: {
        default: Corpus,
        right: RightCorpus
      }
    },
    {
      path: '/corpusreview/:title',
      components: {
        default: CorpusReview,
        right: RightView
      },
      props: {
        default: true,
        right: true
      }
    },
    {
      path: '/documents',
      components: {
        default: Documents,
        right: RightDocuments
      }
    },
    {
      path: '/translation/:title',
      components: {
        default: Translation,
        right: RightTranslation
      },
      props: {
        default: true,
        right: true
      }
    }
  ]
})


new Vue({
  render: h => h(App),
  store: store,
  router: router,
}).$mount('#app')
