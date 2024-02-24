import {IJWXTUser, IUser, IUserExtend} from "@/types/index";

export class User implements IUser {
  account: string;
  auth: AUTH;
  extend?: UserExtend;
  is_active: boolean;

  constructor() {
    this.account = "";
    this.auth = AUTH.USER;
    this.extend = new UserExtend;
    this.is_active = false;
  }

  update(user: IUser) {
    this.account = user.account
    this.auth = user.auth
    this.extend = user.extend
    this.is_active = user.is_active
  }
}

class UserExtend implements IUserExtend {
  class_name: string;
  duties: string | null;
  gender: GENDER;
  name: string;
  uid: string;


  constructor() {
    this.class_name = "";
    this.duties = null;
    this.gender = GENDER.FEMALE;
    this.name = "";
    this.uid = "";
  }
}

export enum AUTH {
  USER,
  ADMIN,
  SUPER_ADMIN
}

export enum GENDER {
  FEMALE,
  MALE
}

export class JWXTUser implements IJWXTUser {
  education_level: string;
  eductional_systme: string;
  faculty: string;
  specialty: string;
  uid: string;

  constructor(education_level = "", eductional_systme = "", faculty = "", specialty = "", uid = "") {
    this.education_level = education_level
    this.eductional_systme = eductional_systme
    this.faculty = faculty
    this.specialty = specialty
    this.uid = uid
  }

}
