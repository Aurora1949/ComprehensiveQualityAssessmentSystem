import { createApp } from 'vue'
import router from "./router";
import './style.scss'
import 'animate.css'
import 'element-plus/es/components/message/style/css'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import {createPinia} from "pinia";
import piniaPersist from 'pinia-plugin-persist'


createApp(App).use(createPinia().use(piniaPersist)).use(router).use(ElementPlus, {locale: zhCn,}).mount('#app')
