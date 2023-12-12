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
    <!--  Step 1. 信息确认  -->
    <div class="container" v-if="assessmentStep.step === 1">
      <el-descriptions
          :title="`开始前请核对信息, 你正在填写的是${comprehensiveStore.getTitle}`"
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
    <!--  Step 2. 填写报表  -->
    <div class="container" v-else-if="assessmentStep.step === 2">
      <el-collapse>
        <el-collapse-item v-for="item in comprehensiveFormTemplate" :key="item.subject">
          <template #title>
            <span class="text-base font-bold">{{ item.subject }}</span>
          </template>
          <el-form>
            <t-divider class="mt-2" position="center">
              <template #title>
                <el-tag type="success" effect="dark" round>加分项目</el-tag>
              </template>
            </t-divider>
            <div class="container divide-y divide-dashed">
              <div v-for="(add, index) in item.add" :key="index" class="mb-2 pt-2">
                <form-item :subject="add" :c-form-list="comprehensiveFormList!" @addClicked="handleAddClicked"
                           @deleteClicked="handleFormItemDelete"/>
              </div>
            </div>
            <t-divider class="my-2" position="center">
              <template #title>
                <el-tag type="danger" effect="dark" round>扣分项目</el-tag>
              </template>
            </t-divider>
            <div class="divide-y divide-dashed">
              <div class="mb-2 pt-2" v-for="(sub, index) in item.subtract" :key="index">
                <form-item :subject="sub" :c-form-list="comprehensiveFormList!" @addClicked="handleAddClicked" @deleteClicked="handleFormItemDelete"/>
              </div>
            </div>
          </el-form>
        </el-collapse-item>
      </el-collapse>
      <div class="sticky bottom-0 bg-white border-t border-dashed">
        <div class="flex justify-end py-4">
          <el-button @click="saveAsDraft" class="my-2">保存为草稿</el-button>
          <el-button type="primary" @click="handleNextStep(2)" class="my-2">下一步</el-button>
        </div>
      </div>
    </div>
    <!--  Step 3. 预览报表  -->
    <div v-if="assessmentStep.step === 3">
      <div v-for="({subject}, index) in comprehensiveFormTemplate">
        <t-divider :title="subject"/>
        <div v-for="([key, item], cIndex) in getComprehensiveMapByIndex(index)" :key="cIndex">
          <div v-if="item.data.length">
            <div>{{ key }} {{ lookForTitle(key) }}</div>
            <ul>
              <li class="pl-4" v-for="i in item.data" :key="i">
                描述: {{ i.content }}
                分值: <span class="font-bold"
                            :class="{'text-green-600': item.isAdd, 'text-red-600': !item.isAdd}">{{ i.score }}</span>
              </li>
            </ul>
          </div>
        </div>
        <span class="font-bold">总计: {{ getTotalScore(index) }}</span>
      </div>
      <div class="flex justify-end">
        <el-button @click="handleNextStep(1)" class="">上一步</el-button>
        <el-button @click="handleSubmitForm" type="primary" class="ml-2">提交</el-button>
      </div>
    </div>
    <!--  Step 4. 提交成功  -->
    <div v-if="assessmentStep.step === 4">
      <el-result icon="success" title="提交成功" sub-title="等待评议小组审核，等待期间报表内容不可修改" />
    </div>
  </div>
</template>


<script setup lang="ts">
import {onMounted, ref} from "vue";
import {IComprehensiveData, IComprehensiveFormTemplate, IConductScorecard} from "@/types";
import {
  getComprehensiveFormData,
  getComprehensiveFormTemplate, getUserComprehensiveStatus,
  saveComprehensiveFormData
} from "@/api/comprehensive.ts";
import {ComprehensiveStatus, useComprehensiveStore, useUserStore} from "@/store";
import {ElMessage} from "element-plus";
import TDivider from "@/components/dividers/TDivider.vue";
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

export type FormListType = "select" | "text"

export interface Standard {
  per_time: number | null,
  standard: number[]
}

export interface FormListItem {
  type: FormListType,
  single: boolean
  data: DataItem[]
  standard: Map<string, Standard>
  isAdd: boolean
  codename: string | null
}

const comprehensiveFormTemplate = ref<IComprehensiveFormTemplate[]>([])
const comprehensiveFormList = ref<Map<string, FormListItem>>()
const comprehensiveUserStatus = ref<boolean>(true)

const handleNextStep = (step: number) => {
  switch (step) {
    case 1:
      if (!assessmentStep.value.stepOneConfirm)
        return
      switch (comprehensiveStore.checkAvailable) {
        case ComprehensiveStatus.NotBegin:
          ElMessage({
            type: "warning",
            message: "本期综测还未开始，请关注综测时间！"
          })
          return
        case ComprehensiveStatus.End:
          ElMessage({
            type: "error",
            message: "本期综测已结束，请关注综测时间！"
          })
          return
      }
      assessmentStep.value.step = 2
      assessmentStep.value.progress = 37.5
      break
    case 2:
      assessmentStep.value.step = 3
      assessmentStep.value.progress = 62.5
      break
    case 3:
      assessmentStep.value.step = 4
      assessmentStep.value.progress = 100
  }
}

interface DutyMapping {
  select: string;
  score: number;
}

interface DataItem {
  codename: string | null
  content: string
  score: number
  disabled: boolean
  select?: string
}

const validateClick = (item: FormListItem): boolean => {
  const dataList = item.data
  if (dataList.length && (!dataList[dataList.length - 1].content || !dataList[dataList.length - 1].score)) {
    ElMessage({
      type: "warning",
      message: "上一项描述或分值未填，不能添加下一项！"
    })
    return false
  }
  if (!item || (item.single && item.data.length === 1)) {
    ElMessage({
      type: "warning",
      message: "该项仅能添加一次，不可多加!"
    });
    return false
  }
  return true
}

const handleAddClicked = (sn: string) => {
  const listItem: FormListItem = comprehensiveFormList.value!.get(sn)!;
  if (!validateClick(listItem)) return

  let obj: DataItem = {
    codename: listItem.codename,
    content: "",
    score: 0,
    disabled: false,
    select: listItem.type === 'select' ? "" : undefined,
  };

  if (sn === '1.2.2') {
    obj = handleSpecialCase(obj, userStore.getDuty);
  }

  listItem.data.push(obj);
};

const handleSpecialCase = (obj: DataItem, duty: string): DataItem => {
  obj.disabled = false;
  obj.content = duty;

  if (duty === '无') {
    return obj;
  }

  const dutyMapping: Record<string, DutyMapping> = {
    '班长': {select: 'yijiganbu', score: 5},
    '团支书': {select: 'yijiganbu', score: 5},
    '班助': {select: 'yijiganbu', score: 5},
    '宿舍长': {select: 'susheizhang', score: 2},
    // Add other mappings as needed
  };

  return {...obj, ...dutyMapping[duty] || {select: 'sanjiganbu', score: 3}};
};

const createFormListItem = (scorecard: IConductScorecard, type: string): FormListItem => ({
  type: scorecard.sub ? "select" : "text",
  single: scorecard.single,
  data: [],
  standard: new Map<string, Standard>,
  isAdd: type === 'add',
  codename: scorecard.codename
});

const addSavedDataToList = (list: FormListItem, savedMap: Map<string, { score: number, content: string }[]>, codename: string, type: string | null) => {
  const savedItem = savedMap.get(codename)
  if (!savedItem) return
  for (const item of savedItem) {
    list.data.push({
    codename: codename,
    content: item.content,
    disabled: false,
    score: item.score,
    select: type ?? undefined
  })
  }
}

const processScorecards = (scorecards: IConductScorecard[], map: Map<string, FormListItem>, type: string, savedMap: Map<string, { score: number, content: string }[]>) => {
  for (const scorecard of scorecards) {
    if (!scorecard.serial_number) continue
    const listItem = createFormListItem(scorecard, type);
    map.set(scorecard.serial_number, listItem);

    if (scorecard.codename) addSavedDataToList(listItem, savedMap, scorecard.codename, null)

    if (!scorecard.sub) continue
    for (const iConductScorecard of scorecard.sub) {
      if (iConductScorecard.codename) addSavedDataToList(listItem, savedMap, iConductScorecard.codename, iConductScorecard.codename)
      listItem.standard.set(iConductScorecard.codename!, {
        per_time: iConductScorecard.per_time,
        standard: iConductScorecard.standard!
      })
    }
  }
};

const handleGetComprehensiveFormList = async () => {
  const formListMap: Map<string, FormListItem> = new Map();
  const savedDataMap = await getSavedDataMap()

  for (const templateItem of comprehensiveFormTemplate.value) {
    processScorecards(templateItem.add, formListMap, 'add', savedDataMap);
    processScorecards(templateItem.subtract, formListMap, '', savedDataMap);
  }

  return formListMap;
};

const handleFormItemDelete = (sn: string, index: integer) => {
  let l = comprehensiveFormList.value!.get(sn)
  if (!l) return
  l.data.splice(index, 1)
}

const lookForTitle = (sn: string): string => {
  const index = parseInt(sn.split('.')[0]) - 1
  const comprehensive = comprehensiveFormTemplate.value[index]
  const lst = [...comprehensive.add, ...comprehensive.subtract]
  for (const o of lst) {
    if (o.serial_number === sn) return o.title
  }
  return ""
}

const getTotalScore = (index: number): number => {
  let total = 0
  const sIndex = String(index + 1)
  for (const [key, value] of comprehensiveFormList.value!) {
    if (key.split('.')[0] !== sIndex) continue
    for (const i of value.data) {
      total += value.isAdd ? parseFloat(String(i.score)) : -1 * parseFloat(String(i.score))
    }
  }
  return total
}

const getComprehensiveMapByIndex = (index: number): Map<string, FormListItem> => {
  let map: Map<string, FormListItem> = new Map()
  for (const [k, v] of comprehensiveFormList.value!) {
    if (k.split('.')[0] !== String(index + 1)) continue
    map.set(k, v)
  }
  return map
}

const saveAsDraft = async () => {
  const data = getComprehensiveDataList()
  try {
    await saveComprehensiveFormData(data, comprehensiveStore.getSemester, true)
    ElMessage({
      "type": "success",
      "message": "保存成功"
    })
  } catch (e) {
    ElMessage({
      "type": "error",
      "message": "出错啦"
    })
  }
}

const getComprehensiveDataList = (): IComprehensiveData[] => {
  let lst: IComprehensiveData[] = []
  for (const [_, {data}] of comprehensiveFormList.value!) {
    if (!data.length) continue
    for (const item of data) {
      lst.push({
        codename: item.codename ?? item.select!,
        content: item.content,
        score: parseFloat(String(item.score))
      })
    }
  }
  return lst
}

const handleSubmitForm = async () => {
  const data = getComprehensiveDataList()
  try {
    await saveComprehensiveFormData(data, comprehensiveStore.getSemester, false)
    handleNextStep(3)
  } catch (e) {
    console.log(e)
  } finally {
    console.log(data)
  }
}

const getSavedDataMap = async () => {
  try {
    const savedData = await getComprehensiveFormData(comprehensiveStore.getSemester)
    const map = new Map<string, { score: number, content: string }[]>()
    for (const item of savedData) {
      let mItem = map.get(item.codename)
      if (mItem) mItem.push({score: item.score, content: item.content})
      else map.set(item.codename, [{score: item.score, content: item.content}])
    }
    return map
  } catch (e) {
    throw e
  }
}

onMounted(async () => {
  try {
    comprehensiveUserStatus.value = await getUserComprehensiveStatus(comprehensiveStore.getSemester)
    if (!comprehensiveUserStatus.value) {
      handleNextStep(3)
      return
    }
    comprehensiveFormTemplate.value = await getComprehensiveFormTemplate()
    comprehensiveFormList.value = await handleGetComprehensiveFormList()
  } catch (e) {
    console.log(e)
  }
})
</script>

<style scoped>

</style>