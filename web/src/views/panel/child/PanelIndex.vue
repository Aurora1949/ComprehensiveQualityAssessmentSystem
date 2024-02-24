<template>
  <el-skeleton :loading="loading" animated>
    <template #template>
      <el-skeleton-item variant="text" style="height: 40px;"/>
      <el-skeleton-item variant="text" style="height: 40px;"/>
      <el-skeleton-item variant="p" style="width: 6em;"/>
      <el-skeleton-item variant="text" style="height: 80px;"/>
      <el-skeleton-item variant="p" style="width: 6em;"/>
      <el-skeleton-item variant="text" style="height: 160px;"/>
    </template>
    <template #default>
      <div class="mb-2">
        <el-alert v-if="isComplete" title="恭喜你，已经完成填报，耐心等待结果吧~" type="success" show-icon
                  :closable="false"/>
        <el-alert v-else title="你还未填写本期综测，快去填写吧！" type="warning" show-icon :closable="false"/>
      </div>
      <el-alert v-if="!isBind" type="warning" show-icon>
        <template #title>
          <span @click="handleShowBindWindow"
                class="cursor-pointer hover:underline underline-offset-auto	">点击此处绑定教务系统查看更多信息。</span>
        </template>
      </el-alert>
      <el-alert v-else type="success" show-icon>
        <template #title>
          <span @click="handleShowBindWindow"
                class="cursor-pointer hover:underline underline-offset-auto	">你已成功绑定至教务系统，点击此处解除绑定。</span>
        </template>
      </el-alert>
      <!--      <div class="my-2">-->
      <!--        <t-divider title="本期综测结果"/>-->
      <!--        <el-empty/>-->
      <!--      </div>-->
      <div class="my-2">
        <el-empty v-if="!isBind"/>
        <div v-else>
          <t-divider title="教务系统信息" class="mb-4"/>
          <el-descriptions :column="3" border class="mb-2">
            <el-descriptions-item label="学号">{{ jwxt_user.uid }}</el-descriptions-item>
            <el-descriptions-item label="学院">{{ jwxt_user.faculty }}</el-descriptions-item>
            <el-descriptions-item label="专业">{{ jwxt_user.specialty }}</el-descriptions-item>
            <el-descriptions-item label="学历">{{ jwxt_user.education_level }}</el-descriptions-item>
            <el-descriptions-item label="学制">{{ jwxt_user.eductional_systme }}年</el-descriptions-item>
          </el-descriptions>
          <p class="font-bold mb-4">学年成绩</p>
          <el-table :data="scoreList" stripe border>
            <el-table-column prop="credit" label="学分" sortable/>
            <el-table-column prop="score" label="成绩" sortable/>
            <el-table-column prop="lesson_name" label="课程名称"/>
            <el-table-column prop="point" label="绩点" sortable/>
            <el-table-column prop="bkcj" label="补考成绩"/>
            <el-table-column prop="cxcj" label="重修成绩"/>
          </el-table>
        </div>
      </div>
    </template>
  </el-skeleton>

  <el-dialog v-model="showBindWindow">
    <template #header>
      绑定至金陵科技学院教务系统
    </template>
    <template #default>
      <el-form :model="bindAccount" label-width="5rem" label-position="left">
        <el-form-item label="用户名" required>
          <el-tooltip content="此为自动识别的结果，不可更改" placement="top-start" effect="light">
            <el-input type="text" v-model="bindAccount.username" disabled/>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="密码" required>
          <el-input type="password" v-model="bindAccount.password" :disabled="isBind"/>
        </el-form-item>
      </el-form>
    </template>
    <template #footer>
      <div class="text-slate-400	text-xs">
        <span v-if="!isBind">绑定即代表您同意将密码保存在服务器上</span>
        <span v-else>解绑后，你的数据将会从服务器中删除</span>
      </div>
      <div class="my-2">
        <el-button @click="handleOnBindClicked" type="primary" v-if="!isBind">绑定</el-button>
        <el-button @click="handleOnBindClicked" type="danger" v-else>解除绑定</el-button>
        <el-button @click="showBindWindow = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import {computed, onMounted, ref, watchEffect} from 'vue'
import {getUserComprehensiveStatus} from "@/api/comprehensive.ts";
import {useComprehensiveStore, useUserStore} from "@/store";
import {ICourse, ICourseData, IJWXTAccount} from "@/types";
import {ElMessage} from "element-plus";
import {storeToRefs} from "pinia";
import {getJWXTScore} from "@/api/user.ts";
import TDivider from "@/components/dividers/TDivider.vue";

const isComplete = ref<boolean>(false)
const isBind = ref<boolean>(false)
const showBindWindow = ref<boolean>(false)
const loading = ref<boolean>(true)
const store = useComprehensiveStore()
const user = useUserStore()
const scoreData = ref<ICourseData>()

const bindAccount = ref<IJWXTAccount>({
  username: "",
  password: ""
})

const handleShowBindWindow = () => {
  showBindWindow.value = true
  bindAccount.value.username = user.user.account
}

const {jwxt_user} = storeToRefs(user)

const handleOnBindClicked = async () => {
  if (!isBind.value) {
    // 绑定操作
    try {
      await user.bindJWXTInfo(bindAccount.value)
      isBind.value = true
      showBindWindow.value = false
    } catch (e: any) {
      ElMessage({
        type: 'error',
        message: e.detail ?? e
      })
    }
  } else {
    // 解绑操作
    await user.deleteJWXTInfo()
    isBind.value = false
    showBindWindow.value = false
    ElMessage({
      type: 'success',
      message: '解绑成功'
    })
  }
}

const scoreList = computed((): ICourse[] => {
  if (!scoreData.value) return [];
  return Object.values(scoreData.value).flat();
});

watchEffect(async () => {
  try {
    scoreData.value = await getJWXTScore(store.getSemester) ?? {};
  } catch (e: any) {
    ElMessage({
      type: 'error',
      message: e.detail ?? e
    })
  }
});

onMounted(async () => {
  await store.update()
  await user.updateJWXTInfo()
  if (user.jwxt_bind)
    isBind.value = true
  isComplete.value = await getUserComprehensiveStatus(store.getSemester)
  loading.value = false
})
</script>

<style scoped>

</style>