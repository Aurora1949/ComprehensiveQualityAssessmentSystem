import {integer} from "@vue/language-server";

declare interface IUserLogin {
  username: string
  password: string
}

declare interface IToken {
  access_token: string
  token_type: string
}

declare interface IUser {
  account: string
  auth: integer
  is_active: boolean
  extend?: IUserExtend
}

declare interface IUserExtend {
  name: string
  duties: string | null
  gender: integer
  class_name: string
  uid: string
}

declare interface IUserPageList {
  items: IUser[]
  total: integer
  page: integer
  size: integer
  pages: integer
}

declare interface IUserPageListParam {
  class_name: string
  base_user_level: integer
  page: integer
  size: integer
}

declare interface ICommonResponse {
  msg: string
}
