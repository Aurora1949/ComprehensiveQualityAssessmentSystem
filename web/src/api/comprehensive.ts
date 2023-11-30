import {request} from "@/api/request.ts";
import {ICommonResponse, IComprehensive, IComprehensiveFormTemplate, ICurrentComprehensive} from "@/types";

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
