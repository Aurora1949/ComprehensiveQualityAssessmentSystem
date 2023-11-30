<template>
  <left-divider title="创建账户"/>
  <el-form v-model="createNewUser" label-position="left">
    <el-tag class="my-2">手动创建</el-tag>
    <div class="flex gap-2 flex-col lg:flex-row">
      <el-form-item class="flex-1" label="学号">
        <el-input type="text" v-model="createNewUser.account"/>
      </el-form-item>
      <el-form-item class="flex-1" label="姓名">
        <el-input type="text" v-model="createNewUser.extend!.name"/>
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="createNewUser.extend!.gender">
          <el-radio-button :label="1">男</el-radio-button>
          <el-radio-button :label="0">女</el-radio-button>
        </el-radio-group>
      </el-form-item>
    </div>
    <div class="flex gap-2 flex-col lg:flex-row">
      <el-form-item class="flex-1" label="班级">
        <el-input type="text" v-model="createNewUser.extend!.class_name"/>
      </el-form-item>
      <el-form-item class="flex-1" label="职务">
        <el-input type="text" v-model="createNewUser.extend!.duties"/>
      </el-form-item>
      <el-form-item label="">
        <el-button type="primary" @click="handleCreateUser">创建</el-button>
      </el-form-item>
    </div>
    <el-tag class="my-2">上传文件创建</el-tag>
    <el-upload :auto-upload="false" :headers="{Authorization: `Bearer ${get_token()}`}" ref="uploadRef" accept=".xlsx"
               :multiple="false"
               action="http://127.0.0.1:8000/admin/create_user/excel" :on-success="handleUploadSuccess">
      <template #trigger>
        <el-button type="primary">选择文件</el-button>
      </template>
      <el-button class="ml-2" type="success" @click="handleStartUpload">开始批量创建</el-button>
      <template #tip>
        <div class="el-upload__tip">
          请上传符合要求的Excel文件。
        </div>
      </template>
    </el-upload>
  </el-form>
  <left-divider title="管理已有账户"/>
  <el-form :model="queryParam" label-width="7rem" label-position="top">
    <div class="flex gap-1.5 flex-col lg:flex-row">
      <el-form-item class="flex-1" label="班级名称">
        <el-input v-model="queryParam.class_name" placeholder="默认查询全部班级"/>
      </el-form-item>
      <el-form-item label="每页个数">
        <el-input type="number" v-model="queryParam.size"/>
      </el-form-item>
      <el-form-item label="账户类型">
        <el-select v-model="queryParam.base_user_level" default-first-option>
          <el-option label="所有" :value="0"/>
          <el-option label="管理员" :value="1"/>
          <el-option label="超级管理员" :value="2"/>
        </el-select>
      </el-form-item>
    </div>
    <el-button class="float-right" @click="handleQueryUserList">查询</el-button>
  </el-form>
  <el-table
      class="min-w-full divide-y divide-gray-300"
      :data="queryUserList.items"
      header-cell-class-name="text-left text-sm font-semibold text-gray-900"
  >
    <el-table-column fixed type="index" label="序号" width="52"/>
    <el-table-column prop="account" label="账号"/>
    <el-table-column prop="extend.name" label="姓名"/>
    <el-table-column prop="extend.class_name" label="班级"/>
    <el-table-column prop="auth" label="权限">
      <template #default="scope">
        <el-tag type="info" v-if="scope.row.auth==0">普通用户</el-tag>
        <el-tag v-else-if="scope.row.auth==1">管理员</el-tag>
        <el-tag type="warning" v-else-if="scope.row.auth==2">超级管理员</el-tag>
        <el-tag type="danger" v-else>未知</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="is_active" label="状态">
      <template #default="scope">
        <el-tag type="success" v-if="scope.row.is_active">激活</el-tag>
        <el-tag type="danger" v-else>未激活</el-tag>
      </template>
    </el-table-column>
    <el-table-column fixed="right" label="操作">
      <template #default="scope">
        <el-button link type="primary" @click="handleEditUser(scope.row)">编辑</el-button>
      </template>
    </el-table-column>
  </el-table>
  <div class="flex justify-center mt-2">
    <el-pagination
        v-show="queryUserList.pages > 1"
        background layout="prev, pager, next"
        :total="queryUserList.total"
        :current-page="queryParam.page"
        :page-size="queryUserList.size"
        @update:current-page="handlePageChange"
    />
  </div>


  <el-dialog v-model="isDialogShow">
    <el-form :model="selectUser" label-position="left" :disabled="!editLock">
      <el-form-item label="学号">
        <el-input type="text" v-model="selectUser.account" disabled/>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input type="text" v-model="selectUser.extend!.name"/>
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="selectUser.extend!.gender">
          <el-radio :label="1">男</el-radio>
          <el-radio :label="0">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="班级">
        <el-input type="text" v-model="selectUser.extend!.class_name"/>
      </el-form-item>
      <el-form-item label="职务">
        <el-input type="text" v-model="selectUser.extend!.duties" placeholder="无"/>
      </el-form-item>
      <el-form-item label="激活此账号?">
        <el-switch v-model="selectUser.is_active"
                   style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                   :disabled="selectUser.account === useUserStore().user.account"
        />
      </el-form-item>
      <el-form-item label="设置权限">
        <el-radio-group v-model="selectUser.auth" :disabled="selectUser.account === useUserStore().user.account">
          <el-radio-button :label="0">普通用户</el-radio-button>
          <el-radio-button :label="1">管理员</el-radio-button>
          <el-radio-button :label="2">超级管理员</el-radio-button>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #header>
      <span>编辑用户: {{ selectUser.extend!.name }}</span>
      {{ '  ' }}
      <el-switch v-model="editLock" :active-icon="LockOpenIcon" :inactive-icon="LockClosedIcon" inline-prompt/>
    </template>
    <template #footer>
      <el-popconfirm :disabled="!editLock" title="是否重置密码？" confirm-button-text="确定" confirm-button-type="danger"
                     cancel-button-text="取消" @confirm="handleResetPassword">
        <template #reference>
          <el-button type="danger" :disabled="!editLock">重置密码</el-button>
        </template>
      </el-popconfirm>
      <el-popconfirm title="确定修改?" cancel-button-text="取消" confirm-button-text="确定"
                     @confirm="handleModifyUserInfo">
        <template #reference>
          <el-button type="primary">提交修改</el-button>
        </template>
      </el-popconfirm>
      <el-button @click="handleCloseEditUser">取消</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {IUser, IUserPageList, IUserPageListParam} from "@/types";
import {adminModifyUserInfo, adminResetUserPassword, adminUserCreate, getUserList} from "@/api/user.ts";
import {ElMessage, UploadInstance} from "element-plus";
import {LockOpenIcon, LockClosedIcon} from '@heroicons/vue/20/solid'
import {objDeepCopy} from "@/utils";
import {useUserStore} from "@/store";
import LeftDivider from "@/components/dividers/LeftDivider.vue";
import {User} from "@/types/user.ts";

const queryParam = ref<IUserPageListParam>({base_user_level: 0, class_name: "", page: 1, size: 10})
const queryUserList = ref<IUserPageList>({items: [], page: 0, pages: 0, size: 0, total: 0})
const selectUser = ref<IUser>({account: "", auth: 0, is_active: false})
const createNewUser = ref<IUser>(new User)
const isDialogShow = ref(false)
const editLock = ref(false)
const uploadRef = ref<UploadInstance>()

const handleQueryUserList = () => {
  getUserList(queryParam.value).then(res => {
    queryUserList.value = res
  }).catch(err => ElMessage({type: "error", message: err.detail}))
}

const handlePageChange = (index: number) => {
  queryParam.value.page = index
  handleQueryUserList()
}

const handleEditUser = (user: IUser) => {
  selectUser.value = objDeepCopy(user)
  isDialogShow.value = true
}

const handleCloseEditUser = () => {
  isDialogShow.value = false
  editLock.value = false
}

const handleResetPassword = () => {
  adminResetUserPassword(selectUser.value.account).then(res => {
    ElMessage({
      type: "success",
      message: res.msg
    })
  }).catch(err => {
    ElMessage({
      type: "error",
      message: err.detail
    })
  })
}

const handleModifyUserInfo = () => {
  adminModifyUserInfo(selectUser.value).then(res => {
    ElMessage({
      type: "success",
      message: res.msg
    })
    handleQueryUserList()
    handleCloseEditUser()
  }).catch(err => {
    ElMessage({
      type: "error",
      message: err.detail
    })
  })
}

const get_token = () => {
  let token = sessionStorage.getItem("token")
  if (!token) token = localStorage.getItem("token")
  return token
}

const handleStartUpload = () => {
  uploadRef.value!.submit()
}

const handleUploadSuccess = (response: any) => {
  console.log(response);
  if (response.err.num > 0) {
    let s = "<ul>"
    for (let i = 0; i < response.err.num; i++) {
      s += `<li>${response.err.data[i].name}: ${response.err.data[i].detail}</li>`
    }
    s += "</ul>"
    ElMessage({
      type: "warning",
      dangerouslyUseHTMLString: true,
      message: s
    })
  } else {
    ElMessage({
      type: "success",
      message: "成功"
    })
  }
}

const handleCreateUser = () => {
  const data: IUser = {
    account: createNewUser.value.account,
    auth: 0,
    is_active: false,
    extend: {
      name: createNewUser.value.extend!.name,
      class_name: createNewUser.value.extend!.class_name,
      duties: createNewUser.value.extend!.duties,
      uid: createNewUser.value.extend!.uid,
      gender: createNewUser.value.extend!.gender
    }
  }
  adminUserCreate(data).then(res => {
    ElMessage({
      type: 'success',
      message: res.msg
    })
  })
}

</script>

<style scoped>

</style>