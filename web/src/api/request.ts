import axios, {AxiosRequestConfig} from 'axios'

export async function request<T>(config: AxiosRequestConfig<any>): Promise<T> {
  const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
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
  }, error => Promise.reject(error.response ? error.response.data : error))

  return instance.request<T>(config).then(res => res.data)
}
