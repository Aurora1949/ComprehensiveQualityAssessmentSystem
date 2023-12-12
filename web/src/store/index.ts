import {defineStore} from "pinia"
import {User} from "@/types/user.ts";
import {getUserInfo} from "@/api/user.ts";
import {ICurrentComprehensive} from "@/types";
import {getCurrentComprehensive} from "@/api/comprehensive.ts";

export const useUserStore = defineStore('user', {
  state: () => ({
    user: new User()
  }),
  getters: {
    getName(): string {
      return this.user.extend ? this.user.extend.name : "null"
    },
    getSerialNumber(): string {
      return this.user.account
    },
    getClassName(): string {
      return this.user.extend ? this.user.extend.class_name : "null"
    },
    getDuty(): string {
      return this.user.extend ? this.user.extend.duties ? this.user.extend.duties : "无" : "无"
    }
  },
  actions: {
    async updateUserInfo() {
      await getUserInfo().then(res => {
        this.user.update(res)
      }).catch(err => Promise.reject(err))
    }
  },
})

type Status = "success" | "info" | "warning" | "danger" | "";

export enum ComprehensiveStatus {
  NotBegin,
  InProgress,
  End
}

export const useComprehensiveStore = defineStore('comprehensive', {
  state: () => ({
    currentComprehensive: {
      semester: '',
      detail: {
        title: '',
        start_date: '',
        end_date: '',
        semester: '',
      }
    } as ICurrentComprehensive
  }),
  getters: {
    getTagText(): { type: Status, msg: string } {
      if (!this.currentComprehensive.detail.start_date && !this.currentComprehensive.detail.end_date)
        return {
          type: "info",
          msg: "null"
        }
      switch (this.checkAvailable) {
        case ComprehensiveStatus.NotBegin:
          return {
            type: "warning",
            msg: "未开始"
          }
        case ComprehensiveStatus.InProgress:
          return {
            type: "success",
            msg: "进行中"
          }
        case ComprehensiveStatus.End:
          return {
            type: "danger",
            msg: "已结束"
          }
      }
    },
    getTitle(): string {
      return this.currentComprehensive.detail.title ? this.currentComprehensive.detail.title : '无'
    },
    getSemester(): string {
      return this.currentComprehensive.semester
    },
    checkAvailable(): ComprehensiveStatus {
      const startDate = new Date(this.currentComprehensive.detail.start_date)
      const endDate = new Date(this.currentComprehensive.detail.end_date)
      const nowDate = new Date()
      if (startDate > nowDate) return ComprehensiveStatus.NotBegin
      else if (endDate < nowDate) return ComprehensiveStatus.End
      return ComprehensiveStatus.InProgress
    }
  },
  actions: {
    async update() {
      try {
        this.currentComprehensive = await getCurrentComprehensive()
      } catch (e) {
        console.log(e);
      }
    }
  }
})