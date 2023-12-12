import {integer} from "@vue/language-server";

export interface IUserLogin {
  username: string
  password: string
}

export interface IToken {
  access_token: string
  token_type: string
}

export interface IUser {
  account: string
  auth: integer
  is_active: boolean
  extend?: IUserExtend
}

export interface IUserExtend {
  name: string
  duties: string | null
  gender: integer
  class_name: string
  uid: string
}

export interface IUserPageList {
  items: IUser[]
  total: integer
  page: integer
  size: integer
  pages: integer
}

export interface IUserPageListParam {
  class_name: string
  base_user_level: integer
  page: integer
  size: integer
}

export interface ICommonResponse {
  msg: string
}

export interface IComprehensive {
  title: string
  start_date: string
  end_date: string
  semester: string
}

export interface ICurrentComprehensive {
  semester: string
  detail: IComprehensive
}

export interface IConductScorecard {
  serial_number: string | null
  title: string
  codename: string | null
  standard: number[] | null
  sub: IConductScorecard[] | null
  no_evidence: boolean
  single: boolean
  multiple: boolean
  per_time: integer | null
  at: string | null
}

export interface IComprehensiveFormTemplate {
  subject: string
  add: IConductScorecard[]
  subtract: IConductScorecard[]
}

export interface IComprehensiveData {
  codename: string
  content: string
  score: number
}
