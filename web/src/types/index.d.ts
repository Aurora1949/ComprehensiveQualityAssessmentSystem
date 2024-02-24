export interface IUserLogin {
  username: string
  password: string
}

hbnv

export interface IToken {
  access_token: string
  token_type: string
}

export interface IUser {
  account: string
  auth: number
  is_active: boolean
  extend?: IUserExtend
}

export interface IUserExtend {
  name: string
  duties: string | null
  gender: number
  class_name: string
  uid: string
}

export interface IUserPageList {
  items: IUser[]
  total: number
  page: number
  size: number
  pages: number
}

export interface IUserPageListParam {
  class_name: string
  base_user_level: number
  page: number
  size: number
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
  per_time: number | null
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
  upload: string | null
}

export interface IIUploadFileResponse {
  filename: string
  hashed_filename: string
}

export interface IJWXTAccount {
  username: string
  password: string
}

export interface IJWXTUser {
  uid: string
  faculty: string
  specialty: string
  education_level: string
  eductional_systme: string
}

export interface ICourse {
  credit: number;
  score: number | string; // 成绩可能是数字或字符串（如“优秀”、“良好”等）
  lesson_name: string;
  point: number;
  bkcj?: string; // 补考成绩，可选属性
  cxcj?: string; // 重修成绩，可选属性
}

export interface ICourseData {
  [semester: string]: ICourse[]; // 使用索引签名，以适应不同的学期
}

export interface IErrType {
  detail: object
}

export interface IUserComprehensiveStatusWithClassName {
  account: string,
  status: boolean | null,
  class_name: string,
  name: string
}

export interface page<T> {
  items: T[],
  total: number,
  page: number,
  size: number,
  pages: number
}

export interface IDistributeJobData {
  semester: string
  admin_id: string
  user_id_list: string[]
}

export interface IComprehensiveJob {
  name: string
  class_name: string
  account: string
  submit_status: boolean
  distribute_status: number
}
