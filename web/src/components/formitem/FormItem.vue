<script setup lang="ts">
import {ArrowUpTrayIcon, PlusIcon, TrashIcon} from "@heroicons/vue/20/solid"

defineProps(['subject'])
</script>

<template>
  <div class="flex justify-between">
    <div>
                <span class="text-base">
                <span class="font-bold">{{ subject.serial_number }}</span>
                <span>{{ subject.title }}</span>
              </span>
    </div>
    <div>
      <el-button circle :icon="PlusIcon" title="添加" @click="handleAddClicked(subject.serial_number!)"/>
    </div>
  </div>
  <div class="flex flex-col animate__animated animate__fadeIn"
       v-for="(content, index) in comprehensiveFormList!.get(subject.serial_number!)!.data">
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

</template>

<style scoped>

</style>