<template>
  <div>
    <p class="text-sm font-medium text-gray-900">填写综合素质评价报表</p>
    <div class="mt-6" aria-hidden="true">
      <div class="overflow-hidden rounded-full bg-gray-200">
        <div class="h-2 rounded-full bg-indigo-600 transition-all duration-500"
             :style="`width: ${assessmentStep.progress}%`"/>
      </div>
      <div class="mt-6 hidden grid-cols-4 text-sm font-medium text-gray-600 sm:grid">
        <div :class="{'text-indigo-600': assessmentStep.step >= 1}">确认你的信息</div>
        <div class="text-center" :class="{'text-indigo-600': assessmentStep.step >= 2}">填写报表</div>
        <div class="text-center" :class="{'text-indigo-600': assessmentStep.step >= 3}">提交预览</div>
        <div class="text-right" :class="{'text-indigo-600': assessmentStep.step >= 4}">提交</div>
      </div>
    </div>
  </div>
  <div class="container mx-auto mt-5">
    <div class="container" v-if="assessmentStep.step === 1">
      <el-descriptions
          :title="`开始前请核对信息, 目前正在进行的是${comprehensiveStore.getTitle}`"
          direction="vertical"
          :column="4"
          border
      >
        <el-descriptions-item label="姓名">{{ userStore.getName }}</el-descriptions-item>
        <el-descriptions-item label="班级">{{ userStore.getClassName }}</el-descriptions-item>
        <el-descriptions-item label="学号" :span="2">{{ userStore.getSerialNumber }}</el-descriptions-item>
        <el-descriptions-item label="职务">{{ userStore.getDuty }}</el-descriptions-item>
        <el-descriptions-item label="确认">
          <el-checkbox v-model="assessmentStep.stepOneConfirm"
                       label="我已核对基本信息确认无误，并已知晓当前期综测通知。"/>
        </el-descriptions-item>
      </el-descriptions>
      <el-button type="primary" class="mt-2 float-right" :disabled="!assessmentStep.stepOneConfirm"
                 @click="handleNextStep(1)">
        下一步
      </el-button>
    </div>
    <div class="container" v-else-if="assessmentStep.step === 2">
      <el-collapse>
        <el-collapse-item v-for="item in comprehensiveFormTemplate" :key="item.subject">
          <template #title>
            <span class="text-base font-bold">{{ item.subject }}</span>
          </template>
          <el-form>
            <t-divider class="mt-2" position="center">
              <template #title>
                <el-tag type="success" effect="dark">加分项目</el-tag>
              </template>
            </t-divider>
            <div class="container divide-y divide-dashed">
              <div v-for="(add, index) in item.add" :key="index" class="mb-2 pt-2">
                <div class="flex justify-between">
                  <div>
                <span class="text-base">
                <span class="font-bold">{{ add.serial_number }}</span>
                <span>{{ add.title }}</span>
              </span>
                  </div>
                  <div>
                    <el-button circle :icon="PlusIcon" title="添加" @click="handleAddClicked(add.serial_number!)"/>
                  </div>
                </div>
                <div class="flex flex-col animate__animated animate__fadeIn"
                     v-for="(content, index) in comprehensiveFormList!.get(add.serial_number!)!.data">
                  <div class="flex justify-between my-2">
                    <div class="flex gap-2">
                      <el-form-item label="明细" v-if="add.sub">
                        <el-select v-model="content.select" :disabled="content.disabled">
                          <el-option v-for="ii in add.sub" :key="ii.title!" :title="ii.title!" :value="ii.title!"/>
                        </el-select>
                      </el-form-item>
                      <el-form-item label="内容">
                        <el-input :disabled="content.disabled" v-model="content.content"
                                  placeholder="请输入说明性文字"/>
                      </el-form-item>
                      <el-form-item label="分值">
                        <el-input :disabled="content.disabled" v-model="content.score" type="number"/>
                      </el-form-item>
                    </div>
                    <el-button circle type="danger" :icon="TrashIcon"
                               @click="handleFormItemDelete(add.serial_number!, index)"/>
                  </div>
                  <el-form-item label="" v-if="!add.no_evidence">
                    <el-upload ref="uploadRef"
                               action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                               :auto-upload="false">
                      <template #trigger>
                        <el-button type="primary" round :icon="PlusIcon">添加佐证材料</el-button>
                      </template>

                      <template #default>
                        <el-button class="ml-3" type="success" @click="" :icon="ArrowUpTrayIcon" round>上传</el-button>
                      </template>

                      <template #tip>
                        <div class="el-upload__tip">
                          仅支持上传图片
                        </div>
                      </template>
                    </el-upload>
                  </el-form-item>
                </div>
              </div>
            </div>
            <t-divider class="my-2" position="center">
              <template #title>
                <el-tag type="danger" effect="dark">扣分项目</el-tag>
              </template>
            </t-divider>
          </el-form>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>


<script setup lang="ts">
import {onMounted, ref} from "vue";
import {IComprehensiveFormTemplate} from "@/types";
import {getComprehensiveFormTemplate} from "@/api/comprehensive.ts";
import {useComprehensiveStore, useUserStore} from "@/store";
import {ElMessage} from "element-plus";
import TDivider from "@/components/dividers/TDivider.vue";
import {PlusIcon, ArrowUpTrayIcon, TrashIcon} from "@heroicons/vue/20/solid"
import {integer} from "@vue/language-server";
import FormItem from "@/components/formitem/FormItem.vue";

const comprehensiveStore = useComprehensiveStore()
const userStore = useUserStore()
const assessmentStep = ref({
  progress: 0,
  step: 1,
  stepOneConfirm: false,
  stepTwoConfirm: false,
  stepThreeConfirm: false,
  stepFourConfirm: false,
})

type FormListType = "select" | "text"

interface FormListItem {
  type: FormListType,
  single: boolean
  data: any[]
}

const comprehensiveFormTemplate = ref<IComprehensiveFormTemplate[]>([])
const comprehensiveFormList = ref<Map<string, FormListItem>>()

const handleNextStep = async (step: number) => {
  switch (step) {
    case 1:
      if (!assessmentStep.value.stepOneConfirm)
        return
      if (!comprehensiveStore.checkAvailable) {
        ElMessage({
          type: "warning",
          message: "本期综测还未开始或已结束，请关注综测时间！"
        })
        return
      }
      assessmentStep.value.step += 1
      assessmentStep.value.progress = 37.5
      break
  }
}

const handleAddClicked = (sn: string) => {
  let l = comprehensiveFormList.value!.get(sn)
  if (!l) return
  if (l.single && l.data.length === 1) {
    ElMessage({
      type: "warning",
      message: "该项仅能添加一次，不可多加!"
    })
    return
  }
  let obj;
  if (l.type === 'text') {
    obj = {
      codename: "",
      content: "",
      score: 0,
      disabled: false
    }
  } else if (l.type === 'select') {
    obj = {
      codename: "",
      select: "",
      content: "",
      score: 0,
      disabled: false
    }
  }
  if (sn === '1.2.2') {
    obj.disabled = true
    const duty = userStore.getDuty
    obj.content = duty
    if (duty === '无') {}
    else if (duty === '班长' || duty === '团支书' || duty === '班助') {
      obj.select = '一级干部'
      obj.score = 5}
    else if (duty === '宿舍长') {
      obj.select = '宿舍长、其他班委会委员'
      obj.score = 2
    }
    else {
      obj.select = '三级干部'
      obj.score = 3
    }
  }
  l.data.push(obj)
}

const handleGetComprehensiveFormList = (): Map<string, FormListItem> => {
  let map: Map<string, FormListItem> = new Map()
  for (const item of comprehensiveFormTemplate.value) {
    for (const addElement of item.add) {
      let obj: FormListItem = {
        type: "text",
        single: false,
        data: []
      }
      if (addElement.sub) obj.type = "select"
      if (addElement.single) obj.single = true
      map.set(addElement.serial_number!, obj)
    }
  }
  return map
}

const handleFormItemDelete = (sn: string, index: integer) => {
  let l = comprehensiveFormList.value!.get(sn)
  if (!l) return
  l.data.splice(index, 1)
}

onMounted(() => {
  getComprehensiveFormTemplate().then(res => {
    comprehensiveFormTemplate.value = res
    comprehensiveFormList.value = handleGetComprehensiveFormList()
  })
})
</script>

<style scoped>

</style>