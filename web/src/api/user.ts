import {request} from "@/api/request.ts";
import {
  ICommonResponse,
  ICourseData,
  IIUploadFileResponse,
  IJWXTAccount,
  IJWXTUser,
  IUser,
  IUserPageList,
  IUserPageListParam
} from "@/types";

export async function getUserInfo() {
  return request<IUser>({
    url: '/user/me',
    method: 'get'
  })
}

export async function getUserList(param: IUserPageListParam) {
  return request<IUserPageList>({
    url: '/admin/get/userList',
    params: param,
    method: 'get'
  })
}

export async function adminResetUserPassword(uid: string) {
  return request<ICommonResponse>({
    url: '/admin/user/resetPasswd',
    params: {
      uid: uid
    },
    method: 'get'
  })
}

export async function adminModifyUserInfo(user: IUser) {
  return request<ICommonResponse>({
    url: '/admin/user/modify',
    method: 'post',
    data: user
  })
}

export async function adminUserCreate(user: IUser) {
  return request<ICommonResponse>({
    url: '/admin/user/create',
    method: 'post',
    data: user
  })
}

export async function uploadFile(formData: FormData) {
  return request<IIUploadFileResponse>({
    url: '/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    },
  })
}

export async function getBindData() {
  return request<IJWXTUser | null>({
    url: '/user/bind/info',
    method: 'get'
  })
}

export async function bindJWXT(jwxt_user: IJWXTAccount) {
  return request<IJWXTUser>({
    url: '/user/bind',
    method: "post",
    data: jwxt_user
  })
}

export async function deleteJWXT() {
  return request({
    url: '/user/bind',
    method: 'delete'
  })
}

export async function getJWXTScore(semester: string) {
  return request<ICourseData | null>({
    url: '/user/bind/score',
    method: 'get',
    params: {semester}
  })
}

export async function getAdminUserIDList() {
  return request<string[]>({
    url: '/admin/query/admin',
    method: 'get'
  })
}

