<template>
  <div class="flex justify-between">
    <div>
      <span class="text-base">
        <span class="font-bold">{{ subject.serial_number + " " }}</span>
        <span>{{ subject.title }}</span>
      </span>
    </div>
    <div>
      <el-button circle :icon="PlusIcon" title="添加" @click="handleOnAddClicked(subject.serial_number!)"/>
    </div>
  </div>
  <div class="flex flex-col animate__animated animate__fadeIn" v-for="(content, index) in cFormList!.get(subject.serial_number!)!.data">
    <p class="text-s text-gray-500">
      评分标准:
      <span v-if="!subject.sub">
        <span v-if="subject.per_time">每<span class="font-bold">{{ subject.per_time }}</span>次</span>
        <span class="font-bold">{{ subject.standard!.join("、") }}</span>分
      </span>
      <span v-else>
        <span v-if="cFormList.get(subject.serial_number!).standard.get(content.select!)">
          <span v-if="cFormList.get(subject.serial_number!).standard.get(content.select!).per_time">
            每<span class="font-bold">{{ cFormList.get(subject.serial_number!).standard.get(content.select).per_time }}</span>次</span>
          <span class="font-bold">
            {{ cFormList.get(subject.serial_number).standard.get(content.select).standard.join("、") }}
          </span>分
        </span>
        <span v-else>请选择明细</span>
      </span>
    </p>
    <div class="flex justify-between my-2">
      <div class="flex gap-2">
        <el-form-item label="明细" v-if="subject.sub">
          <el-select v-model="content.select" :disabled="content.disabled">
            <el-option v-for="ii in subject.sub" :key="ii.title!" :label="ii.title!" :value="ii.codename!"/>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input :disabled="content.disabled" v-model="content.content" placeholder="请输入说明性文字"/>
        </el-form-item>
        <el-form-item label="分值">
          <el-input :disabled="content.disabled" v-model="content.score" type="number" @wheel.prevent/>
        </el-form-item>
        <el-form-item>
          <el-button type="danger" v-if="content.upload" @click="handleCleanUpload(content)" link>清除佐证材料</el-button>
        </el-form-item>
      </div>
      <el-button circle type="danger" :icon="TrashIcon" @click="handleFormItemDelete(subject.serial_number!, index)"/>
    </div>
    <el-form-item label="" v-if="!subject.no_evidence && !content.upload">
      <el-upload ref="uploadRef"
                 action="#"
                 :auto-upload="true"
                 :http-request="(options) => {handleUpload(<UploadRequestOptions>options, content)}"
                 :limit="1"
                 :show-file-list="false"
      >
        <template #trigger>
          <el-button type="primary" round :icon="PlusIcon">添加佐证材料</el-button>
        </template>

        <template #tip>
          <div class="el-upload__tip">
            仅支持上传图片
          </div>
        </template>
      </el-upload>
    </el-form-item>
    <el-image v-if="content.upload" class="w-20 h-20" :src="URL + content.upload" :preview-src-list="[URL + content.upload]" />
  </div>

</template>

<script setup lang="ts">
import {ArrowUpTrayIcon, PlusIcon, TrashIcon} from "@heroicons/vue/20/solid"
import {IConductScorecard} from "@/types";
import {FormListItem, DataItem} from "@/views/panel/child/PanelAssessmentView.vue";
import {UploadRequestOptions} from "element-plus";
import {uploadFile} from "@/api/user.ts";


defineProps<{
  subject: IConductScorecard
  cFormList: Map<string, FormListItem>
}>()

const URL = import.meta.env.VITE_API_URL + "/files/"

const emit = defineEmits(['addClicked', 'deleteClicked'])

const handleOnAddClicked = (serialNumber: string) => {
  emit('addClicked', serialNumber)
}

const handleFormItemDelete = (serialNumber: string, index: number) => {
  emit("deleteClicked", serialNumber, index)
}

const handleUpload = async (options: UploadRequestOptions, dataItem: DataItem) => {
  try {
    const formData = new FormData()
    formData.append('file', options.file)
    const {filename, hashed_filename} = await uploadFile(formData)
    dataItem.upload = hashed_filename
  } catch (e) {
    console.log(e)
  }
}

const handleCleanUpload = (dataItem: DataItem) => {
  dataItem.upload = null
}
</script>


<style lang="scss">
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield; /* Firefox */
}

</style>