import { createApp } from 'vue'
import router from "./router";
import './style.scss'
import 'element-plus/es/components/message/style/css'
import App from './App.vue'
import {createPinia} from "pinia";

createApp(App).use(createPinia()).use(router).mount('#app')
