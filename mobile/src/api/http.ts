import { API_BASE_URL } from '../config'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
}

interface ResponseData<T = any> {
  data: T
  statusCode: number
  errMsg: string
}

export async function request<T = any>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, header = {} } = options

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header
      },
      timeout: 10000,
      success: (res: ResponseData<T>) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          uni.showToast({
            title: `请求失败: ${res.statusCode}`,
            icon: 'none',
            duration: 2000
          })
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '网络请求失败',
          icon: 'none',
          duration: 2000
        })
        reject(err)
      }
    })
  })
}
