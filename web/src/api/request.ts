import axios, {AxiosError, AxiosRequestConfig} from 'axios'

export async function request<T = unknown>(config: AxiosRequestConfig<any>): Promise<T> {
  const instance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 5000,
    headers: {},
    withCredentials: true
  })

  instance.interceptors.request.use(config => {
    let token = sessionStorage.getItem("token")
    if (!token) token = localStorage.getItem("token")
    if (token) config.headers['Authorization'] = `Bearer ${token}`
    else config.headers['Authorization'] = ''
    return config
  }, error => error)
  // bug fixed on csdn https://blog.csdn.net/qq_45325810/article/details/120704910
  instance.interceptors.response.use(resource => {
    if (resource.status === 200) return resource
    return Promise.reject(new Error(resource.data))
  }, (error: AxiosError) => {
    return Promise.reject(error.response ? error.response.data : error.code)
  })

  return instance.request<T>(config).then(res => res.data)
}
