<template>
  <div class="flex min-h-full flex-1">
    <div class="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img class="h-12 w-auto" :src="logo" alt="建筑工程学院"/>
          <h2 class="mt-8 text-2xl font-bold leading-9 tracking-tight text-gray-900">欢迎使用综合素质评价系统</h2>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            请先登录
            {{ ' 或 ' }}
            <router-link :to="{name: 'login'}" class="font-semibold text-indigo-600 hover:text-indigo-500">本期综测结果快速查询</router-link>
          </p>
        </div>

        <div class="mt-10">
          <div>
            <form @submit.prevent class="space-y-6">
              <div>
                <label for="username" class="block text-sm font-medium leading-6 text-gray-900">账号</label>
                <div class="mt-2">
                  <input id="username" name="username" type="text" v-model="login.username" required=""
                         class="block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"/>
                </div>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">密码</label>
                <div class="mt-2">
                  <input id="password" name="password" type="password" v-model="login.passwd" required=""
                         class="block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"/>
                </div>
              </div>

              <!--              <div>-->
              <!--                <label for="code" class="block text-sm font-medium leading-6 text-gray-900">验证码</label>-->
              <!--                <div class="mt-2">-->
              <!--                  <input id="code" name="code" type="text" v-model="login.code" required=""-->
              <!--                         class="block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"/>-->
              <!--                </div>-->
              <!--              </div>-->

              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <input id="remember-me" name="remember-me" type="checkbox" v-model="login.remember"
                         class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"/>
                  <label for="remember-me" class="ml-3 block text-sm leading-6 text-gray-700">记住我</label>
                </div>

                <div class="text-sm leading-6">
                  <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500" @click="handleUnknownMyAccount">忘记密码？</a>
                </div>
              </div>

              <div>
                <button type="submit"
                        class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        @click="handleSubmitButton">
                  登录
                </button>
              </div>
            </form>
          </div>

          <div class="mt-10">
            <div class="relative">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-200"/>
              </div>
              <div class="relative flex justify-center text-sm font-medium leading-6">
                <span class="bg-white px-6 text-gray-900">或使用其他方式</span>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-2 gap-4">
              <a href="#"
                 class="cursor-not-allowed flex w-full items-center justify-center gap-3 rounded-md bg-[#39a2b1] px-3 py-1.5 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1D9BF0]">
                <img class="w-5 h-5" :src="xh" alt="">
                <span class="text-sm font-semibold leading-6">金科统一认证平台</span>
              </a>

              <a href="#"
                 class="cursor-not-allowed flex w-full items-center justify-center gap-3 rounded-md bg-[#1D9BF0] px-3 py-1.5 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#24292F]">
                <svg t="1699276441030" class="w-5 h-5" viewBox="0 0 1024 1024" version="1.1"
                     xmlns="http://www.w3.org/2000/svg" p-id="1641" width="200" height="200">
                  <path
                      d="M721.470952 470.273089c4.394674-17.578697 7.325139-35.157394 7.325139-55.666555 0-117.191995-96.682834-212.408574-213.874829-212.408574-117.191995 0-213.874829 95.218624-213.874829 212.408574 0 19.042907 2.930464 36.621604 7.325139 52.736091-23.437581 11.719813-49.805627 46.877207-64.455904 92.288159-17.578697 60.06123-10.253558 117.191995 17.578697 125.981343 16.114487 4.394674 35.157394-5.858884 51.271881-26.368046 8.789349 17.578697 19.042907 35.157394 32.22693 51.271881-33.693184 8.789349-57.130765 29.29851-57.130765 52.736091 0 33.693184 46.877207 61.52544 104.007972 61.52544 42.482533 0 80.568346-16.114487 95.218624-38.087858 10.253558 1.46421 19.042907 2.930464 27.832255 2.930464 8.789349 0 17.578697-1.46421 27.832255-2.930464 14.648233 21.973371 52.736091 38.087858 95.218624 38.087858 57.130765 0 104.007972-27.832255 104.007972-61.52544 0-23.437581-23.437581-43.946743-57.130765-52.736091 11.719813-14.648233 21.973371-30.76272 30.76272-46.877207 14.648233 17.578697 32.22693 26.368046 46.877207 21.973371 27.832255-8.789349 35.157394-65.920114 17.578697-125.981343C765.417694 517.148251 743.444323 483.457112 721.470952 470.273089z"
                      fill="#ffffff" p-id="1642"></path>
                  <path
                      d="M873.818296 150.926079C781.530137 58.63792 652.620374 1.507154 511.990798 1.507154S242.451459 58.63792 150.163299 150.926079C57.87514 243.214238 0.744375 372.124001 0.744375 512.753577c0 142.093786 57.130765 269.539339 149.418925 361.827498 92.288159 92.288159 221.197922 149.418925 361.827498 149.418925s269.539339-57.130765 361.827498-149.418925c92.288159-92.288159 149.418925-219.733713 149.418925-361.827498C1023.23722 372.124001 966.106455 243.214238 873.818296 150.926079zM831.337808 832.100588c-82.034601 82.034601-194.829877 133.304437-319.344966 133.304437s-237.31241-51.271881-319.344966-133.304437c-82.034601-80.568346-133.304437-194.829877-133.304437-319.344966s51.271881-237.31241 133.304437-319.344966 194.829877-133.304437 319.344966-133.304437 237.31241 51.271881 319.344966 133.304437 133.304437 194.829877 133.304437 319.344966S913.370364 751.532241 831.337808 832.100588z"
                      fill="#ffffff" p-id="1643"></path>
                </svg>
                <span class="text-sm font-semibold leading-6">腾讯QQ</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="relative hidden w-0 flex-1 lg:block">
      <img class="absolute inset-0 h-full w-full object-cover object-left" :src="bg" alt=""/>
    </div>
  </div>
</template>

<script setup lang="ts">
import logo from '@/assets/images/jg_logo.png'
import xh from '@/assets/images/xh-w.png'
import bg from '@/assets/images/login_bg.jpg'
import {onMounted, ref} from "vue";
import {userLogin} from "@/api/login.ts";
import router from "@/router";
import {ElMessage} from "element-plus";

interface LoginModel {
  username: string
  passwd: string
  code: string
  remember: boolean
}

const login = ref<LoginModel>({code: "", passwd: "", remember: false, username: ""})

const handleSubmitButton = async () => {
  const user: IUserLogin = {
    username: login.value.username,
    password: login.value.passwd
  }
  await userLogin(user).then(res => {
    if (login.value.remember) localStorage.setItem('token', res.access_token)
    else sessionStorage.setItem('token', res.access_token)
    router.push({name: 'panelIndex'})
  }).catch(err => {
    ElMessage({
      type: "error",
      message: err.detail ? err.detail : err
    })
  })
}

const handleUnknownMyAccount = () => {
  alert("请联系各班班长获取")
}

onMounted(() => {
  if (localStorage.getItem('token')) router.push({'name': 'panelIndex'})
})

</script>
