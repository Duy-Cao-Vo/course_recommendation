import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios"
import {Row, Col, Menu, Icon, Input, Card, Checkbox, Steps, Button, Rate, Radio, Tag, Tabs, Select, notification, message, Modal, Table, Avatar} from "ant-design-vue"
import "ant-design-vue/dist/antd.css"
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'chart.js';
import VueBlobJsonCsv from 'vue-blob-json-csv';
import JsonCSV from "vue-json-csv"
import { ButtonPlugin, NavbarPlugin, SidebarPlugin, TabsPlugin, DropdownPlugin, IconsPlugin, FormSelectPlugin, BootstrapVue } from 'bootstrap-vue'
import VueApexCharts from "vue-apexcharts";
axios.defaults.baseURL = 'http://localhost:8000'
Vue.config.productionTip = false
Vue.use(VueBlobJsonCsv)
Vue.component('downloadCsv', JsonCSV)

Vue.use(ButtonPlugin)
Vue.use(BootstrapVue)
Vue.use(NavbarPlugin)
Vue.use(SidebarPlugin)
Vue.use(TabsPlugin)
Vue.use(DropdownPlugin)
Vue.use(IconsPlugin)
Vue.use(FormSelectPlugin)
Vue.use(VueApexCharts)
Vue.use(Modal)
Vue.use(Row)
Vue.use(Col)
Vue.use(Menu)
Vue.use(Icon)
Vue.use(Input)
Vue.use(Card)
Vue.use(Checkbox)
Vue.use(Button)
Vue.use(Rate)
Vue.use(Tag)
Vue.use(Radio)
Vue.use(Tabs)
Vue.use(Select)
Vue.use(Steps)
Vue.use(Table)
Vue.use(Avatar)
Vue.prototype.$notification = notification
Vue.prototype.$message = message
Vue.component('apexchart', VueApexCharts)
new Vue({
  router,
  store,
  axios,
  notification,
  render: h => h(App)
}).$mount('#app')

