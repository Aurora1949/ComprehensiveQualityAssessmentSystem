<template>
  <left-divider title="当前综测"/>
  <el-form label-position="left">
    <p class="text-sm">当前进行的综测学期：<strong>{{ currentComprehensive.semester }}</strong></p>
    <el-form-item label="修改进行的综测学期">
      <el-select v-model="selectCurrentComprehensive" @change="handleOnCurrentChange">
        <el-option v-for="item in comprehensiveList" :key="item.semester" :label="item.title" :value="item.semester"/>
      </el-select>
    </el-form-item>
  </el-form>
  <left-divider title="添加新综测"/>
  <el-form :model="createComprehensive">
    <el-form-item label="标题">
      <el-input placeholder="例如：20xx-20xx学年第x学期综合素质评价" v-model="createComprehensive.title"
      :input-style="'block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'.split(' ')"/>
    </el-form-item>
    <el-form-item label="学年简写">
      <el-input placeholder="例如：20xx-20xx-x" v-model="createComprehensive.semester"/>
    </el-form-item>
    <el-form-item label="开始时间">
      <el-date-picker type="date" value-format="YYYY-MM-DD hh:mm:ss" v-model="createComprehensive.start_date"/>
    </el-form-item>
    <el-form-item label="结束时间">
      <el-date-picker type="date" value-format="YYYY-MM-DD hh:mm:ss" v-model="createComprehensive.end_date"/>
    </el-form-item>
    <el-form-item>
      <el-button @click="handleCreateSubmit" type="primary">添加</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">

import LeftDivider from "@/components/dividers/LeftDivider.vue";
import {onMounted, ref} from "vue";
import {
  changeCurrentComprehensive,
  createNewComprehensive,
  getAllComprehensive,
} from "@/api/comprehensive.ts";
import {IComprehensive} from "@/types";
import {ElMessage} from "element-plus";
import {useComprehensiveStore} from "@/store";
import {storeToRefs} from "pinia";

const comprehensiveStore = useComprehensiveStore()
const comprehensiveList = ref<IComprehensive[]>([])
const {currentComprehensive} = storeToRefs(comprehensiveStore)
const selectCurrentComprehensive = ref<string>("")
const createComprehensive = ref<IComprehensive>({end_date: "", semester: "", start_date: "", title: ""})

const refreshComprehensive = async () => {
  try {
    const allResults = await Promise.all([getAllComprehensive(), comprehensiveStore.update()])
    comprehensiveList.value = allResults[0]
    selectCurrentComprehensive.value = currentComprehensive.value.semester
  } catch (e) {
    console.log(e);
  }
}

const handleCreateSubmit = async () => {
  try {
    const res = await createNewComprehensive(createComprehensive.value)
    ElMessage({
      type: 'success',
      message: res.msg
    })
    await refreshComprehensive()
  } catch (e) {
    console.log(e);
  }
}

// const handleCreateSubmitPromise = () => {
//   createNewComprehensive(createComprehensive.value).then(res => {
//     ElMessage({
//       type: 'success',
//       message: res.msg
//     })
//   }).then(() => {
//     refreshComprehensive()
//   }).catch(e => console.log(e))
// }

const handleOnCurrentChange = async (v: string) => {
  try {
    await changeCurrentComprehensive(v)
    await refreshComprehensive()
  } catch (e) {
    console.log(e);
  }
}

onMounted(async () => {
  await refreshComprehensive()
})
</script>

<style scoped>

</style>