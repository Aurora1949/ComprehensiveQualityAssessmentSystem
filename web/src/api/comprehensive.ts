import {request} from "@/api/request.ts";
import {
  ICommonResponse,
  IComprehensive,
  IComprehensiveData,
  IComprehensiveFormTemplate,
  ICurrentComprehensive
} from "@/types";

export async function getAllComprehensive() {
  return request<IComprehensive[]>({
    url: '/admin/comprehensive/queryAll',
    method: 'GET'
  })
}

export async function getCurrentComprehensive() {
  return request<ICurrentComprehensive>({
    url: '/user/comprehensive/query',
    method: 'GET'
  })
}

export async function createNewComprehensive(c: IComprehensive) {
  return request<ICommonResponse>({
    url: '/admin/comprehensive/create',
    method: "POST",
    data: c
  })
}

export async function changeCurrentComprehensive(semester: string) {
  return request({
    url: '/admin/comprehensive/setCurrent',
    method: 'post',
    data: {semester}
  })
}

export async function getComprehensiveFormTemplate() {
  return request<IComprehensiveFormTemplate[]>({
    url: '/user/comprehensive/getForm',
    method: 'get'
  })
}

export async function saveComprehensiveFormData(formData: IComprehensiveData[], semester: string, saveDraft: boolean) {
  return request<null>({
    url: '/user/comprehensive/save',
    method: 'post',
    data: {data: formData, semester, draft: saveDraft},
  })
}

export async function getComprehensiveFormData(semester: string) {
  return request<IComprehensiveData[]>({
    url: '/user/comprehensive/getData',
    method: 'get',
    params: {semester}
  })
}

export async function getUserComprehensiveStatus(semester: string) {
  return request<boolean>({
    url: '/user/comprehensive/available',
    method: 'get',
    params: {semester}
  })
}
