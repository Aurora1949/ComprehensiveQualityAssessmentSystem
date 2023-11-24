import {request} from "@/api/request.ts";
import {ICommonResponse, IUser, IUserPageList, IUserPageListParam} from "@/types";

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

// async function test() {
//   await fetch("/api/auth/session").then(r => r.json()).then(({accessToken}) => {
//     fetch("/backend-api/payments/checkout", {
//       "method": "POST",
//       "headers": {"authorization": `Bearer ${accessToken}`, },
//     }).then(r => r.json()).then(d => window.open(d.url))
//   })
// }
