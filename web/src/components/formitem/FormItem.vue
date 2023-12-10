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
          <el-input :disabled="content.disabled" v-model="content.score" type="number" :min="0"/>
        </el-form-item>
      </div>
      <el-button circle type="danger" :icon="TrashIcon" @click="handleFormItemDelete(subject.serial_number!, index)"/>
    </div>
    <el-form-item label="" v-if="!subject.no_evidence">
      <el-upload ref="uploadRef" action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" :auto-upload="false">
        <template #trigger>
          <el-button type="primary" round :icon="PlusIcon">添加佐证材料</el-button>
        </template>

        <template #default>
          <el-button class="ml-3 flex" type="success" @click="" :icon="ArrowUpTrayIcon" round>上传</el-button>
        </template>

        <template #tip>
          <div class="el-upload__tip">
            仅支持上传图片
          </div>
        </template>
      </el-upload>
    </el-form-item>
  </div>

</template>

<script setup lang="ts">
import {ArrowUpTrayIcon, PlusIcon, TrashIcon} from "@heroicons/vue/20/solid"
import {IConductScorecard} from "@/types";
import {FormListItem} from "@/views/panel/child/PanelAssessmentView.vue";

defineProps<{
  subject: IConductScorecard
  cFormList: Map<string, FormListItem>
}>()

const emit = defineEmits(['addClicked', 'deleteClicked'])

const handleOnAddClicked = (serialNumber: string) => {
  emit('addClicked', serialNumber)
}

const handleFormItemDelete = (serialNumber: string, index: number) => {
  emit("deleteClicked", serialNumber, index)
}
</script>


<style scoped>

</style>