import { request } from './http'

export interface Item {
  id: number
  title: string
  created_at: string
}

export interface ItemCreate {
  title: string
}

/**
 * 获取待办列表
 */
export function listItems(): Promise<Item[]> {
  return request<Item[]>({
    url: '/api/items',
    method: 'GET'
  })
}

/**
 * 创建新的待办项
 */
export function createItem(title: string): Promise<Item> {
  return request<Item>({
    url: '/api/items',
    method: 'POST',
    data: { title }
  })
}
