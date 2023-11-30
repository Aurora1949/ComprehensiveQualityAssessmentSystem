import {request} from "@/api/request.ts";
import qs from 'qs'
import {IToken, IUserLogin} from "@/types";

export async function userLogin(user: IUserLogin) {
  return request<IToken>({
    url: '/token',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: qs.stringify(user)
  })
}
