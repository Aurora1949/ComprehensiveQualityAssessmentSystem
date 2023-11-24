import {defineStore} from "pinia"
import {User} from "@/types/user.ts";
import {getUserInfo} from "@/api/user.ts";

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