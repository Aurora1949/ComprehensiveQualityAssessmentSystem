import {defineStore} from "pinia"
import {User} from "@/types/user.ts";
import {getUserInfo} from "@/api/user.ts";
import {ICurrentComprehensive} from "@/types";
import {getCurrentComprehensive} from "@/api/comprehensive.ts";

export const useUserStore = defineStore('user', {
  state: () => ({
    user: new User()
  }),
  getters: {},
  actions: {
    async updateUserInfo() {
      await getUserInfo().then(res => {
        this.user.update(res)
      }).catch(err => Promise.reject(err))
    }
  },
})

type Status = "success" | "info" | "warning" | "danger" | "";

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
      const startDate = new Date(this.currentComprehensive.detail.start_date)
      const endDate = new Date(this.currentComprehensive.detail.end_date)
      const nowDate = new Date()
      if (nowDate >= startDate && nowDate < endDate) {
        return {
          type: "success",
          msg: "进行中"
        }
      } else if (nowDate < startDate) {
        return {
          type: "warning",
          msg: "未开始"
        }
      } else if (nowDate >= startDate) {
        return {
          type: "danger",
          msg: "已结束"
        }
      }
      return {
        type: "info",
        msg: "null"
      }
    },
    getTitle(): string {
      return this.currentComprehensive.detail.title ? this.currentComprehensive.detail.title : '无'
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