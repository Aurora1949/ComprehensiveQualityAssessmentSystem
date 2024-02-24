<template>
  <div v-if="user.auth>=1">
    <t-divider :title="`我的任务 共${myJobList?.length ?? '0'}个`"/>
    <el-table stripe class="my-4" :data="myJobList" show-overflow-tooltip>
      <el-table-column label="序号" type="index"/>
      <el-table-column label="姓名" prop="name"/>
      <el-table-column label="班级" prop="class_name"/>
      <el-table-column label="学号" prop="account"/>
      <el-table-column label="填报状态" prop="submit_status">
        <template #default="scope">
          <el-tag :type="scope.row.submit_status ? 'success' : 'danger'">
            {{ scope.row.submit_status ? '已填报' : '未填报' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审核状态" prop="distribute_status">
        <template #default="scope">
          <el-tag type="warning" v-if="scope.row.distribute_status==0">待审核</el-tag>
          <el-tag type="success" v-else-if="scope.row.distribute_status==1">已完成</el-tag>
          <el-tag type="info" v-else-if="scope.row.distribute_status==2">驳回</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button
              text
              :type="scope.row.submit_status ? 'primary' : 'info'"
              :disabled="!scope.row.submit_status"
              @click="handleCheckBtn(scope.row)"
          >
            审核
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <div v-if="user.auth>=2">
    <t-divider :title="`任务分配 待分配${distributeJobResponse?.total ?? '0'}个`"/>
    <el-form class="mt-4">
      <el-form-item>
        <el-button type="primary" :disabled="!selectedUserList.length" @click="showDistributeJobDialog = true">分配
        </el-button>
        <span v-show="selectedUserList.length" class="ml-4">已勾选 {{ selectedUserList.length }} 人</span>
      </el-form-item>
    </el-form>
    <el-table stripe class="my-4" :data="distributeJobList" @selection-change="handleSelectChange">
      <el-table-column label="选择" type="selection"/>
      <el-table-column label="姓名" prop="name"/>
      <el-table-column label="班级" prop="class_name"/>
      <el-table-column label="学号" prop="account"/>
      <el-table-column label="填报状态" prop="status">
        <template #default="scope">
          <el-tag :type="scope.row.status ? 'success' : 'danger'">
            {{ scope.row.status ? '已填报' : '未填报' }}
          </el-tag>
        </template>
      </el-table-column>

    </el-table>
    <div class="flex justify-center mt-2">
      <el-pagination background layout="prev, pager, next"
                     :page-count="distributeJobResponse?.pages"
                     @change="pageChange"
                     hide-on-single-page/>
    </div>
  </div>
  <div v-if="user.auth<1">
    <el-empty/>
  </div>

  <el-dialog v-model="showDistributeJobDialog" title="任务分配">
    <p>
      <strong>将以下人员：</strong>
      {{ selectedUserList.map(item => item.name).join('、') }}
    </p>
    <el-form>
      <el-form-item label="分配到">
        <el-select v-model="distributeJobData.admin_id">
          <el-option v-for="item in adminUIDList" :label="item" :value="item"/>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="handleDistributeJobBtn">确定</el-button>
      <el-button class="my-2" @click="showDistributeJobDialog = false">取消</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="showCheckDialog" width="80%">
    <template #header>
      <span>综测核验：{{ curSelectJob?.name }}</span>
    </template>
    <template #default>
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
                <form-item :subject="sub" :c-form-list="comprehensiveFormList!" @addClicked="handleAddClicked"
                           @deleteClicked="handleFormItemDelete"/>
              </div>
            </div>
          </el-form>
        </el-collapse-item>
      </el-collapse>
    </template>
    <template #footer>
      <el-button type="primary">通过</el-button>
      <el-button type="warning">驳回</el-button>
      <el-button type="info">取消</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import {useComprehensiveStore, useUserStore} from "@/store";
import {storeToRefs} from "pinia";
import TDivider from "@/components/dividers/TDivider.vue";
import {computed, onMounted, ref} from "vue";
import {ElMessage} from "element-plus";
import {
  distributeJob,
  getComprehensiveFormData,
  getComprehensiveFormTemplate,
  getDistributeJob,
  getMyJob
} from "@/api/comprehensive.ts";
import {
  IComprehensiveData,
  IComprehensiveFormTemplate,
  IComprehensiveJob,
  IConductScorecard,
  IDistributeJobData,
  IUserComprehensiveStatusWithClassName,
  page
} from "@/types";
import {getAdminUserIDList} from "@/api/user.ts";
import router from "@/router";
import FormItem from "@/components/formitem/FormItem.vue";

const userStore = useUserStore()
const comprehensiveStore = useComprehensiveStore()
const {user} = storeToRefs(userStore)
const perPage = 15

const myJobList = ref<IComprehensiveJob[]>()
const showDistributeJobDialog = ref(false)
const showCheckDialog = ref(false)
const distributeJobResponse = ref<page<IUserComprehensiveStatusWithClassName>>()
const selectedUserList = ref<IUserComprehensiveStatusWithClassName[]>([])
const adminUIDList = ref<string[]>([])
const distributeJobData = ref<IDistributeJobData>({
  admin_id: "",
  semester: "",
  user_id_list: []
})
const distributeJobList = computed(() => distributeJobResponse.value?.items)
const curSelectJob = ref<IComprehensiveJob>()
const curSelectJobData = ref<IComprehensiveData[]>([])

// ! SHIT WARNING =====
interface DutyMapping {
  select: string;
  score: number;
}

type FormListType = "select" | "text"

interface DataItem {
  codename: string | null
  content: string
  score: number
  disabled: boolean
  select?: string
  upload: string | null
}

interface Standard {
  per_time: number | null,
  standard: number[]
}

interface FormListItem {
  type: FormListType,
  single: boolean
  data: DataItem[]
  standard: Map<string, Standard>
  isAdd: boolean
  codename: string | null
}

const comprehensiveFormTemplate = ref<IComprehensiveFormTemplate[]>([])
const comprehensiveFormList = ref<Map<string, FormListItem>>()
// ! ==================

const handleSelectChange = (val: IUserComprehensiveStatusWithClassName[]) => {
  selectedUserList.value = val
}

const handleDistributeJobBtn = async () => {
  distributeJobData.value.semester = comprehensiveStore.getSemester
  distributeJobData.value.user_id_list = selectedUserList.value.map(item => item.account)

  try {
    await distributeJob(distributeJobData.value)
    ElMessage({
      type: 'success',
      message: '分配成功'
    })
    await router.push({name: 'refresh'})
  } catch (e: any) {
    ElMessage({
      type: 'error',
      message: e.detail ?? e
    })
  }
}

const handleCheckBtn = async (select: IComprehensiveJob) => {
  curSelectJob.value = select
  getComprehensiveFormTemplate().then(res => {
    comprehensiveFormTemplate.value = res
    getComprehensiveFormData(comprehensiveStore.getSemester, select.account).then(res => {
      curSelectJobData.value = res
      comprehensiveFormList.value = handleGetComprehensiveFormList()
      showCheckDialog.value = true
    })
  }).catch(e => {
    ElMessage({
      type: 'error',
      message: e.detail ?? e
    })
  })
}

const pageChange = async (currentPage: number) => {
  try {
    distributeJobResponse.value = await getDistributeJob(comprehensiveStore.getSemester, currentPage, perPage)
  } catch (e: any) {
    ElMessage({
      type: 'error',
      message: e.detail ?? e
    })
  }
}

// ! 狗屎警告 ==== 💩💩💩
const getSavedDataMap = () => {
  try {
    const savedData = curSelectJobData.value
    const map = new Map<string, { score: number, content: string, upload: string | null }[]>()
    for (const item of savedData!) {
      let mItem = map.get(item.codename)
      if (mItem) mItem.push({score: item.score, content: item.content, upload: item.upload})
      else map.set(item.codename, [{score: item.score, content: item.content, upload: item.upload}])
    }
    return map
  } catch (e) {
    throw e
  }
}
const createFormListItem = (scorecard: IConductScorecard, type: string): FormListItem => ({
  type: scorecard.sub ? "select" : "text",
  single: scorecard.single,
  data: [],
  standard: new Map<string, Standard>,
  isAdd: type === 'add',
  codename: scorecard.codename
});
const addSavedDataToList = (list: FormListItem, savedMap: Map<string, {
  score: number,
  content: string,
  upload: string | null
}[]>, codename: string, type: string | null) => {
  const savedItem = savedMap.get(codename)
  if (!savedItem) return
  for (const item of savedItem) {
    list.data.push({
      codename: codename,
      content: item.content,
      disabled: false,
      score: item.score,
      select: type ?? undefined,
      upload: item.upload
    })
  }
}
const processScorecards = (scorecards: IConductScorecard[], map: Map<string, FormListItem>, type: string, savedMap: Map<string, {
  score: number,
  content: string,
  upload: string | null
}[]>) => {
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
const handleGetComprehensiveFormList = () => {
  const formListMap: Map<string, FormListItem> = new Map();
  const savedDataMap = getSavedDataMap()

  for (const templateItem of comprehensiveFormTemplate.value!) {
    processScorecards(templateItem.add, formListMap, 'add', savedDataMap);
    processScorecards(templateItem.subtract, formListMap, '', savedDataMap);
  }

  return formListMap;
};
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
    upload: null
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

const handleFormItemDelete = (sn: string, index: number) => {
  let l = comprehensiveFormList.value!.get(sn)
  if (!l) return
  l.data.splice(index, 1)
}
// ! ============ 💩💩💩

onMounted(async () => {
  try {
    const semester = comprehensiveStore.getSemester
    if (!semester)
      await comprehensiveStore.update()
    if (!userStore.user.account)
      await userStore.updateUserInfo()
    if (userStore.user.auth >= 2) {
      distributeJobResponse.value = await getDistributeJob(comprehensiveStore.getSemester, 1, perPage)
      adminUIDList.value = await getAdminUserIDList()
    }
    myJobList.value = await getMyJob(comprehensiveStore.getSemester)
  } catch (e: any) {
    ElMessage({
      type: 'error',
      message: e.detail ?? e
    })
  }
})
</script>

<style scoped>

</style>
